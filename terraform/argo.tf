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
