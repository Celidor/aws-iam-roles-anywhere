# Create IAM Roles Anywhere Profile
* Search for IAM Roles Anywhere
* This will take you to IAM, Roles, Roles Anywhere
* Create a profile
* This is an optional [session policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session) which further limits permissions
* Effective permissions are the intersection of the session and role policies
* Enter a name for the profile, e.g. `s3-read-access-single-bucket`
* Select the role you created earlier
* Copy and Paste the trust policy below
* Replace `<BUCKET_ARN>` with one of your S3 buckets
```json
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Effect":"Allow",
      "Action":"s3:Get*",
      "Resource":[
        "<BUCKET ARN>",
        "<BUCKET ARN>/*"
      ]
    }
  ]
}
```
<kbd>
  <img src="images/create-profile.png" width="500">
</kbd>

* Press Create a Profile
* You will now see both the Trust Anchor and Profile in the Roles Anywhere configuration

<kbd>
  <img src="images/roles-anywhere-config.png" width="500">
</kbd>
