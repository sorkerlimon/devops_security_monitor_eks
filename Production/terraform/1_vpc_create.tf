# ===========================================
# AWS Provider Configuration
# ===========================================

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# ===========================================
# VPC Configuration
# ===========================================

# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# VPC
resource "aws_vpc" "project_devops_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "project-devops-vpc"
  }
}

# ===========================================
# Internet Gateway
# ===========================================

resource "aws_internet_gateway" "project_devops_igw" {
  vpc_id = aws_vpc.project_devops_vpc.id

  tags = {
    Name = "project-devops-igw"
  }
}

# ===========================================
# Public Subnets
# ===========================================

resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.project_devops_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "project-devops-subnet-public1-${data.aws_availability_zones.available.names[0]}"
    Type = "Public"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.project_devops_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = data.aws_availability_zones.available.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name = "project-devops-subnet-public2-${data.aws_availability_zones.available.names[1]}"
    Type = "Public"
  }
}

# ===========================================
# Private Subnets
# ===========================================

resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.project_devops_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "project-devops-subnet-private1-${data.aws_availability_zones.available.names[0]}"
    Type = "Private"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.project_devops_vpc.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "project-devops-subnet-private2-${data.aws_availability_zones.available.names[1]}"
    Type = "Private"
  }
}

# ===========================================
# Elastic IP for NAT Gateway
# ===========================================

resource "aws_eip" "nat_eip" {
  domain = "vpc"
  depends_on = [aws_internet_gateway.project_devops_igw]

  tags = {
    Name = "project-devops-nat-eip"
  }
}

# ===========================================
# NAT Gateway
# ===========================================

resource "aws_nat_gateway" "project_devops_nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet_1.id
  depends_on    = [aws_internet_gateway.project_devops_igw]

  tags = {
    Name = "project-devops-nat-public1-${data.aws_availability_zones.available.names[0]}"
  }
}

# ===========================================
# Route Tables
# ===========================================

# Public Route Table
resource "aws_route_table" "public_rtb" {
  vpc_id = aws_vpc.project_devops_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.project_devops_igw.id
  }

  tags = {
    Name = "project-devops-rtb-public"
  }
}

# Private Route Table 1
resource "aws_route_table" "private_rtb_1" {
  vpc_id = aws_vpc.project_devops_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.project_devops_nat.id
  }

  tags = {
    Name = "project-devops-rtb-private1-${data.aws_availability_zones.available.names[0]}"
  }
}

# Private Route Table 2
resource "aws_route_table" "private_rtb_2" {
  vpc_id = aws_vpc.project_devops_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.project_devops_nat.id
  }

  tags = {
    Name = "project-devops-rtb-private2-${data.aws_availability_zones.available.names[1]}"
  }
}

# ===========================================
# Route Table Associations
# ===========================================

# Associate public subnets with public route table
resource "aws_route_table_association" "public_subnet_1_association" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rtb.id
}

resource "aws_route_table_association" "public_subnet_2_association" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_rtb.id
}

# Associate private subnets with their respective route tables
resource "aws_route_table_association" "private_subnet_1_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rtb_1.id
}

resource "aws_route_table_association" "private_subnet_2_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rtb_2.id
}
