# Evolution of Todo - Containerized Deployment

This document describes the containerized deployment of the Evolution of Todo application using Docker, Kubernetes, and Helm.

## Architecture Overview

The system consists of four main components:
- **Frontend**: Next.js web application (port 3000)
- **Backend API**: FastAPI backend service (port 8000)
- **MCP Server**: MCP protocol server for agent communication (port 8001)
- **AI Agent**: AI agent service (port 8002)

All services are designed to be stateless with externalized configuration.

## Prerequisites

- Docker
- Kubernetes cluster (tested with Minikube)
- Helm 3.x
- kubectl

## Local Development Setup

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Access the services:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# MCP Server: http://localhost:8001
# Agent: http://localhost:8002
```

### Using Minikube and Helm

```bash
# Start Minikube
minikube start

# Install the Helm chart
helm install todo-app charts/todo-app/

# Port forward to access services
kubectl port-forward svc/frontend-service 3000:3000
kubectl port-forward svc/backend-service 8000:8000
kubectl port-forward svc/mcp-service 8001:8001
kubectl port-forward svc/agent-service 8002:8002
```

## Configuration

Configuration is externalized through:
- Environment variables for non-sensitive data
- Kubernetes Secrets for sensitive information (database credentials, API keys)

### Environment Variables

The following environment variables can be configured:

**Frontend:**
- `BACKEND_URL`: URL of the backend API

**Backend:**
- `DATABASE_URL`: PostgreSQL database connection string
- `MCP_SERVER_URL`: URL of the MCP server

**MCP Server:**
- `DATABASE_URL`: PostgreSQL database connection string

**AI Agent:**
- `MCP_SERVER_URL`: URL of the MCP server
- `OPENAI_API_KEY`: OpenAI API key

## Deployment

### Production Deployment

To deploy to a production Kubernetes cluster:

1. Update the values in `charts/todo-app/values.yaml` as needed
2. Create secrets for sensitive data:
   ```bash
   kubectl create secret generic db-secret --from-literal=url="your-db-url"
   kubectl create secret generic openai-secret --from-literal=apiKey="your-openai-key"
   ```
3. Deploy using Helm:
   ```bash
   helm install todo-app charts/todo-app/ -n todo-app --create-namespace
   ```

### Helm Values

The Helm chart supports the following customizable values:

- `frontend.replicaCount`: Number of frontend replicas
- `backend.replicaCount`: Number of backend replicas
- `mcp.replicaCount`: Number of MCP server replicas
- `agent.replicaCount`: Number of AI agent replicas
- Resource requests and limits for each service
- Service ports and types

## Health Checks

Each service implements health checks:
- Frontend: `/api/health`
- Backend: `/health`
- MCP Server: `/health`
- AI Agent: `/health`

These endpoints are used for Kubernetes liveness and readiness probes.

## Scaling

Services can be scaled independently:

```bash
# Scale frontend
kubectl scale deployment frontend-deployment --replicas=3

# Scale backend
kubectl scale deployment backend-deployment --replicas=2
```

## Security

- All container images use non-root users where possible
- Sensitive data is stored in Kubernetes Secrets
- Network policies can be configured to restrict service communication
- Regular security scanning of container images is recommended

## Backup and Recovery

Since all services are stateless, backup primarily involves:
- Database backup (handled externally)
- Configuration backup (stored in version control)
- Kubernetes resource definitions (stored in Helm charts)

## Troubleshooting

### Common Issues

1. **Service won't start**: Check logs with `kubectl logs <pod-name>`
2. **Database connection errors**: Verify `DATABASE_URL` in secrets
3. **Inter-service communication failures**: Check service DNS names and ports
4. **Resource constraints**: Adjust resource limits in Helm values

### Useful Commands

```bash
# Check all pods
kubectl get pods

# Check all services
kubectl get services

# Check logs for a specific service
kubectl logs deployment/frontend-deployment

# Execute commands in a running container
kubectl exec -it deployment/backend-deployment -- /bin/sh
```

## Development Workflow

1. Make changes to the application code
2. Build new container images
3. Update the image tags in `values.yaml`
4. Upgrade the Helm release: `helm upgrade todo-app charts/todo-app/`
5. Test the deployment

## Compliance

This deployment follows the constitutional requirements for Phase IV:
- All services are stateless
- No application code changes were made
- All Phase III functionality is preserved
- AI-assisted tools (Gordon, kubectl-ai, kagent) were used only as development-time tools
- Containerization and orchestration technologies are properly implemented