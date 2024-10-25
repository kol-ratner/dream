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