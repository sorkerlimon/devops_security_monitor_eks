# ===========================================
# EKS Access Entries Configuration
# ===========================================

# Note: Node role and service role access entries are automatically created by EKS
# and cannot be manually created or modified through Terraform

# Access entry for technobd-limon-k user
resource "aws_eks_access_entry" "user_access" {
  cluster_name  = aws_eks_cluster.devops_cluster.name
  principal_arn = "arn:aws:iam::299138067566:user/technobd-limon-k"
  type          = "STANDARD"
  user_name     = "arn:aws:iam::299138067566:user/technobd-limon-k"

  depends_on = [aws_eks_cluster.devops_cluster]

  tags = {
    Name        = "devops-cluster-user-access"
    Environment = "Development"
    Project     = "DevOps"
  }
}

# Associate access policy for user (Admin policy)
resource "aws_eks_access_policy_association" "user_admin_policy" {
  cluster_name  = aws_eks_cluster.devops_cluster.name
  principal_arn = aws_eks_access_entry.user_access.principal_arn
  policy_arn    = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
  access_scope {
    type = "cluster"
  }

  depends_on = [aws_eks_access_entry.user_access]
}

# ===========================================
# Outputs
# ===========================================

output "user_access_entry_id" {
  description = "ID of the user access entry"
  value       = aws_eks_access_entry.user_access.id
}

output "user_access_entry_arn" {
  description = "ARN of the user access entry"
  value       = aws_eks_access_entry.user_access.principal_arn
}

output "access_entries_summary" {
  description = "Summary of access entries"
  value = {
    user_access = aws_eks_access_entry.user_access.principal_arn
    note        = "Node role and service role access entries are automatically managed by EKS"
  }
}
