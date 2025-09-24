#!/bin/bash

# Simple Kubernetes Deployment Script
# Deploys Security Monitor with raw Kubernetes manifests

# kind create cluster --name cka-cluster1
# kind get clusters
# kubectl get nodes
# kind delete cluster --name cka-cluster1
# kind create cluster --name cka-cluster2 --config cluster_create.yml
# kubectl cluster-info --context kind-cka-cluster1
# kubectl config get-contexts
# kubectl config use-context kind-cka-cluster1

# # Delete contexts
# kubectl config delete-context kind-cka-cluster1

# # Delete clusters
# kubectl config delete-cluster kind-cka-cluster1

# # Delete users
# kubectl config unset users.kind-cka-cluster1



set -e

echo "🚀 Deploying Security Monitor to Kubernetes..."

# Note: Using ECR images instead of building locally
echo "🐳 Using ECR images..."
echo "   Backend: 299138067566.dkr.ecr.eu-central-1.amazonaws.com/devops-backend:latest"
echo "   Frontend: 299138067566.dkr.ecr.eu-central-1.amazonaws.com/devops-frontend:latest"

# Step 1: Create namespace
echo "📦 Step 1: Creating namespace..."
kubectl apply -f namespace.yaml
echo "   ✅ Check: kubectl get namespace security-monitor"
kubectl config set-context --current --namespace=security-monitor
kubectl get namespaces | grep security-monitor

# Step 2: Apply ConfigMap
echo "🔧 Step 2: Applying ConfigMap..."
kubectl apply -f configmap.yaml
echo "   ✅ Check: kubectl get configmap -n security-monitor"
kubectl get configmap -n security-monitor

# Step 3: Apply Secrets
echo "🔐 Step 3: Applying Secrets..."
kubectl apply -f secret.yaml
echo "   ✅ Check: kubectl get secrets -n security-monitor"
kubectl get secrets -n security-monitor

# Step 4: Create ECR Secret (Working method)
echo "🐳 Step 4: Creating ECR secret..."
kubectl create secret docker-registry ecr-secret \
  --docker-server=299138067566.dkr.ecr.eu-central-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region eu-central-1) \
  --namespace=security-monitor
echo "   ✅ ECR secret created successfully"

# Step 5: Deploy Backend
echo "🚀 Step 5: Deploying Backend..."
kubectl apply -f backend-deployment.yaml
echo "   ✅ Check: kubectl get pods -n security-monitor"
kubectl get pods -n security-monitor

# Step 6: Deploy Backend Service
echo "🌐 Step 6: Deploying Backend Service..."
kubectl apply -f backend-service.yaml
echo "   ✅ Check: kubectl get svc -n security-monitor"
kubectl get svc -n security-monitor

# Step 7: Create Admin User
echo "👤 Step 7: Creating Admin User..."
kubectl exec -it deployment/security-monitor-backend -n security-monitor -- python create_admin.py
echo "   ✅ Admin user created/verified"

# Step 8: Deploy Frontend
echo "🎨 Step 8: Deploying Frontend..."
kubectl apply -f frontend-deployment.yaml
echo "   ✅ Check: kubectl get pods -n security-monitor"
kubectl get pods -n security-monitor





# Step 4: Create ECR Secret (Working method)
echo "🐳 Step 4: Creating ECR secret..."
kubectl create secret docker-registry ecr-secret \
  --docker-server=299138067566.dkr.ecr.eu-central-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region eu-central-1) \
  --namespace=security-monitor
echo "   ✅ ECR secret created successfully"


# Step 9: Deploy Frontend Service
echo "🌐 Step 9: Deploying Frontend Service..."
kubectl apply -f frontend-service.yaml
echo "   ✅ Check: kubectl get svc -n security-monitor"
kubectl get svc -n security-monitor

# Step 10: Set up Port Forwarding
echo "🔗 Step 10: Setting up Port Forwarding..."
echo "   Backend: kubectl port-forward svc/security-monitor-backend 8000:8000 -n security-monitor"
echo "   Frontend: kubectl port-forward svc/security-monitor-frontend 3000:3000 -n security-monitor"
echo ""
echo "   🌐 Access URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Backend Docs: http://localhost:8000/docs"
echo ""
echo "   🔐 Login Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "   🗄️ Database: MySQL (192.168.50.89:3306)"
echo ""
echo "✅ Deployment Complete! Run the port-forward commands to access the application."