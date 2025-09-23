# Security Monitor - DevOps Infrastructure Project

## 🚀 Project Overview

A comprehensive network security monitoring application deployed on AWS EKS with full DevOps practices including Infrastructure as Code, CI/CD, monitoring, and security best practices.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud Infrastructure                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Route 53      │  │   CloudFront    │  │   ACM (SSL)     │  │
│  │   DNS           │  │   CDN           │  │   Certificates  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    EKS Cluster                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Frontend  │  │   Backend   │  │   Ingress   │        │ │
│  │  │   (React)   │  │   (FastAPI) │  │  (NGINX)    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   ConfigMap │  │   Secrets   │  │   Services  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   RDS MySQL     │  │   ECR Registry  │  │   CloudWatch    │  │
│  │   Database      │  │   Images        │  │   Logs          │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Core Technologies
- **Kubernetes**: Amazon EKS (Elastic Kubernetes Service)
- **Container Orchestration**: Docker + Kubernetes
- **Infrastructure as Code**: Terraform
- **CI/CD**: GitHub Actions
- **Cloud Provider**: AWS
- **Database**: MySQL (RDS)
- **Container Registry**: Amazon ECR

### Application Stack
- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: MySQL with SQLAlchemy ORM
- **Reverse Proxy**: NGINX Ingress Controller
- **SSL/TLS**: Let's Encrypt (cert-manager)

### DevOps Tools
- **Monitoring**: CloudWatch, Kubernetes metrics
- **Security**: AWS IAM, RBAC, secrets management
- **Scripting**: Python, Bash, PowerShell
- **Version Control**: Git

## 📁 Project Structure

```
security-monitor/
├── terraform/                    # Infrastructure as Code
│   ├── 1_vpc_create.tf          # VPC and networking
│   ├── 2_eks_role_create.tf     # EKS IAM roles
│   ├── 3_sg_create.tf           # Security groups
│   ├── 4_eks_cluster_create.tf  # EKS cluster
│   ├── 5_eks_cluster_access_entries_create.tf
│   ├── 6_eks_node_group_create.tf
│   ├── 7_eks_cluster_addons_create.tf
│   ├── 8_eks_ecr_frontend.tf    # ECR repositories
│   ├── 9_eks_ecr_backend.tf
│   ├── 10_ecr_permission_eks.tf
│   ├── 11_ec2_bastion_monitoring.tf
│   ├── variables.tf
│   └── terraform.tfvars
├── kubernetes/                   # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── ingress.yaml
│   ├── production_*.yaml         # Production configurations
│   ├── deploy-simple.sh         # Deployment scripts
│   └── production_deploy.sh
├── ci-cd/                       # CI/CD pipelines
│   └── .github/workflows/
├── monitoring/                   # Monitoring configurations
│   └── prometheus-grafana/
├── backend/                     # Backend application
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   ├── models.py
│   ├── routers/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                    # Frontend application
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
└── docs/                        # Documentation
    ├── architecture.md
    ├── security.md
    └── deployment.md
```

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured
- kubectl installed
- Docker installed
- Terraform installed

### 1. Infrastructure Setup
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 2. Deploy Application
```bash
cd kubernetes
./production_deploy.sh
```

### 3. Access Application
- **URL**: https://security-monitor.dreamhrai.com
- **Username**: admin
- **Password**: admin123

## 🔒 Security Features

### Infrastructure Security
- **VPC Isolation**: Private subnets for EKS nodes
- **Security Groups**: Restrictive firewall rules
- **IAM Roles**: Least privilege access
- **Encryption**: Data encrypted in transit and at rest
- **RBAC**: Kubernetes role-based access control

### Application Security
- **JWT Authentication**: Secure token-based auth
- **CORS Configuration**: Proper cross-origin policies
- **SSL/TLS**: Automatic certificate management
- **Secrets Management**: Kubernetes secrets for sensitive data
- **Input Validation**: API request validation

### DevSecOps Practices
- **Container Scanning**: Docker image vulnerability scanning
- **Code Quality**: Linting and security checks in CI/CD
- **Dependency Management**: Regular security updates
- **Access Control**: Multi-layer authentication

## 📊 Monitoring & Observability

