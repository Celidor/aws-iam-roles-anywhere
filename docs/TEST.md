# Test with unrestricted policy
* At this stage we should have read access to any S3 bucket in the AWS account

## Download AWS IAM Roles Anywhere Credential Helper
* [Download](https://docs.aws.amazon.com/rolesanywhere/latest/userguide/credential-helper.html) the AWS IAM Roles Anywhere Credential Helper tool for your operating system
* If using MacOS or Linux, copy the binary into this repository
* Alternatively copy to another location, e.g. `usr/bin/local` and set directory in your `PATH` by editing your `.zshrc` file on MacOS

## Set file permissions on MacOS
* remove file name extended attribute
```
xattr -c aws_signing_helper
```
* set as executable
```
chmod 755 aws_signing_helper
```

## Test
* substitute the ARNs below with your values
* you can create and use a file `my-test.sh` as that is already included in `.gitignore`
```
./aws_signing_helper credential-process \
    --certificate ./crypto/client/test-client.pem \
    --private-key ./crypto/client/test-client.key \
    --trust-anchor-arn <anchor-arn> \
    --profile-arn <profile-arn> \
    --role-arn <role-arn>
```
* enter the command
* you should receive a response like this:
```
{"Version":1,"AccessKeyId":"ASIA2L5BHF3A55HVXRPZ","SecretAccessKey":"l06S3HyTG3fR/zZ0qDGzR1a0ziCztD7/97fsUvzX","SessionToken":"IQoJb3JpZ2luX2VjEKj//////////wEaCWV1LXdlc3QtMiJHMEUCIQCYykiyQpbdJTSPKl+W9sX55i2VKnqL5CmCrHwlRX7OswIgTIyi+LgJqNBTvBZPzHopm23l3btYt3dDIu7xtjFKprgqmgQIkf//////////ARAEGgw3MTI3NjU4MTI0MTciDFjj6NYsuNV+wYCrtCruA0sdP8rw6xL7KFs7KLtCc1M9mK/2M/+I2ZKm3quoSa1XQYvVLaqQ8uL5qMzx3XRr0D0vDzLlBGb6v4KGT+7jqeGZbfnt2UbYh9Ae6Q2A6/3W3fzCFxAFmVLv8/NlZ9pMPSurv/NZB1BRYb78PBfQYtCeSnbKh8TDX71GxkfN20CZvguiCZjwEXLPxMmDadZOYUkBfAo3zBIhAA1Sp1KSnMCy0Z4f9yb5Zo5fZ0rY2YN/QQmqW3Dz8fXrH+U9bk5L/PhaBZ3eDhbhcw5NYFFe3/nFOIJ5T0z8J2Exqe89Hact+VxCHlsSAYn55Ip2R8ORd6sVglGFgVSCnmFHvmkXuujEhXs5gXZ2AabPl/2jJsZ8e1mV6yVvjmcSn7Khzqmir3mKyBtz5wK1P9/sNchmcnZY+sCGsGXfh0FISjqFXTu+nIAUKA32adYfKepztV30x/v/Z6qk044AQUEuRD4kc7fI9JXKc1WIl5IC1pP45E7jQUOWhWSPAoyqpt+uTvNhix+WsdE8DrhkJEcAUuapafnLOn8lXz2StpW01rz8JP77UX4u7a2lxoGcNGFuq0bbgKvUlxMa3GrW5sa7HkhtIPzGip/KCRIdKt5R/SxSW5mlZbzRjDOeMPlIshqWQJnXQbASMRJLtjSnhsEUADOYMIvGnKgGOvMBRo7IY+bP990QxxIsC4imQxphZmFx93jsDEHLHRGkWsiOhqgzR41FSGb6TZmLj/5qG7rF4RaFmbHnpTLsfw9HVAlVuKKuGJ2+IlztvXlRxwiJEKFds8E93onCpNnYe6cfjmtZUaRugBP4ZUKP8/+humpTDrsLGeYhTbySSr3YEjuCzeXwNcaUU185rPPljGwFdqMthp5jntLbBd6mWSSXPLz32cFT3msuJrmnXCBNRjiDEK6GPZo/qcNdVbLAKaTEP7HUK32OTvWd0JdiFMFYGPIyLUThyyXhLYSrsUHWWIGN6RAPITfjf7782eys6onr48he","Expiration":"2023-09-17T17:02:19Z"}
```

## set variables automatically
* for ease of use, create a file `get-creds.sh` (already included in `.gitignore`)
* enter:
```
export $(./aws_signing_helper credential-process \
    --certificate ./crypto/client/test-client.pem \
    --private-key ./crypto/client/test-client.key \
    --trust-anchor-arn <anchor-arn> \
    --profile-arn <profile-arn> \
    --role-arn <role-arn> | python get_creds.py)
```
* substitute your ARNs
* copy and paste the script to your terminal
* press enter

## test access
* check AWS identity, this should succeed
```
aws sts get-caller-identity
```
* list all S3 buckets, this should fail as access is only allowed to a single bucket
```
aws s3 ls
An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied
```
* download a file from the designated S3 bucket, this should succeed
* replace the example below with your own S3 bucket and object
```
aws s3 cp s3://celidor-confidential/confidential.png confidential.png
download: s3://celidor-confidential/confidential.png to ./confidential.png
```
