# ===========================================
# EKS Cluster Configuration (Cluster Only)
# ===========================================

# EKS Cluster
resource "aws_eks_cluster" "devops_cluster" {
  name     = "devops_cluster"
  role_arn = "arn:aws:iam::299138067566:role/AmazonEKSAutoClusterRole"
  version  = "1.33"

  vpc_config {
    subnet_ids = [
      "subnet-05e101e5fc59ea135",
      "subnet-05f6d920c97137d97", 
      "subnet-074a6549675c80c2c",
      "subnet-0726834ef8b632510"
    ]
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
    security_group_ids      = [aws_security_group.eks_cluster_sg.id]
  }

  # Set authentication mode to EKS API and ConfigMap
  access_config {
    authentication_mode = "API_AND_CONFIG_MAP"
  }

  # Enable EKS Cluster Logging
  enabled_cluster_log_types = [
    "api",
    "audit", 
    "authenticator",
    "controllerManager",
    "scheduler"
  ]

  depends_on = [
    aws_iam_role_policy_attachment.AmazonEKSAutoClusterRole_ClusterPolicy,
    aws_iam_role_policy_attachment.AmazonEKSAutoClusterRole_CNI_Policy,
    aws_iam_role_policy_attachment.AmazonEKSAutoClusterRole_NetworkingPolicy,
    aws_iam_role_policy_attachment.AmazonEKSAutoClusterRole_LoadBalancingPolicy,
    aws_iam_role_policy_attachment.AmazonEKSAutoClusterRole_BlockStoragePolicy,
    aws_iam_role_policy_attachment.AmazonEKSAutoClusterRole_ComputePolicy
  ]

  tags = {
    Name        = "devops_cluster"
    Environment = "Development"
    Project     = "DevOps"
  }
}

# ===========================================
# Outputs
# ===========================================

output "cluster_id" {
  description = "EKS cluster ID"
  value       = aws_eks_cluster.devops_cluster.id
}

output "cluster_arn" {
  description = "The Amazon Resource Name (ARN) of the cluster"
  value       = aws_eks_cluster.devops_cluster.arn
}

output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = aws_eks_cluster.devops_cluster.endpoint
}

output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = aws_eks_cluster.devops_cluster.vpc_config[0].cluster_security_group_id
}

output "cluster_iam_role_name" {
  description = "IAM role name associated with EKS cluster"
  value       = aws_eks_cluster.devops_cluster.role_arn
}

output "cluster_oidc_issuer_url" {
  description = "The URL on the EKS cluster for the OpenID Connect identity provider"
  value       = aws_eks_cluster.devops_cluster.identity[0].oidc[0].issuer
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the cluster"
  value       = aws_eks_cluster.devops_cluster.certificate_authority[0].data
}

output "cluster_authentication_mode" {
  description = "Authentication mode of the EKS cluster"
  value       = aws_eks_cluster.devops_cluster.access_config[0].authentication_mode
}