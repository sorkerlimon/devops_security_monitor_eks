# ===========================================
# ECR Repository for Backend Application
# ===========================================

# ECR Repository for Backend
resource "aws_ecr_repository" "backend" {
  name                 = "devops-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Name        = "devops-backend-ecr"
    Environment = "Development"
    Project     = "DevOps"
    Application = "Backend"
  }
}

# ===========================================
# Outputs
# ===========================================

output "ecr_backend_repository_url" {
  description = "URL of the ECR backend repository"
  value       = aws_ecr_repository.backend.repository_url
}

output "ecr_backend_repository_arn" {
  description = "ARN of the ECR backend repository"
  value       = aws_ecr_repository.backend.arn
}

output "ecr_backend_registry_id" {
  description = "Registry ID of the ECR backend repository"
  value       = aws_ecr_repository.backend.registry_id
}

output "ecr_backend_repository_name" {
  description = "Name of the ECR backend repository"
  value       = aws_ecr_repository.backend.name
}
