# ===========================================
# ECR Permissions for EKS Node Group
# ===========================================

# ECR Repository Policy for Frontend - EKS Node Group Access
resource "aws_ecr_repository_policy" "frontend_eks_policy" {
  repository = aws_ecr_repository.frontend.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowEKSNodeGroupPullFrontend"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::299138067566:role/AmazonEKSAutoNodeRole"
        }
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
      }
    ]
  })

  depends_on = [aws_ecr_repository.frontend]
}

# ECR Repository Policy for Backend - EKS Node Group Access
resource "aws_ecr_repository_policy" "backend_eks_policy" {
  repository = aws_ecr_repository.backend.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowEKSNodeGroupPullBackend"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::299138067566:role/AmazonEKSAutoNodeRole"
        }
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
      }
    ]
  })

  depends_on = [aws_ecr_repository.backend]
}

# ===========================================
# Outputs
# ===========================================

output "ecr_policies_summary" {
  description = "Summary of ECR policies for EKS access"
  value = {
    frontend_policy = aws_ecr_repository_policy.frontend_eks_policy.id
    backend_policy  = aws_ecr_repository_policy.backend_eks_policy.id
    node_role_arn   = "arn:aws:iam::299138067566:role/AmazonEKSAutoNodeRole"
  }
}

output "ecr_access_status" {
  description = "ECR access configuration status"
  value = {
    frontend_repository = aws_ecr_repository.frontend.name
    backend_repository  = aws_ecr_repository.backend.name
    eks_node_access    = "Configured for pull operations"
  }
}
