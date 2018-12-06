## 1. Avoid using "root" account
Implement the `Ensure a log metric filter and alarm `exist for usage of "root" account recommendation in the Monitoring section of this benchmark to receive notifications of root account usage.

Find out the last time the root account was used:

`aws iam generate-credential-report`

`aws iam get-credential-report --query 'Content' --output text | base64 -D | cut -d, -f1,5,11,16 | grep -B1 '<root_account>'`

Follow the remediation instructions of the Ensure IAM policies are attached only to groups or roles [recommendation](http://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
Find out if a MFA device is enabled for all IAM users having a console password:
Via Management Console
1. Open the IAM console 
2. In the left pane, select Users
3. If the MFA Device or Password columns are not visible in the table, click the gear
icon at the upper right corner of the table and ensure a checkmark is next to both,
then click Close .
4. Ensure each user having a checkmark in the Password column also has a value in the
MFA Device column.
Via the CLI
5. Run the following command (OSX/Linux/UNIX) to generate a list of all IAM users along with their password and MFA status:
` aws iam generate-credential-report`

    `aws iam get-credential-report --query 'Content' --output text | base64 -D | cut -d, -f1,4,8`

6. The output of this command will produce a table similar to the following:
user,password_enabled,mfa_active
elise,false,false
brandon,true,true
rakesh,false,false
helene,false,false
paras,true,true
anitha,false,false
:fire: For any column having password_enabled set to true , ensure mfa_active is also set to true
## 1.2 Ensure multi-factor authentication (MFA) is enabled for all IAM users that have a console password
Perform the following to determine if a MFA device is enabled for all IAM users having a console password:
Via Management Console
1. Open the IAM console at https://console.aws.amazon.com/iam/.
2. In the left pane, select Users
3. If the MFA Device or Password columns are not visible in the table, click the gear
icon at the upper right corner of the table and ensure a checkmark is next to both,
then click Close .
4. Ensure each user having a checkmark in the Password column also has a value in the
MFA Device column.
Via the CLI
1. Run the following command (OSX/Linux/UNIX) to generate a list of all IAM users along with their password and MFA status:
    `aws iam generate-credential-report1`

    `   aws iam get-credential-report --query 'Content' --output text | base64 -d | cut -d, -f1,4,8`

2. The output of this command will produce a table similar to the following:
```
user,password_enabled,mfa_active
elise,false,false
brandon,true,true
rakesh,false,false
helene,false,false
paras,true,true
anitha,false,false
```
For any column having password_enabled set to true , ensure mfa_active is also set to true.
### Remediation:
Perform the following to enable MFA:
1. Sign in to the AWS Management Console and open the IAM console at https://console.aws.amazon.com/iam/.
2. In the navigation pane, choose Users.
3. In the User Name list, choose the name of the intended MFA user.
4. Choose the Security Credentials tab, and then choose Manage MFA Device.
5. In the Manage MFA Device wizard, choose A virtual MFA device, and then choose
Next Step.

##1.3  Check credentials not used in last 90 or greater
AWS IAM users can access AWS resources using different types of credentials, such as passwords or access keys. It is recommended that all credentials that have been unused in 90 or greater days be removed or deactivated.
###Rationale:
Disabling or removing unnecessary credentials will reduce the window of opportunity for credentials associated with a compromised or abandoned account to be used.
###Audit:
Perform the following to determine if unused credentials exist:
Download Credential Report:
Using Management Console:
1. Login to the AWS Management Console
2. Click Services
3. Click IAM
4. Click on Credential Report
5. This will download an .xls file which contains credential usage for all users within an AWS Account - open this file

Via CLI
1. Run the following commands:
   ` aws iam generate-credential-report`

    `aws iam get-credential-report --query 'Content' --output text | base64 -D | cut -d, -f1,4,5,6,9,10,11,14,15,16`

    Ensure unused credentials does not exist:
2. For each user having password_enabled set to TRUE , ensure password_last_used_date is less than 90 days ago.

    When password_enabled is set to TRUE and password_last_used is set to No_Information , ensure password_last_changed is less than 90 days ago.
3. For each user having an access_key_1_active or access_key_2_active to TRUE , ensure the corresponding access_key_n_last_used_date is less than 90 days ago.

    When a user having an access_key_x_active (where x is 1 or 2) to TRUE and corresponding access_key_x_last_used_date is set to N/A', ensureaccess_key_x_last_rotated` is less than 90 days ago.



Linux, OS X, Unix
> `export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE`

> `export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

Windows:
> set AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
> set AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

You can use the following command to retrieve the details about your IAM entities and then save them to a JSON file (the default output format).

> aws iam get-account-authorization-details > output.json
### Remediation:
Perform the following to remove or deactivate credentials:
1. Login to the AWS Management Console:
2. Click Services
3. Click IAM
4. Click on Users
5. Click on Security Credentials
6. As an Administrator
Click on Make Inactive for credentials that have not been used in 90 Days
7. As an IAM User
Click on Make Inactive or Delete for credentials which have not been used in 90 Days
## 1.4 Ensure access keys are rotated every 90 days or less
### Rationale:
Rotating access keys will reduce the window of opportunity for an access key that is associated with a compromised or terminated account to be used.
Access keys should be rotated to ensure that data cannot be accessed with an old key which might have been lost, cracked, or stolen.
Audit:
Perform the following to determine if access keys are rotated as prescribed:
1. Login to the AWS Management Console
2. Click Services
3. Click IAM
4. Click on Credential Report
5. This will download an .xls file which contains Access Key usage for all IAM users within an AWS Account - open this file
6. Focus on the following columns (where x = 1 or 2)
`access_key_X_active`
`access_key_X_last_rotated`
7. Ensure all active keys have been rotated within 90 days 

Via CLI
```
aws iam generate-credential-report
aws iam get-credential-report --query 'Content' --output text | base64 -d
```
### Remediation:
Perform the following to rotate access keys:
1. Login to the AWS Management Console:
2. Click Services
3. Click IAM
4. Click on Users
5. Click on Security Credentials
6. As an Administrator
    Click on Make Inactive for keys that have not been rotated in 90 Days
7. As an IAM User
    Click on Make Inactive or Delete for keys which have not been rotated or used in 90 Days
8. Click on `Create Access Key`
9. Update programmatic call with new Access Key credentials
Via CLI
    ```
    aws iam update-access-key
    aws iam create-access-key
    aws iam delete-access-key
    ```
## 1.5 Ensure IAM password policy requires at least one uppercase letter
Via CLI
`aws iam get-account-password-policy`
Ensure the output of the above command includes "RequireUppercaseCharacters": true
Via CLI
`aws iam update-account-password-policy --require-uppercase-characters`
## 1.6 Ensure IAM password policy requires at least one lowercase letter
Via CLI
`aws iam get-account-password-policy`
Ensure the output of the above command includes "RequireUppercaseCharacters": true
Via CLI
`aws iam update-account-password-policy --require-lowercase-characters`

