- [ ] Implement the `Ensure a log metric filter and alarm `exist for usage of "root" account recommendation in the Monitoring section of this benchmark to receive notifications of root account usage.

Find out the last time the root account was used:

`aws iam generate-credential-report`

`aws iam get-credential-report --query 'Content' --output text | base64 -D | cut -d, -f1,5,11,16 | grep -B1 '<root_account>'`

- [ ] Follow the remediation instructions of the Ensure IAM policies are attached only to groups or roles [recommendation](http://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [ ] Find out if a MFA device is enabled for all IAM users having a console password:
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
## Check credentials not used in last 90 or greater
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
1. For each user having password_enabled set to TRUE , ensure password_last_used_date is less than 90 days ago.
 When password_enabled is set to TRUE and password_last_used is set to No_Information , ensure password_last_changed is less than 90 days ago.
3. For each user having an access_key_1_active or access_key_2_active to TRUE , ensure the corresponding access_key_n_last_used_date is less than 90 days ago.
 When a user having an access_key_x_active (where x is 1 or 2) to TRUE and corresponding access_key_x_last_used_date is set to N/A', ensureaccess_key_x_last_rotated` is less than 90 days ago.



Linux, OS X, Unix
> `export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE`

> `export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

Windows:
> set AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
> set AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

You can use the following command to retrieve the details about your IAM entities and then save them to a JSON file (the default output format).

> aws iam get-account-authorization-details > output.json