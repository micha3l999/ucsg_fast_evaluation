# AWS - ucsg_fast_evaluation

Each lambda is stored under its respectively folder.

### Before to run it
If you do not have any of these lambdas created in your AWS account with the same name, remember 
replace those names in the `./bash` file or, use the command `create-function` instead `update-function-code` 
in the same file.

### Updating a lambda via terminal
To update a lambda in AWS, run this command at folder level

E.g. updating `lambda_example` lambda:

- `cd ./lambda_example`

- `. ./bash.sh`

## Testing a lambda
To test a lambda, create a lambda_event.json file in each lambda folder and add the body to test the lambda

### References

- If you want to check what are your AWS profiles, check this [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

- If you want to learn more about `aws cli` and the commands related with lambda, check this [one](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/index.html).