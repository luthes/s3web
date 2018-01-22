### s3web
Someone on Reddit was asking about copying files from the web to S3, so I thought I'd make something that does that.
It's not the greatest thing ever, but it does what it's intended to do.

I haven't tested this on files with spaces, and I'm guessing that's going to cause an issues.

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
- [ ] Add arg for status message, the current status tracker creates a lot of output if the file size is large
- [ ] Refactor some of this. It's a bit messy, but works for a first time go at it.
- [ ] Use bucket filename instead of filename from web, if specified.
- [ ] Flag to keep temp file.

