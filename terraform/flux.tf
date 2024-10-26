
data "github_repository" "this" {
  name = var.github_repository
}

# ==========================================
# Bootstrap KinD cluster
# ==========================================

resource "flux_bootstrap_git" "this" {
  depends_on = [data.github_repository.this]

  embedded_manifests = true
  path               = "kubernetes/clusters/kind"
  components_extra   = ["image-reflector-controller", "image-automation-controller"]
}
