# aws-iam-roles-anywhere
Testing AWS IAM Roles Anywhere
* create test CA and client certificate locally using Python Cryptography module

## important warning
The code in this repository is for test purposes only and is not suitable for a production certificate authority. 

A production certificate authority should have its keys generated in a Hardware Security Module (HSM) and it should not be possible to export the private key from the HSM.

With this code, private keys are held locally on disk, and loss of these could potentially lead to takeover of your AWS Accounts.

## set up Python virtual environment
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## create test certs
```
python main.py
```

## test AWS IAM Roles Anywhere
[Create Trust Anchor](docs/TRUST_ANCHOR.md)  
[Create IAM Role](docs/IAM_ROLE.md)  
[Create Roles Anywhere Profile](docs/PROFILE.md)  
[Test AWS IAM Roles Anywhere](docs/TEST.md)  

## acknowledgement
[Medium article by Roy Ben](https://medium.com/cyberark-engineering/calling-aws-services-from-your-on-premises-servers-using-iam-roles-anywhere-3e335ed648be)