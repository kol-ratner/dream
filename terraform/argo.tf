resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }

  depends_on = [
    kind_cluster.default,
    local_file.kubeconfig
  ]
}

resource "helm_release" "argocd" {
  name       = "argocd"
  namespace  = kubernetes_namespace.argocd.metadata[0].name
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "7.6.12"

  depends_on = [
    kind_cluster.default,
    local_file.kubeconfig,
    kubernetes_namespace.argocd
  ]
}

# resource "kubernetes_ingress" "argocd" {
#   wait_for_load_balancer = true
#   metadata {
#     name      = "argocd-server"
#     namespace = kubernetes_namespace.argocd.id
#     annotations = {
#       "kubernetes.io/ingress.class" = "nginx"
#     }
#   }

#   spec {
#     rule {
#       http {
#         path {
#           path = "/"
#           backend {
#             service_name = "argocd-server"
#             service_port = 80
#           }
#         }
#       }
#     }
#   }
# }

# output "load_balancer_hostname" {
#   value = kubernetes_ingress.argocd.status.0.load_balancer.0.ingress.0.hostname
# }
