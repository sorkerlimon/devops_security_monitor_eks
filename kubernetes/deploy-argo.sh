#!/bin/bash

echo "🚀 Deploying ArgoCD for Security Monitor..."

# Step 1: Create namespace
echo "Creating ArgoCD namespace..."
kubectl apply -f argocd-namespace.yaml

# Step 2: Install ArgoCD
echo "Installing ArgoCD..."
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Step 3: Wait for ArgoCD to be ready
echo "Waiting for ArgoCD to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Step 4: Create Security Monitor application
echo "Creating Security Monitor application..."
kubectl apply -f argocd-application.yaml

# Step 5: Get admin password
echo "Getting admin password..."
ADMIN_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

echo ""
echo "✅ ArgoCD deployed successfully!"
echo ""
echo "📋 Access Information:"
echo "======================"
echo "ArgoCD UI: https://localhost:8080"
echo "Username: admin"
echo "Password: $ADMIN_PASSWORD"
echo ""
echo "🔧 To access ArgoCD:"
echo "kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo ""
echo "Then open: https://localhost:8080"
