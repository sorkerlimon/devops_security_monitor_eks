#!/bin/bash

# Production EKS Cleanup Script
# Removes all Security Monitor resources from EKS

set -e

echo "🧹 Starting Production EKS Cleanup..."
echo "=========================================="

# Step 1: Delete Ingress
echo "🌐 Step 1: Deleting ingress..."
kubectl delete -f production_ingress.yaml --ignore-not-found=true
echo "   ✅ Ingress deleted"

# Step 2: Delete Certificate Issuer
echo "🔐 Step 2: Deleting certificate issuer..."
kubectl delete -f production_cert_issuer.yaml --ignore-not-found=true
echo "   ✅ Certificate issuer deleted"

# Step 3: Delete Frontend
echo "🎨 Step 3: Deleting frontend..."
kubectl delete -f frontend-service.yaml --ignore-not-found=true
kubectl delete -f frontend-deployment.yaml --ignore-not-found=true
echo "   ✅ Frontend deleted"

# Step 4: Delete Backend
echo "🔧 Step 4: Deleting backend..."
kubectl delete -f backend-service.yaml --ignore-not-found=true
kubectl delete -f backend-deployment.yaml --ignore-not-found=true
echo "   ✅ Backend deleted"

# Step 5: Delete Secrets
echo "🔐 Step 5: Deleting secrets..."
kubectl delete -f secret.yaml --ignore-not-found=true
kubectl delete secret ecr-secret -n security-monitor --ignore-not-found=true
echo "   ✅ Secrets deleted"

# Step 6: Delete ConfigMap
echo "⚙️  Step 6: Deleting ConfigMap..."
kubectl delete -f production_configmap.yaml --ignore-not-found=true
echo "   ✅ ConfigMap deleted"

# Step 7: Delete Namespace
echo "📦 Step 7: Deleting namespace..."
kubectl delete -f namespace.yaml --ignore-not-found=true
echo "   ✅ Namespace deleted"

echo ""
echo "🎉 Production Cleanup Complete!"
echo "=========================================="
echo "All Security Monitor resources have been removed from EKS."
