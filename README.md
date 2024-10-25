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


another little hack cus we dont want to be creating secrets all over the place - just trying to keep this project as simple as possible for now
`kubectl get sa mongodb-database -n mongodb -o yaml | sed 's/namespace: mongodb/namespace: default/' | kubectl apply -f -`
