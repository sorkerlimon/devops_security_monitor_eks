#!/bin/bash

# Production EKS Deployment Script
# Deploys Security Monitor to AWS EKS with domain configuration

set -e

echo "🚀 Starting Production EKS Deployment..."
echo "Domain: security-monitor.dreamhrai.com"
echo "Cluster: devops_cluster"
echo "=========================================="

# Connect to EKS cluster
echo "🔗 Connecting to EKS cluster..."
aws eks update-kubeconfig --region eu-central-1 --name devops_cluster
echo "   ✅ Connected to devops_cluster"

# Step 1: Create namespace
echo "📦 Step 1: Creating namespace..."
kubectl apply -f namespace.yaml
echo "   ✅ Namespace created"
kubectl config set-context --current --namespace=security-monitor

# Step 2: Apply production ConfigMap
echo "⚙️  Step 2: Applying production ConfigMap..."
kubectl apply -f production_configmap.yaml
echo "   ✅ Production ConfigMap applied"

# Step 3: Apply Secrets
echo "🔐 Step 3: Applying secrets..."
kubectl apply -f secret.yaml
echo "   ✅ Secrets applied"

# Step 4: Create ECR Secret
echo "🐳 Step 4: Creating ECR secret..."
kubectl create secret docker-registry ecr-secret \
  --docker-server=299138067566.dkr.ecr.eu-central-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region eu-central-1) \
  --namespace=security-monitor \
  --dry-run=client -o yaml | kubectl apply -f -
echo "   ✅ ECR secret created/updated"

# Step 5: Deploy Backend
echo "🔧 Step 5: Deploying backend..."
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
echo "   ✅ Backend deployed"

# Step 6: Wait for backend to be ready
echo "⏳ Step 6: Waiting for backend to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/security-monitor-backend
echo "   ✅ Backend is ready"

# Step 7: Create Admin User
echo "👤 Step 7: Creating admin user..."
kubectl exec -it deployment/security-monitor-backend -- python create_admin.py
echo "   ✅ Admin user created"

# Step 8: Deploy Frontend
echo "🎨 Step 8: Deploying frontend..."
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
echo "   ✅ Frontend deployed"

# Step 9: Wait for frontend to be ready
echo "⏳ Step 9: Waiting for frontend to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/security-monitor-frontend
echo "   ✅ Frontend is ready"

# Step 10: Install NGINX Ingress Controller (if not exists)
echo "🌐 Step 10: Checking NGINX Ingress Controller..."
if ! kubectl get deployment -n ingress-nginx nginx-ingress-controller >/dev/null 2>&1; then
    echo "   Installing NGINX Ingress Controller..."
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/aws/deploy.yaml
    kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=300s
    echo "   ✅ NGINX Ingress Controller installed"
else
    echo "   ✅ NGINX Ingress Controller already exists"
fi

# Step 11: Install cert-manager (if not exists)
echo "🔒 Step 11: Checking cert-manager..."
if ! kubectl get deployment -n cert-manager cert-manager >/dev/null 2>&1; then
    echo "   Installing cert-manager..."
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
    kubectl wait --namespace cert-manager --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=300s
    echo "   ✅ cert-manager installed"
else
    echo "   ✅ cert-manager already exists"
fi

# Step 12: Create SSL Certificate Issuer
echo "🔐 Step 12: Creating SSL certificate issuer..."
kubectl apply -f production_cert_issuer.yaml
echo "   ✅ SSL certificate issuer created"

# Step 13: Deploy Production Ingress
echo "🌐 Step 13: Deploying production ingress..."
kubectl apply -f production_ingress.yaml
echo "   ✅ Production ingress deployed"

# Step 14: Get LoadBalancer Information
echo "📋 Step 14: Getting LoadBalancer information..."
echo "   Getting LoadBalancer details..."
kubectl get svc -n ingress-nginx

echo ""
echo "🎉 Production Deployment Complete!"
echo "=========================================="
echo "Next Steps:"
echo "1. Get the LoadBalancer IP from above"
echo "2. Point your domain security-monitor.dreamhrai.com to the LoadBalancer IP"
echo "3. Wait for DNS propagation (5-30 minutes)"
echo "4. Access your application at: https://security-monitor.dreamhrai.com"
echo ""
echo "To check status:"
echo "kubectl get all -n security-monitor"
echo "kubectl get ingress -n security-monitor"
echo "kubectl get certificate -n security-monitor"
