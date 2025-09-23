# Security Monitor - Deployment Guide

## 🚀 Deployment Overview

This guide provides comprehensive instructions for deploying the Security Monitor application to AWS EKS using Infrastructure as Code and DevOps best practices.

## 📋 Prerequisites

### Required Tools
- **AWS CLI** v2.0+
- **kubectl** v1.28+
- **Terraform** v1.5+
- **Docker** v20.0+
- **Git** v2.30+

### AWS Account Setup
- AWS Account with appropriate permissions
- IAM user with programmatic access
- AWS CLI configured with credentials

### Domain Setup
- Domain name registered
- DNS management access
- SSL certificate (handled automatically)

## 🏗️ Infrastructure Deployment

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/security-monitor.git
cd security-monitor
```

### Step 2: Configure AWS Credentials
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., eu-central-1)
# Enter your default output format (json)
```

### Step 3: Deploy Infrastructure with Terraform
```bash
cd terraform

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the infrastructure
terraform apply

# Note the outputs (EKS cluster name, RDS endpoint, etc.)
```

### Step 4: Configure kubectl
```bash
# Update kubeconfig
aws eks update-kubeconfig --region eu-central-1 --name devops_cluster

# Verify connection
kubectl get nodes
```

## 🐳 Container Image Deployment

### Step 1: Build and Push Images
```bash
# Login to ECR
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 299138067566.dkr.ecr.eu-central-1.amazonaws.com

# Build and push backend
cd ../backend
docker build -t 299138067566.dkr.ecr.eu-central-1.amazonaws.com/devops-backend:latest .
docker push 299138067566.dkr.ecr.eu-central-1.amazonaws.com/devops-backend:latest

# Build and push frontend
cd ../frontend
docker build -t 299138067566.dkr.ecr.eu-central-1.amazonaws.com/devops-frontend:latest .
docker push 299138067566.dkr.ecr.eu-central-1.amazonaws.com/devops-frontend:latest
```

## ☸️ Kubernetes Deployment

### Step 1: Deploy Core Components
```bash
cd ../kubernetes

# Create namespace
kubectl apply -f namespace.yaml

# Apply ConfigMap
kubectl apply -f production_configmap.yaml

# Apply secrets
kubectl apply -f secret.yaml

# Create ECR secret
kubectl create secret docker-registry ecr-secret \
  --docker-server=299138067566.dkr.ecr.eu-central-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region eu-central-1) \
  --namespace=security-monitor
```

### Step 2: Deploy Backend
```bash
# Deploy backend
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml

# Wait for backend to be ready
kubectl wait --for=condition=available --timeout=300s deployment/security-monitor-backend -n security-monitor

# Create admin user
kubectl exec -it deployment/security-monitor-backend -n security-monitor -- python create_admin.py
```

### Step 3: Deploy Frontend
```bash
# Deploy frontend
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml

# Wait for frontend to be ready
kubectl wait --for=condition=available --timeout=300s deployment/security-monitor-frontend -n security-monitor
```

### Step 4: Deploy Ingress and SSL
```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/aws/deploy.yaml

# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Wait for controllers to be ready
kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=300s
kubectl wait --namespace cert-manager --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=300s

# Deploy certificate issuer
kubectl apply -f production_cert_issuer.yaml

# Deploy ingress
kubectl apply -f production_ingress.yaml
```

## 🌐 DNS Configuration

### Step 1: Get LoadBalancer IP
```bash
kubectl get svc -n ingress-nginx
# Note the EXTERNAL-IP of the ingress-nginx-controller
```

### Step 2: Configure DNS
1. Go to your domain registrar (GoDaddy, Namecheap, etc.)
2. Create an A record:
   - **Name**: `security-monitor` (or `@` for root domain)
   - **Type**: `A`
   - **Value**: LoadBalancer IP from step 1
   - **TTL**: `300`

### Step 3: Wait for DNS Propagation
- DNS propagation typically takes 5-30 minutes
- You can check with: `nslookup security-monitor.yourdomain.com`

## ✅ Verification

### Step 1: Check Application Status
```bash
# Check all resources
kubectl get all -n security-monitor

# Check ingress
kubectl get ingress -n security-monitor

# Check SSL certificate
kubectl get certificate -n security-monitor
```

