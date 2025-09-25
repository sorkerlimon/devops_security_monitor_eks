#!/bin/bash

# Script to update ECR secret with fresh credentials
# This should be run whenever AWS credentials are refreshed

echo "🔄 Updating ECR secret with fresh credentials..."

# Delete existing ECR secret
echo "1. Deleting existing ECR secret..."
kubectl delete secret ecr-secret -n security-monitor --ignore-not-found=true

# Create new ECR secret with fresh credentials
echo "2. Creating new ECR secret with fresh AWS credentials..."
aws ecr get-login-password --region eu-central-1 | kubectl create secret docker-registry ecr-secret \
  --docker-server=299138067566.dkr.ecr.eu-central-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region eu-central-1) \
  --namespace=security-monitor

# Verify the secret was created
echo "3. Verifying ECR secret..."
kubectl get secret ecr-secret -n security-monitor

echo "✅ ECR secret updated successfully!"
echo "💡 Run this script whenever your AWS credentials are refreshed."
