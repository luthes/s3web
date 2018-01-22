# S3 Web

Someone on Reddit was asking about copying files from the web to S3, so I thought I'd make something that does that.
It's not the greatest thing ever, but it does what it's intended to do.

I haven't tested this on files with spaces, and I'm guessing that's going to cause an issues.

## Todo:
- [ ] Check if the file exists and prompt for overwrite
- [ ] Add logging
- [ ] Tests
- [ ] Add arg for status message, the current status tracker creates a lot of output if the file size is large
- [ ] Refactor some of this. It's a bit messy, but works for a first time go at it.
