resource "kubernetes_namespace" "nginx" {
  metadata {
    name = "nginx"
  }

  depends_on = [
    kind_cluster.default,
  ]
}

resource "helm_release" "nginx" {
  name       = "ingress-nginx"
  namespace  = kubernetes_namespace.nginx.metadata[0].name
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  version    = "4.11.3"

  set {
    name  = "namespace"
    value = kubernetes_namespace.nginx.id
  }


  depends_on = [
    kind_cluster.default,
    kubernetes_namespace.nginx
  ]
}
