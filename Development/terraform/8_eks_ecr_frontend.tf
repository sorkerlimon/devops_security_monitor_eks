# ===========================================
# ECR Repository for Frontend Application
# ===========================================

# ECR Repository for Frontend
resource "aws_ecr_repository" "frontend" {
  name                 = "devops-frontend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Name        = "devops-frontend-ecr"
    Environment = "Development"
    Project     = "DevOps"
    Application = "Frontend"
  }
}

# ===========================================
# Outputs
# ===========================================

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.frontend.repository_url
}

output "ecr_repository_arn" {
  description = "ARN of the ECR repository"
  value       = aws_ecr_repository.frontend.arn
}

output "ecr_registry_id" {
  description = "Registry ID of the ECR repository"
  value       = aws_ecr_repository.frontend.registry_id
}

output "ecr_repository_name" {
  description = "Name of the ECR repository"
  value       = aws_ecr_repository.frontend.name
}

