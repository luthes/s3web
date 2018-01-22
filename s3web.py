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
    return file_name


def boto_cp(temp_file, s3_bucket):
    s3 = boto3.resource('s3')
    file_data = open('/tmp/' + temp_file, "rb")
    s3_url = parse_s3_url(s3_bucket)
    s3_bucket = s3_url.netloc
    s3_file_path = s3_url.path[1:]
    s3.Bucket(str(s3_bucket)).put_object(Bucket=s3_bucket, Key=str(s3_file_path), Body=file_data)
    return


def main():
    helptext = '<S3 Bucket> <HTTP/S location> or <HTTP/S location> <S3 Bucket>'
    parser = argparse.ArgumentParser(description='Get web URL and upload to S3 Bucket')
    args = parser.add_argument('strings', type=str, nargs=2, help=helptext)
    strings = (parser.parse_args()).strings

    if strings[0].startswith('s3'):
        s3_url = strings[0]
        http_url = strings[1]
    else:
        s3_url = strings[1]
        http_url = strings[0]

    # Global temp file location
    temp_file_name = get_file_name(http_url)
    # Temp file location for cleanup
    temp_file_location = '/tmp/' + get_file_name(http_url)
    # Global S3 File Location
    s3_path = str(s3_url + temp_file_name)

    # Download File from Web address
    print('Getting file from web: ' + http_url)
    get_file(http_url)

    # Copy file to S3
    print('Putting file to bucket: ' + s3_path)

    # TODO: Check if file exists in bucket, and prompt for overwrite, maybe add arg for auto overwrite

    # S3_URL + FileName
    boto_cp(temp_file_name, s3_path)

    # Clean up temp files
    os.remove(temp_file_location)
    print('Cleaning up temp file: ' + temp_file_location)


if __name__ == '__main__':
    main()

