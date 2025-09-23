# Security Monitor - Monitoring Setup

## 📊 Monitoring Overview

This directory contains monitoring configurations for the Security Monitor application, including Prometheus, Grafana, and CloudWatch integration.

## 🛠️ Components

### 1. Prometheus & Grafana
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **AlertManager**: Alerting and notifications

### 2. CloudWatch Integration
- **CloudWatch Agent**: Container and application metrics
- **Log Groups**: Centralized logging
- **Custom Metrics**: Application-specific metrics

## 🚀 Quick Setup

### Install Prometheus & Grafana
```bash
# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Prometheus stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --values monitoring/prometheus-grafana/values.yaml

# Wait for deployment
kubectl wait --for=condition=available --timeout=300s deployment/prometheus-grafana -n monitoring
```

### Install CloudWatch Agent
```bash
# Create namespace
kubectl create namespace amazon-cloudwatch

# Install CloudWatch agent
kubectl apply -f monitoring/cloudwatch-config.yaml

# Verify installation
kubectl get pods -n amazon-cloudwatch
```

## 📈 Dashboards

### Security Monitor Dashboard
- **Application Metrics**: Response times, error rates, throughput
- **Resource Usage**: CPU, memory, disk usage
- **Database Metrics**: Connection pool, query performance
- **Security Metrics**: Authentication attempts, failed logins

### Kubernetes Cluster Dashboard
- **Node Metrics**: CPU, memory, disk, network
- **Pod Metrics**: Resource usage per pod
- **Service Metrics**: Service health and performance
- **Ingress Metrics**: Traffic and error rates

## 🔔 Alerting Rules

### Application Alerts
- **High Error Rate**: > 5% error rate for 5 minutes
- **High Response Time**: > 1 second average response time
- **Database Connection Issues**: Connection pool exhaustion
- **Memory Usage**: > 80% memory usage

### Infrastructure Alerts
- **Pod Restarts**: Pod restarting frequently
- **Node Issues**: Node not ready or high resource usage
- **Disk Space**: < 20% disk space remaining
- **Network Issues**: High packet loss or latency

## 📊 Metrics Collection

### Application Metrics
```python
# Backend metrics (FastAPI)
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Database metrics
DB_CONNECTIONS = Gauge('database_connections_active', 'Active database connections')
DB_QUERY_DURATION = Histogram('database_query_duration_seconds', 'Database query duration')

# Security metrics
LOGIN_ATTEMPTS = Counter('login_attempts_total', 'Total login attempts', ['status'])
FAILED_LOGINS = Counter('failed_logins_total', 'Failed login attempts')
```

### Frontend Metrics
```javascript
// Frontend metrics (React)
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

// Core Web Vitals
getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);

// Custom metrics
const trackPageView = (page) => {
  // Send to analytics
  console.log('Page view:', page);
};
```

## 🔍 Logging Strategy

### Log Levels
- **ERROR**: Critical errors requiring immediate attention
- **WARN**: Warning conditions that should be investigated
- **INFO**: General information about application flow
- **DEBUG**: Detailed information for debugging

### Log Format
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "service": "security-monitor-backend",
  "message": "User login successful",
  "user_id": "admin",
  "ip_address": "192.168.1.1",
  "request_id": "req-123456"
}
```

### Log Aggregation
- **CloudWatch Logs**: Centralized log storage
- **Log Groups**: Organized by service and environment
- **Log Streams**: Individual pod/container logs
- **Retention**: 30 days for application logs, 7 days for debug logs

## 🚨 Alerting Configuration

### Alert Channels
- **Email**: Critical alerts to admin team
- **Slack**: Real-time notifications to DevOps channel
- **PagerDuty**: On-call escalation for critical issues
- **Webhook**: Custom integrations

### Alert Severity Levels
- **Critical**: Service down, security breach
- **High**: Performance degradation, resource exhaustion
- **Medium**: Warning conditions, capacity planning
- **Low**: Informational alerts, maintenance windows

## 📊 Performance Monitoring

### Key Performance Indicators (KPIs)
- **Availability**: 99.9% uptime target
- **Response Time**: < 200ms average API response
- **Throughput**: 1000+ requests per minute
- **Error Rate**: < 1% error rate

### Monitoring Queries
```promql
# Average response time
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# Database connection pool usage
database_connections_active / database_connections_max

# Memory usage
container_memory_usage_bytes / container_spec_memory_limit_bytes
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Metrics Not Appearing
```bash
# Check Prometheus targets
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring
# Open http://localhost:9090/targets

# Check service monitor
kubectl get servicemonitor -n security-monitor
```

#### 2. Grafana Dashboard Issues
```bash
# Check Grafana logs
kubectl logs deployment/prometheus-grafana -n monitoring

# Access Grafana
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
# Open http://localhost:3000 (admin/admin123)
```

#### 3. CloudWatch Logs Not Appearing
```bash
# Check CloudWatch agent
kubectl logs daemonset/cloudwatch-agent -n amazon-cloudwatch

# Check log groups in AWS Console
aws logs describe-log-groups --log-group-name-prefix "/aws/eks/security-monitor"
```

### Debug Commands
```bash
# Check all monitoring pods
kubectl get pods -n monitoring
kubectl get pods -n amazon-cloudwatch

# Check Prometheus configuration
kubectl get configmap prometheus-kube-prometheus-prometheus -n monitoring -o yaml

# Check Grafana configuration
kubectl get configmap prometheus-grafana -n monitoring -o yaml

# Check CloudWatch configuration
kubectl get configmap cloudwatch-config -n amazon-cloudwatch -o yaml
```

## 📚 Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
- [Kubernetes Monitoring](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/)

---

**For monitoring support, contact the DevOps team or create an issue in the repository.**
