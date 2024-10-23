variable "home_directory" {
  default = "/home/" # Replace with the actual path to the home directory
}

variable "github_token" {
  description = "GitHub token"
  sensitive   = true
  type        = string
  default     = ""
}

variable "github_org" {
  description = "GitHub organization"
  type        = string
  default     = "kol-ratner"
}

variable "github_repository" {
  description = "GitHub repository"
  type        = string
  default     = "dream"
}
