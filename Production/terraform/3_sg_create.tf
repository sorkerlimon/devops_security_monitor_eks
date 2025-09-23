# ===========================================
# EKS Cluster Security Group Configuration
# ===========================================

# Security Group for EKS Cluster (matching the image configuration)
resource "aws_security_group" "eks_cluster_sg" {
  name        = "eks-cluster-sg"
  description = "EKS created security group applied to ENI that is attached to EKS Control Plane master nodes, as well as any managed workloads."
  vpc_id      = aws_vpc.project_devops_vpc.id

  # Inbound Rules - Only one rule allowing all traffic from self (matching the image)
  ingress {
    description = "Allow all traffic from self"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
  }

  # Outbound Rules - Two rules (matching the image)
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic to self"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
  }

  tags = {
    Name        = "eks-cluster-sg"
    Environment = "Development"
    Project     = "DevOps"
    Description = "EKS Cluster Security Group"
  }
}

# Security Group for EKS Node Group
resource "aws_security_group" "eks_node_sg" {
  name        = "eks-node-sg"
  description = "Security group for EKS worker nodes"
  vpc_id      = aws_vpc.project_devops_vpc.id

  # Allow inbound traffic from EKS cluster
  ingress {
    description     = "Allow traffic from EKS cluster"
    from_port       = 0
    to_port         = 65535
    protocol        = "tcp"
    security_groups = [aws_security_group.eks_cluster_sg.id]
  }

  # Allow inbound traffic from nodes to nodes
  ingress {
    description = "Allow all traffic from nodes"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
  }

  # Allow inbound HTTPS traffic
  ingress {
    description = "Allow HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow inbound HTTP traffic
  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow inbound SSH traffic (for debugging)
  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound Rules
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "eks-node-sg"
    Environment = "Development"
    Project     = "DevOps"
    Description = "EKS Node Group Security Group"
  }
}

# ===========================================
# Outputs
# ===========================================

output "eks_cluster_security_group_id" {
  description = "ID of the EKS cluster security group"
  value       = aws_security_group.eks_cluster_sg.id
}

output "eks_node_security_group_id" {
  description = "ID of the EKS node security group"
  value       = aws_security_group.eks_node_sg.id
}
