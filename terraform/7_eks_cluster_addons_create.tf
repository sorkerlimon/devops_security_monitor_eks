# ===========================================
# EKS Add-ons Configuration
# ===========================================

# CoreDNS Add-on - Service discovery
resource "aws_eks_addon" "coredns" {
  cluster_name  = aws_eks_cluster.devops_cluster.name
  addon_name    = "coredns"
  addon_version = "v1.12.1-eksbuild.2"

  depends_on = [aws_eks_cluster.devops_cluster]

  tags = {
    Name        = "devops-cluster-coredns"
    Environment = "Development"
    Project     = "DevOps"
  }
}

# Amazon EKS Pod Identity Agent Add-on - IAM permissions for pods
resource "aws_eks_addon" "eks_pod_identity_agent" {
  cluster_name  = aws_eks_cluster.devops_cluster.name
  addon_name    = "eks-pod-identity-agent"
  addon_version = "v1.3.8-eksbuild.2"

  depends_on = [aws_eks_cluster.devops_cluster]

  tags = {
    Name        = "devops-cluster-pod-identity-agent"
    Environment = "Development"
    Project     = "DevOps"
  }
}

# External DNS Add-on - Control DNS records
resource "aws_eks_addon" "external_dns" {
  cluster_name  = aws_eks_cluster.devops_cluster.name
  addon_name    = "external-dns"
  addon_version = "v0.19.0-eksbuild.2"

  depends_on = [aws_eks_cluster.devops_cluster]

  tags = {
    Name        = "devops-cluster-external-dns"
    Environment = "Development"
    Project     = "DevOps"
  }
}

# Metrics Server Add-on - Resource usage data for autoscaling
resource "aws_eks_addon" "metrics_server" {
  cluster_name  = aws_eks_cluster.devops_cluster.name
  addon_name    = "metrics-server"
  addon_version = "v0.8.0-eksbuild.2"

  depends_on = [aws_eks_cluster.devops_cluster]

  tags = {
    Name        = "devops-cluster-metrics-server"
    Environment = "Development"
    Project     = "DevOps"
  }
}

# Amazon VPC CNI Add-on - Pod networking
resource "aws_eks_addon" "vpc_cni" {
  cluster_name  = aws_eks_cluster.devops_cluster.name
  addon_name    = "vpc-cni"
  addon_version = "v1.19.5-eksbuild.1"

  depends_on = [aws_eks_cluster.devops_cluster]

  tags = {
    Name        = "devops-cluster-vpc-cni"
    Environment = "Development"
    Project     = "DevOps"
  }
}

# kube-proxy Add-on - Service networking
resource "aws_eks_addon" "kube_proxy" {
  cluster_name  = aws_eks_cluster.devops_cluster.name
  addon_name    = "kube-proxy"
  addon_version = "v1.33.0-eksbuild.2"

  depends_on = [aws_eks_cluster.devops_cluster]

  tags = {
    Name        = "devops-cluster-kube-proxy"
    Environment = "Development"
    Project     = "DevOps"
  }
}

# ===========================================
# Outputs
# ===========================================

output "addons_summary" {
  description = "Summary of all EKS add-ons"
  value = {
    coredns                = aws_eks_addon.coredns.addon_version
    pod_identity_agent     = aws_eks_addon.eks_pod_identity_agent.addon_version
    external_dns           = aws_eks_addon.external_dns.addon_version
    metrics_server         = aws_eks_addon.metrics_server.addon_version
    vpc_cni                = aws_eks_addon.vpc_cni.addon_version
    kube_proxy             = aws_eks_addon.kube_proxy.addon_version
  }
}

output "addons_arns" {
  description = "ARNs of all EKS add-ons"
  value = {
    coredns                = aws_eks_addon.coredns.arn
    pod_identity_agent     = aws_eks_addon.eks_pod_identity_agent.arn
    external_dns           = aws_eks_addon.external_dns.arn
    metrics_server         = aws_eks_addon.metrics_server.arn
    vpc_cni                = aws_eks_addon.vpc_cni.arn
    kube_proxy             = aws_eks_addon.kube_proxy.arn
  }
}
