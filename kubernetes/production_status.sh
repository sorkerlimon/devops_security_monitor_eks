#!/bin/bash

# Production EKS Status Check Script
# Shows the status of all Security Monitor resources

echo "📊 Security Monitor Production Status"
echo "=========================================="

# Check namespace
echo "📦 Namespace:"
kubectl get namespace security-monitor 2>/dev/null || echo "   ❌ Namespace not found"

echo ""

# Check pods
echo "🔄 Pods:"
kubectl get pods -n security-monitor 2>/dev/null || echo "   ❌ No pods found"

echo ""

# Check services
echo "🌐 Services:"
kubectl get svc -n security-monitor 2>/dev/null || echo "   ❌ No services found"

echo ""

# Check deployments
echo "🚀 Deployments:"
kubectl get deployment -n security-monitor 2>/dev/null || echo "   ❌ No deployments found"

echo ""

# Check ingress
echo "🌍 Ingress:"
kubectl get ingress -n security-monitor 2>/dev/null || echo "   ❌ No ingress found"

echo ""

# Check certificates
echo "🔒 Certificates:"
kubectl get certificate -n security-monitor 2>/dev/null || echo "   ❌ No certificates found"

echo ""

# Check LoadBalancer
echo "⚖️  LoadBalancer:"
kubectl get svc -n ingress-nginx 2>/dev/null || echo "   ❌ No LoadBalancer found"

echo ""

# Check logs (last 5 lines)
echo "📝 Recent Backend Logs:"
kubectl logs -n security-monitor deployment/security-monitor-backend --tail=5 2>/dev/null || echo "   ❌ No backend logs found"

echo ""

echo "📝 Recent Frontend Logs:"
kubectl logs -n security-monitor deployment/security-monitor-frontend --tail=5 2>/dev/null || echo "   ❌ No frontend logs found"

echo ""
echo "=========================================="
echo "To access the application:"
echo "https://security-monitor.dreamhrai.com"
