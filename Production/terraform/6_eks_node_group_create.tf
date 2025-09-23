# ===========================================
# EKS Node Group Configuration
# ===========================================

resource "aws_eks_node_group" "node" {
  cluster_name    = aws_eks_cluster.devops_cluster.name
  node_group_name = "node"
  node_role_arn   = "arn:aws:iam::299138067566:role/AmazonEKSAutoNodeRole"
  subnet_ids      = [
    "subnet-05e101e5fc59ea135",
    "subnet-05f6d920c97137d97"
  ]

  capacity_type  = "ON_DEMAND"
  instance_types = ["t2.small"]
  disk_size      = 20

  scaling_config {
    desired_size = 2
    max_size     = 4
    min_size     = 1
  }

  update_config {
    max_unavailable_percentage = 25
  }

  # Ensure that IAM Role permissions are created before and deleted after EKS Node Group handling.
  depends_on = [
    aws_iam_role_policy_attachment.AmazonEKSAutoNodeRole_WorkerNodePolicy,
    aws_iam_role_policy_attachment.AmazonEKSAutoNodeRole_CNI_Policy,
    aws_iam_role_policy_attachment.AmazonEKSAutoNodeRole_ECRPolicy,
    aws_iam_role_policy_attachment.AmazonEKSAutoNodeRole_ECRReadOnlyPolicy
  ]

  tags = {
    Name        = "devops-cluster-node-group"
    Environment = "Development"
    Project     = "DevOps"
  }
}

# ===========================================
# Outputs
# ===========================================

output "node_group_arn" {
  description = "Amazon Resource Name (ARN) of the EKS Node Group"
  value       = aws_eks_node_group.node.arn
}

output "node_group_status" {
  description = "Status of the EKS Node Group"
  value       = aws_eks_node_group.node.status
}

output "node_group_capacity_type" {
  description = "Type of capacity associated with the EKS Node Group"
  value       = aws_eks_node_group.node.capacity_type
}
