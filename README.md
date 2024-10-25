README


1.
```
cd terraform
export TF_VAR_home_directory="$HOME" \
export TF_VAR_github_token=$GITHUB_TOKEN \
terraform init; terraform apply
```



once mongo is live u need to run:

<!-- this is a demo password obviously - u can input whatever you want -->
`kubectl create secret generic base-secret --from-literal=password=secret123`

After the MongoDBCommunity resource is running, the Operator no longer requires the user's secret. MongoDB recommends that you securely store the user's password and then delete the user secret:
`kubectl delete secret base-secret`