# Phase IV Data Model

## Overview

This document describes the data model considerations for the containerized deployment of the Evolution of Todo system. Since Phase IV is focused on infrastructure and deployment rather than new functionality, the data model remains unchanged from Phase III.

## Entity Definitions

### Todo Entity
- **Fields**:
  - id: integer (primary key, auto-increment)
  - title: string (required, max length 255)
  - description: string (optional, max length 1000)
  - completed: boolean (default false)
  - created_at: datetime (auto-generated)
  - updated_at: datetime (auto-generated)

### User Entity (Authentication)
- **Fields**:
  - id: integer (primary key, auto-increment)
  - email: string (required, unique, max length 255)
  - name: string (optional, max length 255)
  - created_at: datetime (auto-generated)
  - updated_at: datetime (auto-generated)

## Relationships

### Todo to User Relationship
- One User can have many Todos
- Foreign key: todos.user_id → users.id
- Relationship: todos.user (many-to-one)

## Validation Rules

### Todo Validation
- Title must not be empty (length > 0)
- Title must not exceed 255 characters
- Description, if provided, must not exceed 1000 characters
- Completed status must be boolean

### User Validation
- Email must be valid email format
- Email must be unique
- Email must not exceed 255 characters
- Name, if provided, must not exceed 255 characters

## State Transitions

### Todo State Transitions
- Created → Active (initial state upon creation)
- Active ↔ Completed (toggle between states)
- Any state → Deleted (permanent deletion)

### User State Transitions
- Registered → Active (initial state upon registration)
- Active → Inactive (deactivation - not implemented in current system)

## Configuration Data

### Runtime Configuration
The following configuration values will be externalized as environment variables:

- DATABASE_URL: Connection string for PostgreSQL database
- FRONTEND_PORT: Port for Next.js frontend (default: 3000)
- BACKEND_PORT: Port for FastAPI backend (default: 8000)
- MCP_SERVER_PORT: Port for MCP server (default: 8001)
- AGENT_SERVICE_PORT: Port for AI agent service (default: 8002)
- SECRET_KEY: Secret key for authentication
- DEBUG: Enable/disable debug mode (default: false)

### Kubernetes Resource Configuration
The following resources will be configured via Helm values:

- CPU requests and limits for each service
- Memory requests and limits for each service
- Replica counts for each service
- Health check timeouts and intervals
- Service ports and types

## Constraints

### Database Constraints
- Primary key constraints on all id fields
- Unique constraint on user email
- Foreign key constraint on todo user_id
- Not-null constraints on required fields

### Container Constraints
- All services must be stateless
- No local file storage allowed
- All configuration must be externalized
- All secrets must be passed via environment variables or mounted volumes

## Migration Considerations

Since Phase IV does not involve database schema changes, no migrations are required. The existing schema from Phase II/III remains unchanged.

### Backward Compatibility
- All existing API endpoints remain unchanged
- Database schema remains identical
- MCP tool interfaces remain unchanged
- AI agent behaviors remain unchanged