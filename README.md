### s3web
Someone on Reddit was asking about copying files from the web to S3, so I thought I'd make something that does that.
It's not the greatest thing ever, but it does what it's intended to do.

I haven't tested this on files with spaces, and I'm guessing that's going to cause an issues.

#### Requirements
Make sure you have all the packages in the requirements.txt, `pip3 install requirements.txt`
Make sure that the AWS CLI is installed `pip install awscli`
Make sure that your AWS credentials are added to your ~/.aws directory. `aws configure`

#### Usage
Fairly straight forward, I modeled the syntax from the AWS CLI. This will take a file from the web, download it to the local /tmp directory, upload it to S3, and remove the temp file.
```bash
./s3web.py http://google/test.zip s3://bucket/folder/test.txt
```
You can interchange the arguments, the order doesn't matter.

#### Todo:
- [ ] Check if the file exists and prompt for overwrite
- [ ] Add logging
- [ ] Tests
- [X] Add arg for status message, the current status tracker creates a lot of output if the file size is large
- [ ] Refactor some of this. It's a bit messy, but works for a first time go at it.
- [ ] Use bucket filename instead of filename from web, if specified.
- [X] Flag to keep temp file.
- [ ] Port this to AWS Lambda - Might run in to file size issues though, might be a whole new project using API Gateway, etc.
- [ ] Bit of a stretch goal - Download entire directories. Might be difficult to tree

