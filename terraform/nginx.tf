resource "kubernetes_namespace" "nginx" {
  metadata {
    name = "nginx"
  }

  depends_on = [
    kind_cluster.default,
    local_file.kubeconfig
  ]
}

resource "helm_release" "ingress_nginx" {
  name       = "ingress-nginx"
  namespace  = kubernetes_namespace.nginx.id
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  version    = "4.11.3"

  set {
    name  = "namespace"
    value = kubernetes_namespace.nginx.id
  }
  set {
    name  = "controller.kind"
    value = "DaemonSet"
    type  = "string"
  }
  set {
    name  = "controller.ingressClass"
    value = "nginx"
    type  = "string"
  }
  set {
    name  = "controller.hostPort.enabled"
    value = true
    type  = "string"
  }
  set {
    name  = "controller.service.type"
    value = "NodePort"
    type  = "string"
  }

  depends_on = [
    kind_cluster.default,
    local_file.kubeconfig,
    kubernetes_namespace.nginx
  ]
}
