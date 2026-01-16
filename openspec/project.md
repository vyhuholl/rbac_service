# Project Context

## Purpose
This project implements a Role-Based Access Control (RBAC) service. The purpose is to provide a centralized system for managing user roles, permissions, and access policies to ensure secure and controlled access to resources in applications. The goals include enabling fine-grained authorization, supporting scalability for large user bases, and integrating seamlessly with various authentication systems.

## Tech Stack
- Backend: Python + Django + DRF
- Database: PostgreSQL
- Deployment: Docker for containerization
- Version Control: Git
- Specification Management: OpenSpec framework
- uv for virtual environment management and running code
- ruff for linting
- ruff-format for code formatting (line length: 79, quote-style: single)
- pytest for testing
- pytest-cov for code coverage reporting

## Project Conventions

### Code Style
- Use ruff for linting and ruff-format for formatting
- Line length: 79 characters
- Quote style: single
- Follow PEP 8 style guide with ruff-specific rules

### Architecture Patterns
Follow Django's MTV (Model-Template-View) pattern extended with Django REST Framework (DRF) for API development. Use a service layer to encapsulate business logic and keep views thin. Implement RBAC using custom permission classes and decorators. Database schema includes models for Users, Roles, Permissions, and many-to-many relationships. Adopt microservices principles if the system grows, but start monolithic. Ensure scalability with database indexing and caching.

### Testing Strategy
Employ pytest + pytest-django as the primary testing framework. Write unit tests for individual components like models, serializers, and services. Create integration tests for API endpoints using DRF's test client. Use pytest-cov for code coverage reporting, aiming for at least 80% coverage. Develop fixtures for reusable test data (e.g., users, roles, permissions). Include tests for authentication flows, permission checks, and edge cases. Run tests automatically in the CI/CD pipeline before deployments.

### Git Workflow
Adopt GitFlow branching strategy: 'master' branch for production releases, 'develop' branch for ongoing development. Create feature branches (feature/*) from develop for new features, bugfix branches (bugfix/*) for fixes, and hotfix branches (hotfix/*) from main for urgent patches. Use pull requests with mandatory code review before merging to develop or main. Commit messages follow Conventional Commits: type(scope): description (e.g., feat(auth): implement JWT authentication, fix(roles): correct permission assignment). For architectural changes or new capabilities, create and apply change proposals using the OpenSpec framework as outlined in AGENTS.md.

## Domain Context
Role-Based Access Control (RBAC) is an access control paradigm whereby users are granted access to resources based on their assigned roles. Core concepts include: Principals (users or entities), Roles (named sets of permissions), Permissions (specific rights like read, write, delete on resources), and Resources (protected entities). Roles can form hierarchies where higher-level roles inherit permissions from lower ones. Key principles: Principle of Least Privilege (grant minimal necessary access), Separation of Duties (prevent conflicts of interest), and Role-Based Security. Common operations: User-role assignment, role-permission association, permission checks during resource access.

## Important Constraints
Technical: Require Python 3.10 or higher, Django 4.2+, DRF 3.14+, PostgreSQL 13+. Performance constraints: Support 10,000+ concurrent users with sub-100ms response times for permission checks. Scalability: Design for horizontal scaling behind a load balancer. Security: Mandatory encryption (HTTPS/TLS 1.3), rate limiting, comprehensive audit logging. Regulatory: Ensure GDPR compliance for user data processing, data minimization, and user consent. Business: Flexible for enterprise deployments, support integration with SAML/OAuth providers, avoid vendor lock-in.

## External Dependencies
PostgreSQL database for persistent storage of users, roles, and permissions.