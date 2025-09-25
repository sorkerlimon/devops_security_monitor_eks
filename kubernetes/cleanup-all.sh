#!/bin/bash

echo "🧹 Starting Complete Cleanup..."

# Function to delete namespace from context
delete_namespace_from_context() {
    local context=$1
    echo "Deleting from context: $context"
    kubectl config use-context "$context" 2>/dev/null || echo "Context $context not found, skipping..."
    
    # Delete namespace and all resources
    kubectl delete namespace security-monitor --ignore-not-found=true
    kubectl delete all --all --namespace=security-monitor --ignore-not-found=true
    kubectl delete configmap --all --namespace=security-monitor --ignore-not-found=true
    kubectl delete secret --all --namespace=security-monitor --ignore-not-found=true
    kubectl delete pvc --all --namespace=security-monitor --ignore-not-found=true
}

# Delete from all contexts
echo "📦 Deleting namespaces from all contexts..."
delete_namespace_from_context "arn:aws:eks:eu-central-1:299138067566:cluster/devops_cluster"
delete_namespace_from_context "arn:aws:eks:eu-central-1:299138067566:cluster/cluster-devops"
delete_namespace_from_context "kind-cka-cluster1"
delete_namespace_from_context "kind-cks-cluster2"

# Delete Kind clusters
echo "🗑️ Deleting Kind clusters..."
kind delete cluster --name cka-cluster1 2>/dev/null || echo "Kind cluster cka-cluster1 not found"
kind delete cluster --name cks-cluster2 2>/dev/null || echo "Kind cluster cks-cluster2 not found"

# Clean up kubectl contexts
echo "🔧 Cleaning up kubectl contexts..."
kubectl config delete-context kind-cka-cluster1 2>/dev/null || echo "Context kind-cka-cluster1 not found"
kubectl config delete-context kind-cks-cluster2 2>/dev/null || echo "Context kind-cks-cluster2 not found"

# Clean up kubectl clusters
echo "🏗️ Cleaning up kubectl clusters..."
kubectl config delete-cluster kind-cka-cluster1 2>/dev/null || echo "Cluster kind-cka-cluster1 not found"
kubectl config delete-cluster kind-cks-cluster2 2>/dev/null || echo "Cluster kind-cks-cluster2 not found"

# Clean up kubectl users
echo "👤 Cleaning up kubectl users..."
kubectl config unset users.kind-cka-cluster1 2>/dev/null || echo "User kind-cka-cluster1 not found"
kubectl config unset users.kind-cks-cluster2 2>/dev/null || echo "User kind-cks-cluster2 not found"

# Clean up Docker images
echo "🐳 Cleaning up Docker images..."
docker rmi $(docker images | grep "devops-backend\|devops-frontend" | awk '{print $3}') --force 2>/dev/null || echo "No Docker images to clean"

# Clean up Docker system
echo "🧽 Cleaning up Docker system..."
docker system prune -a --force

# Clean up ECR repositories (optional - uncomment if needed)
# echo "☁️ Cleaning up ECR repositories..."
# aws ecr delete-repository --repository-name devops-backend --force --region eu-central-1 2>/dev/null || echo "ECR repository devops-backend not found"
# aws ecr delete-repository --repository-name devops-frontend --force --region eu-central-1 2>/dev/null || echo "ECR repository devops-frontend not found"

echo "✅ Cleanup Complete!"
echo ""
echo "Remaining contexts:"
kubectl config get-contexts
