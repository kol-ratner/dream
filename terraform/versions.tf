terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "0.6.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.33.0"
    }
    # helm = {
    #   source  = "hashicorp/helm"
    #   version = "2.16.1"
    # }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.1"
    }
    flux = {
      source  = "fluxcd/flux"
      version = "1.4.0"
    }
    # github = {
    #   source  = "fluxcd/flux"
    #   version = "6.1.0"
    # }
  }
}

provider "kind" {}

# provider "kubernetes" {
#   config_path = "~/.kube/config"
# }

# provider "helm" {
#   kubernetes {
#     config_path = "~/.kube/config"
#   }
# }

provider "local" {}

provider "flux" {
  kubernetes = {
    host                   = kind_cluster.default.endpoint
    client_certificate     = kind_cluster.default.client_certificate
    client_key             = kind_cluster.default.client_key
    cluster_ca_certificate = kind_cluster.default.cluster_ca_certificate
  }
  git = {
    url = "https://github.com/${var.github_org}/${var.github_repository}.git"
    http = {
      username = "git" # This can be any string when using a personal access token
      password = var.github_token
    }
  }
}

provider "github" {
  owner = var.github_org
  token = var.github_token
}
