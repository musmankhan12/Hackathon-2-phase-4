# Phase IV Quickstart Guide

## Overview

This guide provides instructions for quickly deploying the Evolution of Todo system using containerization and Kubernetes. This is intended for developers and operators who need to get the system running quickly.

## Prerequisites

### Local Development
- Docker Desktop or Docker Engine
- Minikube
- Helm 3.x
- kubectl
- Git

### Production Deployment
- Kubernetes cluster (v1.20+)
- Helm 3.x
- kubectl
- Container registry access
- Domain name and TLS certificates (optional for basic deployment)

## Quick Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Start Minikube Cluster
```bash
minikube start
```

### 3. Build Container Images
Using Docker AI Agent (Gordon) to assist with optimized Dockerfiles:
```bash
# Gordon will help generate optimized Dockerfiles
gordon analyze .
gordon generate-dockerfile frontend --base=node:18-alpine
gordon generate-dockerfile backend --base=python:3.11-slim
gordon generate-dockerfile mcp-server --base=python:3.11-slim
gordon generate-dockerfile ai-agent --base=python:3.11-slim
```

### 4. Build and Push Images
```bash
# Build all images
docker build -t todo-frontend:latest -f Dockerfile.frontend .
docker build -t todo-backend:latest -f Dockerfile.backend .
docker build -t todo-mcp:latest -f Dockerfile.mcp .
docker build -t todo-agent:latest -f Dockerfile.agent .

# If using remote registry, tag and push
docker tag todo-frontend:latest <registry>/todo-frontend:latest
docker tag todo-backend:latest <registry>/todo-backend:latest
docker tag todo-mcp:latest <registry>/todo-mcp:latest
docker tag todo-agent:latest <registry>/todo-agent:latest

docker push <registry>/todo-frontend:latest
docker push <registry>/todo-backend:latest
docker push <registry>/todo-mcp:latest
docker push <router>/todo-agent:latest
```

### 5. Install Helm Chart
```bash
# Navigate to helm chart directory
cd charts/todo-app

# Install the chart
helm install todo-app . \
  --set frontend.image.repository=todo-frontend \
  --set frontend.image.tag=latest \
  --set backend.image.repository=todo-backend \
  --set backend.image.tag=latest \
  --set mcp.image.repository=todo-mcp \
  --set mcp.image.tag=latest \
  --set agent.image.repository=todo-agent \
  --set agent.image.tag=latest \
  --set database.url=<your-database-url>
```

### 6. Verify Installation
```bash
# Check all pods are running
kubectl get pods

# Check services are available
kubectl get services

# Check ingress (if configured)
kubectl get ingress
```

### 7. Access the Application
```bash
# Get the frontend service URL
minikube service todo-frontend --url

# Or if using ingress
minikube tunnel
# Then access http://localhost (or your configured domain)
```

## Configuration Options

### Environment Variables
Configure the system using environment variables passed through Helm values:

```yaml
# Example values.yaml
frontend:
  env:
    - name: BACKEND_URL
      value: "http://todo-backend:8000"
backend:
  env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: url
    - name: MCP_SERVER_URL
      value: "http://todo-mcp:8001"
mcp:
  env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: url
agent:
  env:
    - name: MCP_SERVER_URL
      value: "http://todo-mcp:8001"
    - name: OPENAI_API_KEY
      valueFrom:
        secretKeyRef:
          name: openai-secret
          key: apiKey
```

### Resource Allocation
Adjust resource allocation based on your needs:

```yaml
frontend:
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi
backend:
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi
```

## Troubleshooting

### Common Issues

#### Pods Stuck in Pending State
- Check if there are enough resources in the cluster
- Verify node selectors or affinity rules

#### Service Not Accessible
- Check if the service port matches the container port
- Verify ingress configuration if using ingress

#### Database Connection Issues
- Verify DATABASE_URL is correctly configured
- Check if the database is accessible from the cluster

### Useful Commands

```bash
# View logs for a specific service
kubectl logs -l app=todo-frontend

# Get detailed pod information
kubectl describe pod <pod-name>

# Execute commands inside a container
kubectl exec -it <pod-name> -- /bin/sh

# Port forward for local debugging
kubectl port-forward svc/todo-frontend 3000:3000
```

## Cleanup

To remove the deployment:

```bash
# Uninstall the Helm release
helm uninstall todo-app

# Stop minikube (for local development)
minikube stop

# Delete minikube cluster (to free resources)
minikube delete
```

## Next Steps

1. Configure production-grade database access
2. Set up monitoring and logging
3. Implement CI/CD pipeline for automated deployments
4. Configure SSL/TLS for secure connections
5. Set up backup and disaster recovery procedures