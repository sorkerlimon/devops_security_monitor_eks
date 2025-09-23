# Security Monitor - Architecture Documentation

## 🏗️ System Architecture

### High-Level Architecture

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

## 🔧 Component Details

### Frontend Architecture
- **Technology**: React 18 + Vite + Tailwind CSS
- **Container**: Multi-stage Docker build
- **Web Server**: NGINX Alpine
- **Port**: 3000
- **Replicas**: 2 (High Availability)

### Backend Architecture
- **Technology**: FastAPI + Python 3.11
- **Container**: Python slim base image
- **Port**: 8000
- **Replicas**: 2 (High Availability)
- **Database**: MySQL with SQLAlchemy ORM

### Database Architecture
- **Technology**: Amazon RDS MySQL
- **Connection Pooling**: SQLAlchemy with connection pooling
- **Security**: VPC isolation, encryption at rest
- **Backup**: Automated snapshots

## 🌐 Network Architecture

### VPC Configuration
```
VPC: 10.0.0.0/16
├── Public Subnets (2 AZs)
│   ├── 10.0.1.0/24 (AZ-a)
│   └── 10.0.2.0/24 (AZ-b)
└── Private Subnets (2 AZs)
    ├── 10.0.3.0/24 (AZ-a) - EKS Nodes
    └── 10.0.4.0/24 (AZ-b) - EKS Nodes
```

### Security Groups
- **EKS Cluster SG**: Inbound 443 from ALB
- **EKS Node SG**: Inbound 1025-65535 from EKS Cluster SG
- **RDS SG**: Inbound 3306 from EKS Node SG
- **ALB SG**: Inbound 80,443 from 0.0.0.0/0

## 🔄 Data Flow

### User Request Flow
1. **User** → Browser request to `security-monitor.dreamhrai.com`
2. **Route 53** → DNS resolution to ALB
3. **ALB** → Load balancing to NGINX Ingress
4. **NGINX Ingress** → Route based on path:
   - `/` → Frontend pods
   - `/api/*` → Backend pods
5. **Backend** → Database queries to RDS MySQL
6. **Response** → Back through the chain to user

### Authentication Flow
1. **Frontend** → Login form submission
2. **Backend** → Validate credentials against database
3. **Backend** → Generate JWT token
4. **Frontend** → Store token in localStorage
5. **Frontend** → Include token in subsequent requests

## 📊 Monitoring Architecture

### Logging Strategy
```
Application Logs → CloudWatch Logs
├── Frontend Logs: /aws/eks/security-monitor/frontend
├── Backend Logs: /aws/eks/security-monitor/backend
└── Ingress Logs: /aws/eks/security-monitor/ingress
```

### Metrics Collection
- **Kubernetes Metrics**: Node and pod metrics
- **Application Metrics**: Custom application metrics
- **Database Metrics**: RDS performance insights
- **Infrastructure Metrics**: EKS cluster health

## 🔒 Security Architecture

### Defense in Depth
1. **Network Level**: VPC, Security Groups, NACLs
2. **Application Level**: JWT authentication, input validation
3. **Container Level**: Non-root users, minimal base images
4. **Kubernetes Level**: RBAC, Pod Security Standards
5. **Cloud Level**: IAM roles, encryption

### Secrets Management
- **Kubernetes Secrets**: Database credentials, JWT secrets
- **AWS Secrets Manager**: Integration for production secrets
- **Encryption**: Secrets encrypted at rest and in transit

## 🚀 Deployment Architecture

### Rolling Deployment Strategy
1. **New Pods** → Start with new image
2. **Health Checks** → Verify new pods are healthy
3. **Traffic Shift** → Gradually shift traffic to new pods
4. **Old Pods** → Terminate old pods
5. **Rollback** → Automatic rollback on failure

### Blue-Green Deployment
- **Blue Environment**: Current production
- **Green Environment**: New version
- **Switch**: Instant traffic switch
- **Rollback**: Instant rollback capability

## 📈 Scalability Architecture

### Horizontal Scaling
- **HPA**: CPU and memory-based scaling
- **VPA**: Vertical pod autoscaling
- **Cluster Autoscaler**: Node group scaling

### Vertical Scaling
- **Resource Requests**: Guaranteed resources
- **Resource Limits**: Maximum resource usage
- **Node Types**: Optimized instance types

## 🔄 CI/CD Architecture

### Pipeline Stages
1. **Source**: Git repository
2. **Build**: Docker image building
3. **Test**: Automated testing
4. **Security**: Vulnerability scanning
5. **Deploy**: Kubernetes deployment
6. **Verify**: Health checks

### Environment Promotion
```
Development → Staging → Production
     ↓           ↓         ↓
   Local      EKS Dev   EKS Prod
```

## 🛡️ Disaster Recovery Architecture

### Backup Strategy
- **Database**: Automated RDS snapshots
- **Configuration**: Git-based version control
- **Images**: ECR image versioning
- **Infrastructure**: Terraform state management

### Recovery Procedures
- **RTO**: 15 minutes (Recovery Time Objective)
- **RPO**: 5 minutes (Recovery Point Objective)
- **Multi-AZ**: Database and application redundancy
- **Cross-Region**: Backup to secondary region

## 📋 Performance Characteristics

### Expected Performance
- **Response Time**: < 200ms for API calls
- **Throughput**: 1000+ requests/minute
- **Availability**: 99.9% uptime
- **Scalability**: Auto-scale to 10+ pods

### Resource Requirements
- **Frontend**: 100m CPU, 128Mi memory per pod
- **Backend**: 200m CPU, 256Mi memory per pod
- **Database**: db.t3.micro (1 vCPU, 1GB RAM)
- **Storage**: 20GB for database

## 🔧 Configuration Management

### Environment Variables
- **ConfigMaps**: Non-sensitive configuration
- **Secrets**: Sensitive data (passwords, keys)
- **External Config**: AWS Parameter Store integration

### Configuration Hierarchy
1. **Default Values**: Application defaults
2. **ConfigMap Values**: Kubernetes ConfigMap
3. **Secret Values**: Kubernetes Secrets
4. **Environment Overrides**: Pod-level overrides
