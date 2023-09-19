# Test with cert in MacOS Keychain

## Update Certificate Selector
* Open `selector.json`
```json
[
    {
      "Key": "x509Subject",
      "Value": "CN=MacOS Client,OU=Cloud Security,O=Test Company,L=London,ST=England,C=GB"
    },
    {
      "Key": "x509Issuer",
      "Value": "CN=Test Company Root CA,O=Test Company,L=London,ST=England,C=GB"
    },
    {
      "Key": "x509Serial",
      "Value": "7C2218B31614DE69CFB8BA2F54781C6B88C7C48A"
    }
  ]
```
* serial number needs to be updated with that of your MacOS client certificate
* In MacOS Keychain, My Certificates, open MacOS client certificate

<kbd>
  <img src="images/keychain-macos-client-cert.png" width="500">
</kbd>

* copy the certificate serial number
* paste into the `x509Serial` value field
* remove spaces

## Initial MacOS client test
* copy `examples/macos-test.example` into the repo directory
* rename the file extension to `.sh`
```
./aws_signing_helper credential-process \
    --cert-selector file://selector.json \
    --trust-anchor-arn "arn:aws:rolesanywhere:eu-west-2:012345678901:trust-anchor/0b855d05-6a40-4eea-af88-b9e9e0d60156" \
    --profile-arn "arn:aws:rolesanywhere:eu-west-2:012345678901:profile/b62e420d-2af7-4f3b-afd1-e631e2242744" \
    --role-arn "arn:aws:iam::012345678901:role/roles-anywhere-s3-full-access"
```
* update with your AWS Account number, region and ARNs
* copy and paste into your terminal
* press enter
* temporary AWS credentials should be returned in JSON format:
```json
{
  "Version":1,
  "AccessKeyId":"ASIA2L5BHF3A55HVXRPZ",
  "SecretAccessKey":"l06S3HyTG3fR/zZ0qDGzR1a0ziCztD7/97fsUvzX","SessionToken":"IQoJb3JpZ2luX2VjEKj//////////wEaCWV1LXdlc3QtMiJHMEUCIQCYykiyQpbdJTSPKl+W9sX55i2VKnqL5CmCrHwlRX7OswIgTIyi+LgJqNBTvBZPzHopm23l3btYt3dDIu7xtjFKprgqmgQIkf//////////ARAEGgw3MTI3NjU4MTI0MTciDFjj6NYsuNV+wYCrtCruA0sdP8rw6xL7KFs7KLtCc1M9mK/2M/+I2ZKm3quoSa1XQYvVLaqQ8uL5qMzx3XRr0D0vDzLlBGb6v4KGT+7jqeGZbfnt2UbYh9Ae6Q2A6/3W3fzCFxAFmVLv8/NlZ9pMPSurv/NZB1BRYb78PBfQYtCeSnbKh8TDX71GxkfN20CZvguiCZjwEXLPxMmDadZOYUkBfAo3zBIhAA1Sp1KSnMCy0Z4f9yb5Zo5fZ0rY2YN/QQmqW3Dz8fXrH+U9bk5L/PhaBZ3eDhbhcw5NYFFe3/nFOIJ5T0z8J2Exqe89Hact+VxCHlsSAYn55Ip2R8ORd6sVglGFgVSCnmFHvmkXuujEhXs5gXZ2AabPl/2jJsZ8e1mV6yVvjmcSn7Khzqmir3mKyBtz5wK1P9/sNchmcnZY+sCGsGXfh0FISjqFXTu+nIAUKA32adYfKepztV30x/v/Z6qk044AQUEuRD4kc7fI9JXKc1WIl5IC1pP45E7jQUOWhWSPAoyqpt+uTvNhix+WsdE8DrhkJEcAUuapafnLOn8lXz2StpW01rz8JP77UX4u7a2lxoGcNGFuq0bbgKvUlxMa3GrW5sa7HkhtIPzGip/KCRIdKt5R/SxSW5mlZbzRjDOeMPlIshqWQJnXQbASMRJLtjSnhsEUADOYMIvGnKgGOvMBRo7IY+bP990QxxIsC4imQxphZmFx93jsDEHLHRGkWsiOhqgzR41FSGb6TZmLj/5qG7rF4RaFmbHnpTLsfw9HVAlVuKKuGJ2+IlztvXlRxwiJEKFds8E93onCpNnYe6cfjmtZUaRugBP4ZUKP8/+humpTDrsLGeYhTbySSr3YEjuCzeXwNcaUU185rPPljGwFdqMthp5jntLbBd6mWSSXPLz32cFT3msuJrmnXCBNRjiDEK6GPZo/qcNdVbLAKaTEP7HUK32OTvWd0JdiFMFYGPIyLUThyyXhLYSrsUHWWIGN6RAPITfjf7782eys6onr48he","Expiration":"2023-09-17T17:02:19Z"
  }
```

## Set MacOS client variables automatically
* copy `examples/get-macos-creds.example` into the repo directory and rename it with a `.sh` extension
* format of file:
```
export $(./aws_signing_helper credential-process \
    --cert-selector file://selector.json \
    --trust-anchor-arn "arn:aws:rolesanywhere:eu-west-2:012345678901:trust-anchor/0b855d05-6a40-4eea-af88-b9e9e0d60156" \
    --profile-arn "arn:aws:rolesanywhere:eu-west-2:012345678901:profile/b62e420d-2af7-4f3b-afd1-e631e2242744" \
    --role-arn "arn:aws:iam::012345678901:role/roles-anywhere-s3-full-access" | python get_creds.py)
```
* substitute your ARNs
* copy and paste the script to your terminal
* press enter

<kbd>
  <img src="images/keychain-authorise.png" width="300">
</kbd>

* enter your MacOS password
* press Always Allow

## Test MacOS client access
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

## View connection details
* At IAM, Roles, Roles Anywhere, navigate to your region
* Select Subject Activity

<kbd>
  <img src="images/subject-activity.png" width="300">
</kbd>

* A record of connections using the original and MacOS certificates can be seen
* Click on one of the links to view the certificate used to authenticate