### Application Monitoring
- **Health Checks**: Kubernetes liveness and readiness probes
- **Logging**: Centralized logging with CloudWatch
- **Metrics**: Application and infrastructure metrics
- **Alerting**: Automated alerting for critical issues

### Infrastructure Monitoring
- **Cluster Health**: EKS cluster monitoring
- **Resource Usage**: CPU, memory, and storage metrics
- **Network Monitoring**: Traffic and connectivity monitoring
- **Cost Monitoring**: AWS cost optimization

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
1. **Code Push**: Trigger on push to main branch
2. **Security Scan**: Container and dependency scanning
3. **Build**: Docker image building
4. **Test**: Automated testing
5. **Push**: Push to ECR registry
6. **Deploy**: Deploy to EKS cluster
7. **Verify**: Health checks and smoke tests

### Deployment Strategy
- **Blue-Green Deployment**: Zero-downtime deployments
- **Rolling Updates**: Gradual pod replacement
- **Rollback Capability**: Quick rollback on issues
- **Environment Promotion**: Dev → Staging → Production

## 🌍 Multi-Environment Support

### Environments
- **Development**: Local development with Docker Compose
- **Staging**: EKS cluster with staging configuration
- **Production**: EKS cluster with production configuration

### Environment-Specific Configurations
- **ConfigMaps**: Environment-specific settings
- **Secrets**: Secure credential management
- **Resource Limits**: Environment-appropriate resource allocation
- **Monitoring**: Environment-specific alerting

## 📈 Scalability Features

### Horizontal Scaling
- **Auto Scaling**: Kubernetes HPA (Horizontal Pod Autoscaler)
- **Load Balancing**: NGINX ingress load balancing
- **Database Scaling**: Connection pooling and optimization

### Vertical Scaling
- **Resource Requests/Limits**: Proper resource allocation
- **Node Scaling**: EKS node group auto-scaling
- **Storage Scaling**: Dynamic volume provisioning

## 🛡️ Disaster Recovery

### Backup Strategy
- **Database Backups**: Automated RDS snapshots
- **Configuration Backup**: Git-based configuration management
- **Image Registry**: ECR image versioning

### Recovery Procedures
- **Infrastructure Recovery**: Terraform state management
- **Application Recovery**: Kubernetes deployment restoration
- **Data Recovery**: Database point-in-time recovery

## 📋 Project Answers

### 1. Why did you choose this project?
I chose to build a Security Monitor application because it demonstrates real-world DevOps challenges including:
- **Complex Application Architecture**: Multi-tier application with frontend, backend, and database
- **Security Focus**: Security monitoring application requires robust security practices
- **Scalability Requirements**: Monitoring applications need to handle varying loads
- **Production Readiness**: Real-world deployment with proper monitoring and alerting

### 2. How does your infrastructure ensure security and scalability?
**Security:**
- VPC isolation with private subnets
- IAM roles with least privilege
- Kubernetes RBAC
- SSL/TLS encryption
- Secrets management
- Container security scanning

**Scalability:**
- Kubernetes auto-scaling (HPA)
- Load balancing with NGINX ingress
- Database connection pooling
- EKS node group auto-scaling
- Resource optimization

### 3. Describe your CI/CD and monitoring strategy.
**CI/CD Strategy:**
- GitHub Actions for automated pipelines
- Multi-stage Docker builds
- Automated testing and security scanning
- Blue-green deployments
- Automated rollback capabilities

**Monitoring Strategy:**
- CloudWatch for centralized logging
- Kubernetes metrics collection
- Health checks and alerting
- Performance monitoring
- Cost optimization tracking

### 4. What was your biggest challenge?
The biggest challenge was **database connectivity in the Kubernetes environment**. The application worked locally but had intermittent connection issues in EKS due to:
- Connection pooling configuration
- Network timeouts
- Database connection limits

**Solution:** Implemented proper connection pooling with `pool_pre_ping=True` and connection recycling to ensure stable database connections in the containerized environment.

## 🎯 Demo Credentials

- **Application URL**: https://security-monitor.dreamhrai.com
- **Username**: admin
- **Password**: admin123

## 📞 Contact

- **GitHub**: [Your GitHub Profile]
- **Email**: [Your Email]
- **LinkedIn**: [Your LinkedIn Profile]

---

**Built with ❤️ using modern DevOps practices and cloud-native technologies.**
