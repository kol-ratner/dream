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
  values = [
    <<-EOT
    configs:
      applications:
        - name: root-app
          namespace: argocd
          project: default
          source:
            repoURL: 'https://github.com/kol-ratner/dream.git'
            targetRevision: HEAD
            path: kubernetes/apps
          destination:
            server: https://kubernetes.default.svc
            namespace: argocd
          syncPolicy:
            automated:
              prune: true
              selfHeal: true
    EOT
  ]

  depends_on = [
    kind_cluster.default,
    local_file.kubeconfig,
    kubernetes_namespace.argocd
  ]
}

# resource "helm_release" "argocd_image_updater" {
#   name       = "argocd-image-updater"
#   namespace  = kubernetes_namespace.argocd.metadata[0].name
#   repository = "https://argoproj.github.io/argo-helm"
#   chart      = "argocd-image-updater"
#   # version    = "7.6.12"

#   depends_on = [
#     kind_cluster.default,
#     local_file.kubeconfig,
#     kubernetes_namespace.argocd
#   ]
# }