### Step 2: Test Application
1. Open browser to `https://security-monitor.yourdomain.com`
2. Login with:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Verify all features are working

### Step 3: Check Logs
```bash
# Backend logs
kubectl logs deployment/security-monitor-backend -n security-monitor

# Frontend logs
kubectl logs deployment/security-monitor-frontend -n security-monitor

# Ingress logs
kubectl logs deployment/ingress-nginx-controller -n ingress-nginx
```

## 🔄 CI/CD Pipeline Setup

### Step 1: GitHub Actions Setup
```yaml
# .github/workflows/deploy.yml
name: Deploy to EKS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: eu-central-1
    
    - name: Build and push images
      run: |
        # Build and push backend
        docker build -t $ECR_REGISTRY/devops-backend:$GITHUB_SHA ./backend
        docker push $ECR_REGISTRY/devops-backend:$GITHUB_SHA
        
        # Build and push frontend
        docker build -t $ECR_REGISTRY/devops-frontend:$GITHUB_SHA ./frontend
        docker push $ECR_REGISTRY/devops-frontend:$GITHUB_SHA
    
    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --region eu-central-1 --name devops_cluster
        kubectl set image deployment/security-monitor-backend security-monitor-backend=$ECR_REGISTRY/devops-backend:$GITHUB_SHA -n security-monitor
        kubectl set image deployment/security-monitor-frontend security-monitor-frontend=$ECR_REGISTRY/devops-frontend:$GITHUB_SHA -n security-monitor
```

### Step 2: Configure Secrets
1. Go to GitHub repository settings
2. Navigate to Secrets and Variables > Actions
3. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `ECR_REGISTRY`

## 📊 Monitoring Setup

### Step 1: Install Prometheus and Grafana
```bash
# Add Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# Install Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set persistence.enabled=true \
  --set adminPassword=admin123
```

### Step 2: Configure CloudWatch Logs
```bash
# Install CloudWatch agent
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cloudwatch-namespace.yaml

# Apply CloudWatch configuration
kubectl apply -f monitoring/cloudwatch-config.yaml
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Pods Not Starting
```bash
# Check pod status
kubectl get pods -n security-monitor

# Check pod logs
kubectl logs <pod-name> -n security-monitor

# Check events
kubectl get events -n security-monitor
```

#### 2. Database Connection Issues
```bash
# Test database connection
kubectl exec -it deployment/security-monitor-backend -n security-monitor -- python -c "
import pymysql
conn = pymysql.connect(host='your-rds-endpoint', port=3306, user='username', password='password', database='security_monitor')
print('Database connection: SUCCESS')
conn.close()
"
```

#### 3. SSL Certificate Issues
```bash
# Check certificate status
kubectl describe certificate security-monitor-tls -n security-monitor

# Check cert-manager logs
kubectl logs deployment/cert-manager -n cert-manager
```

#### 4. Ingress Issues
```bash
# Check ingress status
kubectl describe ingress security-monitor-ingress -n security-monitor

# Check NGINX logs
kubectl logs deployment/ingress-nginx-controller -n ingress-nginx
```

### Debug Commands
```bash
# Get all resources
kubectl get all -n security-monitor

# Describe resources
kubectl describe deployment security-monitor-backend -n security-monitor

# Check logs
kubectl logs -f deployment/security-monitor-backend -n security-monitor

# Port forward for testing
kubectl port-forward svc/security-monitor-backend 8000:8000 -n security-monitor
```

## 🧹 Cleanup

### Remove Application
```bash
# Delete Kubernetes resources
kubectl delete -f production_ingress.yaml
kubectl delete -f production_cert_issuer.yaml
kubectl delete -f frontend-deployment.yaml
kubectl delete -f frontend-service.yaml
kubectl delete -f backend-deployment.yaml
kubectl delete -f backend-service.yaml
kubectl delete -f secret.yaml
kubectl delete -f production_configmap.yaml
kubectl delete -f namespace.yaml
```

### Remove Infrastructure
```bash
cd terraform
terraform destroy
```

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [cert-manager Documentation](https://cert-manager.io/docs/)

---

**For support, please contact the DevOps team or create an issue in the repository.**
