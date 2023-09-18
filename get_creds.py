import json
import sys

creds = json.loads(sys.stdin.read())
print(
    f"AWS_ACCESS_KEY_ID={creds['AccessKeyId']} AWS_SECRET_ACCESS_KEY={creds['SecretAccessKey']} AWS_SESSION_TOKEN={creds['SessionToken']}"
)
