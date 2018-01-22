#!/usr/bin/python3

'''
TODO: Add logging instead of print statements.

Uses the AWS CLI to take files from the web, and move them to S3.
Uses your AWS config file to upload.
1. Download the specified file to /tmp
      - Check the file path for spaces
      -
2. Use boto to copy the file returned from the download function (eg. /tmp/img.jpg)
3. Remove the temp file
'''


import os
import logging
import boto3
import argparse
import urllib.request
from urllib.parse import urlparse


# Set Logger
#boto3.set_stream_logger(name='botocore', level=4)


# Get File name from URL
def get_file_name(url):
    file_name = url.split('/')[-1]
    return file_name


# Create file path for temporary file
def temp_file_location(url):
    file_name = get_file_name(url)
    file_path = "/tmp/" + file_name
    return file_path


# This creates an S3 URL object, format as follows: bucket: s3_url.netloc; path: s3_url.path
def parse_s3_url(s3_url):
    s3_url = urlparse(s3_url)
    return s3_url


# Download https file
def get_file(url):
    # Download file to /tmp directory, maybe check if windows, probably not.
    file_name = get_file_name(url)
    u = urllib.request.urlopen(url)
    temp_file = '/tmp/' + file_name
    f = open(temp_file, 'wb')
    meta = u.info()
    file_size = int(meta.get_all("Content-Length")[0])

    file_size_dl = 0
    block_size = 8192
    while True:
        file_buffer = u.read(block_size)
        if not file_buffer:
            break
        file_size_dl += len(file_buffer)
        f.write(file_buffer)
        # TODO: Add arg for status because this generates a ton of console output if the file size is large.
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        print(status)
    return file_name


def boto_cp(temp_file, s3_bucket):
    s3 = boto3.resource('s3')
    file_data = open('/tmp/' + temp_file, "rb")
    s3_url = parse_s3_url(s3_bucket)
    s3_bucket = s3_url.netloc
    s3_file_path = s3_url.path[1:]
    s3.Bucket(str(s3_bucket)).put_object(Bucket=s3_bucket, Key=str(s3_file_path), Body=file_data)
    return


def remove_file(file_location):
    os.remove(file_location)
    return


def main():
    logging.basicConfig(filename='s3web.log',level=logging.DEBUG)
    helptext = '<S3 Bucket> <HTTP/S location> or <HTTP/S location> <S3 Bucket>'
    parser = argparse.ArgumentParser(description='Get web URL and upload to S3 Bucket',
                                     epilog='Written by Steven Luther - 2018\n\n'
                                            'For any issues or suggestions refer to Github\n'
                                            'https://github.com/luthes/s3web\n')
    parser.add_argument('strings',
                        type=str,
                        nargs=2,
                        help=helptext)

    # TODO: I don't think I need all of these bool args. One should be sufficient, and check True/False
    parser.add_argument('--progress',
                        dest='progress',
                        action='store_true',
                        help='Add progress message for downloading files, this is the default behavior.')
    parser.add_argument('--no-progress',
                        dest='progress',
                        action='store_false',
                        help='Remove progress message for downloading files.')
    parser.set_defaults(status=True)
    parser.add_argument('--cleanup',
                        dest='cleanup',
                        action='store_true',
                        help='Delete temp files after files are upload to S3, this is the default behavior.')
    parser.add_argument('--no-cleanup',
                        dest='cleanup',
                        action='store_false',
                        help='Keep temp files after S3 upload.')
    parser.set_defaults(cleanup=True)
    parser.add_argument('--dryrun',
                        dest='dryrun',
                        action='store_false',
                        help='Show file URL and S3 bucket files will be uploaded to/from')
    parser.add_argument('--no-dryrun',
                        dest='dryrun',
                        action='store_true',
                        help='Just upload the files...')
    parser.set_defaults(dryrun=False)
    strings = (parser.parse_args()).strings
    cleanup_arg = (parser.parse_args()).cleanup
    progress_arg = (parser.parse_args()).progress
    dryrun_arg = (parser.parse_args()).dryrun

    # Logging initialization needs to go here so we can get a log level from arguments
    logging.basicConfig(filename='s3web.log',
                        level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    # TODO Put these in a loop. I'm going to bed.
    logging.info('Argument: Key - {0} - Value {1}'.format("Strings", strings))
    logging.info('Argument: Key - {0} - Value {1}'.format("Cleanup", str(cleanup_arg)))
    logging.info('Argument: Key - {0} - Value {1}'.format("Progress", str(progress_arg)))
    logging.info('Argument: Key - {0} - Value {1}'.format("Dryrun", str(dryrun_arg)))

    if strings[0].startswith('s3'):
        s3_url = strings[0]
        http_url = strings[1]
        logging.debug('First string is the S3 bucket {0}'.format(s3_url))
        logging.debug('Second string is the web file {0}'.format(http_url))
    else:
        s3_url = strings[1]
        http_url = strings[0]
        logging.debug('First string is the web file {0}'.format(http_url))
        logging.debug('Second string is the S3 Bucket {0}'.format(s3_url))

    # Global temp file location
    temp_file_name = get_file_name(http_url)
    # Temp file location for cleanup
    temp_file = '/tmp/' + get_file_name(http_url)
    # Global S3 File Location
    s3_path = str(s3_url + temp_file_name)

    # Download File from Web address
    if dryrun_arg is False:
        print('Getting file from web: ' + http_url)
        get_file(http_url)

        # Copy file to S3
        print('Putting file to bucket: ' + s3_path)

        # TODO: Check if file exists in bucket, and prompt for overwrite, maybe add arg for auto overwrite
        # S3_URL + FileName
        logging.info('Starting transfer of files: {0} to {1}'.format(temp_file_name, s3_path))
        boto_cp(temp_file_name, s3_path)
        logging.info('Transfer of files complete')

        # Clean up temp files
        if cleanup_arg:
            logging.info('Cleanup set to True, removing temp file.')
            print('Cleaning up temp file: ' + temp_file)
            remove_file(temp_file)
            logging.debug('Cleanup complete, removed {0}'.format(str(temp_file)))
        else:
            print('Skipping Cleanup')
    else:
        logging.debug('Dry Run Enabled - Nothing moved')
        logging.debug('Getting file from web: ' + http_url)
        logging.debug('Putting file to bucket: ' + s3_path)
        logging.debug('Cleaning up temp file: ' + temp_file)
        print('Dry Run Enabled - Nothing moved')
        print('Getting file from web: ' + http_url)
        print('Putting file to bucket: ' + s3_path)
        print('Cleaning up temp file: ' + temp_file)


if __name__ == '__main__':
    main()

