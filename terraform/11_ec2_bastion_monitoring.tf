# ===========================================
# EC2 Bastion Host for Monitoring
# ===========================================

# Security Group for Bastion Host
resource "aws_security_group" "devops_ec2_sg" {
  name        = "devops_ec2_sg"
  description = "Security group for DevOps EC2 bastion host"
  vpc_id      = aws_vpc.project_devops_vpc.id

  # SSH access
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP access
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS access
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # All outbound traffic
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "devops_ec2_sg"
    Environment = "Development"
    Project     = "DevOps"
    Purpose     = "Bastion Host"
  }
}

# EC2 Instance - Bastion Host
resource "aws_instance" "bastion_monitoring" {
  ami                    = "ami-0a116fa7c861dd5f9"
  instance_type          = "t2.small"
  key_name               = "europe_limon"
  vpc_security_group_ids = [aws_security_group.devops_ec2_sg.id]
  subnet_id              = aws_subnet.public_subnet_1.id

  # Enable public IP
  associate_public_ip_address = true

  # Root volume configuration
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 20
    delete_on_termination = true
    encrypted             = true

    tags = {
      Name        = "devops-bastion-root-volume"
      Environment = "Development"
      Project     = "DevOps"
    }
  }

  # User data script for initial setup
  user_data_base64 = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker
    usermod -a -G docker ec2-user
    
    # Install kubectl
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    mv kubectl /usr/local/bin/
    
    # Install AWS CLI v2
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    ./aws/install
    
    # Install eksctl
    curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
    mv /tmp/eksctl /usr/local/bin
    
    # Install Helm
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
  EOF
  )

  tags = {
    Name        = "devops-bastion-monitoring"
    Environment = "Development"
    Project     = "DevOps"
    Purpose     = "Bastion Host for EKS Monitoring"
    Type        = "Bastion"
  }

  depends_on = [aws_security_group.devops_ec2_sg]
}

# Elastic IP for Bastion Host
resource "aws_eip" "bastion_eip" {
  instance = aws_instance.bastion_monitoring.id
  domain   = "vpc"

  tags = {
    Name        = "devops-bastion-eip"
    Environment = "Development"
    Project     = "DevOps"
    Purpose     = "Bastion Host Static IP"
  }

  depends_on = [aws_instance.bastion_monitoring]
}

# ===========================================
# EKS Security Group Rule for Bastion Access
# ===========================================

# Allow bastion host to access EKS cluster API server
resource "aws_security_group_rule" "eks_allow_bastion_https" {
  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.devops_ec2_sg.id
  security_group_id        = aws_security_group.eks_cluster_sg.id
  description              = "Allow bastion host to access EKS API server"

  depends_on = [
    aws_security_group.devops_ec2_sg,
    aws_security_group.eks_cluster_sg
  ]
}

# ===========================================
# Outputs
# ===========================================

output "bastion_public_ip" {
  description = "Public IP address of the bastion host"
  value       = aws_eip.bastion_eip.public_ip
}

output "bastion_public_dns" {
  description = "Public DNS name of the bastion host"
  value       = aws_instance.bastion_monitoring.public_dns
}

output "bastion_instance_id" {
  description = "Instance ID of the bastion host"
  value       = aws_instance.bastion_monitoring.id
}

output "bastion_security_group_id" {
  description = "Security group ID for the bastion host"
  value       = aws_security_group.devops_ec2_sg.id
}

output "ssh_connection_command" {
  description = "SSH command to connect to bastion host"
  value       = "ssh -i europe_limon.pem ec2-user@${aws_eip.bastion_eip.public_ip}"
}

output "bastion_setup_summary" {
  description = "Bastion host setup summary"
  value = {
    instance_type    = aws_instance.bastion_monitoring.instance_type
    ami_id          = aws_instance.bastion_monitoring.ami
    key_name        = aws_instance.bastion_monitoring.key_name
    security_group  = aws_security_group.devops_ec2_sg.name
    public_ip       = aws_eip.bastion_eip.public_ip
    installed_tools = ["Docker", "kubectl", "AWS CLI v2", "eksctl", "Helm"]
  }
}

output "eks_security_group_rule_id" {
  description = "ID of the EKS security group rule for bastion access"
  value       = aws_security_group_rule.eks_allow_bastion_https.id
}