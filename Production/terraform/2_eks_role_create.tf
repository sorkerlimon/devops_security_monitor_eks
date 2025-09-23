# ===========================================
# EKS IAM Roles Configuration
# ===========================================

# ===========================================
# 1. AmazonEKSAutoClusterRole
# ===========================================

resource "aws_iam_role" "AmazonEKSAutoClusterRole" {
  name = "AmazonEKSAutoClusterRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      },
      {
        Action = "sts:TagSession"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "AmazonEKSAutoClusterRole"
  }
}

# Attach policies to AmazonEKSAutoClusterRole
resource "aws_iam_role_policy_attachment" "AmazonEKSAutoClusterRole_CNI_Policy" {
  role       = aws_iam_role.AmazonEKSAutoClusterRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "AmazonEKSAutoClusterRole_BlockStoragePolicy" {
  role       = aws_iam_role.AmazonEKSAutoClusterRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSBlockStoragePolicy"
}

resource "aws_iam_role_policy_attachment" "AmazonEKSAutoClusterRole_ClusterPolicy" {
  role       = aws_iam_role.AmazonEKSAutoClusterRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_iam_role_policy_attachment" "AmazonEKSAutoClusterRole_ComputePolicy" {
  role       = aws_iam_role.AmazonEKSAutoClusterRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSComputePolicy"
}

resource "aws_iam_role_policy_attachment" "AmazonEKSAutoClusterRole_LoadBalancingPolicy" {
  role       = aws_iam_role.AmazonEKSAutoClusterRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSLoadBalancingPolicy"
}

resource "aws_iam_role_policy_attachment" "AmazonEKSAutoClusterRole_NetworkingPolicy" {
  role       = aws_iam_role.AmazonEKSAutoClusterRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSNetworkingPolicy"
}

# ===========================================
# 2. AmazonEKSAutoNodeRole
# ===========================================

resource "aws_iam_role" "AmazonEKSAutoNodeRole" {
  name = "AmazonEKSAutoNodeRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "AmazonEKSAutoNodeRole"
  }
}

# Attach policies to AmazonEKSAutoNodeRole
resource "aws_iam_role_policy_attachment" "AmazonEKSAutoNodeRole_ECRPolicy" {
  role       = aws_iam_role.AmazonEKSAutoNodeRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPullOnly"
}

resource "aws_iam_role_policy_attachment" "AmazonEKSAutoNodeRole_ECRReadOnlyPolicy" {
  role       = aws_iam_role.AmazonEKSAutoNodeRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_role_policy_attachment" "AmazonEKSAutoNodeRole_CNI_Policy" {
  role       = aws_iam_role.AmazonEKSAutoNodeRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "AmazonEKSAutoNodeRole_WorkerNodePolicy" {
  role       = aws_iam_role.AmazonEKSAutoNodeRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

# ===========================================
# 3. AWSServiceRoleForAmazonEKS
# ===========================================

resource "aws_iam_role" "AWSServiceRoleForAmazonEKS" {
  name = "AmazonEKSClusterServiceRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "AmazonEKSClusterServiceRole"
  }
}

# Attach policy to AWSServiceRoleForAmazonEKS
resource "aws_iam_role_policy_attachment" "AWSServiceRoleForAmazonEKS_ServiceRolePolicy" {
  role       = aws_iam_role.AWSServiceRoleForAmazonEKS.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}
