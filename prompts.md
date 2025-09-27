# GetCovered Application Development Prompts

This document contains comprehensive prompts that could have been used to build the entire GetCovered application from scratch. These prompts are organized by development phase and can be used for evaluation purposes.

## Table of Contents

1. [Project Planning & Architecture](#project-planning--architecture)
2. [Backend Development](#backend-development)
3. [Frontend Development](#frontend-development)
4. [Database & Authentication](#database--authentication)
5. [Integration & Testing](#integration--testing)
6. [Deployment & DevOps](#deployment--devops)
7. [Debugging & Troubleshooting](#debugging--troubleshooting)
8. [Optimization & Enhancements](#optimization--enhancements)

---

## Project Planning & Architecture

### Initial Project Setup

**Prompt 1: Project Architecture Planning**
```
I need to create a full-stack web application called "GetCovered" for user management with the following requirements:

- User authentication with Google OAuth
- Role-based access control (Admin/Client roles)
- User profile management
- Admin dashboard for user management
- Client dashboard for personal profiles
- Domain-restricted registration (only specific email domains allowed)
- Modern, responsive UI
- RESTful API design
- Docker containerization
- Production deployment ready

Please suggest a complete technology stack and project structure that would be optimal for this application. Include recommendations for:
- Backend framework and database
- Frontend framework and styling
- Authentication strategy
- Deployment approach
- Development workflow
```

**Prompt 2: Project Structure Creation**
```
Based on the technology stack recommendation (FastAPI + React + MySQL), create a complete project directory structure for the GetCovered application. Include:

- Root directory structure
- Backend application structure with FastAPI
- Frontend application structure with React
- Configuration files for Docker, deployment, and development
- Environment variable templates
- Package.json files with appropriate dependencies
- Docker configuration for multi-container setup

Please create all necessary directories and initial configuration files.
```

**Prompt 3: Development Environment Setup**
```
Create a complete development environment setup for the GetCovered project including:

1. Docker Compose configuration for local development with:
   - MySQL database container
   - FastAPI backend container
   - React frontend container
   - Proper networking and volume management

2. Package.json files for both root and frontend with:
   - Appropriate scripts for development and production
   - All necessary dependencies
   - Heroku deployment configuration

3. Requirements.txt for Python backend with all necessary packages

4. Environment variable templates (.env.example files) for both backend and frontend
```

---

## Backend Development

### Core Backend Setup

**Prompt 4: FastAPI Application Foundation**
```
Create a FastAPI application (main.py) for the GetCovered user management system with the following features:

1. Basic FastAPI app setup with CORS middleware
2. SQLAlchemy integration with MySQL database
3. User model with fields: id, username, email, password_hash, role, created_at, updated_at
4. Database connection with environment variable configuration
5. Automatic table creation on startup
6. Basic health check endpoint
7. Session middleware setup
8. Proper error handling and logging

Include all necessary imports and configuration for a production-ready application.
```

**Prompt 5: Authentication System Implementation**
```
Implement a complete authentication system for the FastAPI backend with:

1. Google OAuth 2.0 integration using Authlib
2. JWT token generation and validation
3. User registration with domain restriction (only allowed email domains)
4. Login endpoints (/auth/login, /auth/callback)
5. Token verification middleware
6. Role-based access control decorator
7. Password hashing utilities (for fallback authentication)
8. Session management

Include proper error handling for authentication failures and security best practices.
```

**Prompt 6: User Management API Endpoints**
```
Create comprehensive user management API endpoints for the FastAPI backend:

1. GET /users/me - Get current user profile (authenticated users)
2. PUT /users/me - Update current user profile (authenticated users)
3. GET /users - List all users with pagination (admin only)
4. POST /users - Create new user (admin only)
5. PUT /users/{user_id} - Update specific user (admin only)
6. DELETE /users/{user_id} - Delete user (admin only)

Include:
- Proper request/response models using Pydantic
- Role-based access control
- Input validation and sanitization
- Error handling with appropriate HTTP status codes
- Database transaction management
```

### Advanced Backend Features

**Prompt 7: Database Models and Relationships**
```
Enhance the SQLAlchemy database models for the GetCovered application:

1. Improve the User model with additional fields:
   - first_name, last_name
   - profile_picture_url
   - phone_number
   - is_active, is_verified
   - last_login timestamp

2. Add proper database constraints and indexes
3. Implement database migration system using Alembic
4. Add data validation at the database level
5. Create utility functions for database operations
6. Add database seeding for admin user creation

Include proper relationship mappings and database best practices.
```

**Prompt 8: Security and Middleware Enhancement**
```
Enhance the FastAPI application with advanced security features:

1. Implement rate limiting middleware
2. Add request logging and audit trails
3. Implement CSRF protection
4. Add input sanitization middleware
5. Implement secure headers middleware
6. Add API key authentication option
7. Implement refresh token mechanism
8. Add brute force protection for login attempts

Ensure all security implementations follow OWASP best practices.
```

---

## Frontend Development

### React Application Foundation

**Prompt 9: React Application Setup**
```
Create a React application for the GetCovered frontend with:

1. Modern React 18 setup with functional components and hooks
2. React Router DOM for client-side routing
3. Axios for API communication with interceptors
4. Context API for global state management (authentication state)
5. Tailwind CSS integration for styling
6. Component structure for:
   - App.js (main application component)
   - Login component
   - Dashboard components (Admin/Client)
   - User profile components

Include proper error boundaries and loading states.
```

**Prompt 10: Authentication Frontend Implementation**
```
Implement the frontend authentication system for the React application:

1. Google OAuth login flow integration
2. JWT token management (storage, refresh, expiration handling)
3. Protected route components
4. Authentication context provider
5. Login component with Google sign-in button
6. Automatic token validation on app startup
7. Logout functionality with token cleanup
8. Redirect handling after successful authentication

Include proper error handling and user feedback for authentication states.
```

**Prompt 11: Admin Dashboard Development**
```
Create a comprehensive admin dashboard component for the GetCovered application:

1. User management interface with:
   - User list with search and pagination
   - User creation form
   - User editing capabilities
   - User deletion with confirmation
   - Role assignment functionality

2. Dashboard layout with:
   - Navigation sidebar
   - Header with user info and logout
   - Data tables with sorting and filtering
   - Modal dialogs for user operations
   - Responsive design for mobile devices

3. State management for:
   - User data fetching and caching
   - Form state management
   - Loading and error states

Use Tailwind CSS for styling and ensure accessibility compliance.
```

**Prompt 12: Client Dashboard and Profile Management**
```
Create client dashboard and profile management components:

1. Client Dashboard with:
   - Welcome message with user info
   - Profile summary card
   - Quick access to profile editing
   - Recent activity display (if applicable)

2. User Profile component with:
   - Display mode showing user information
   - Edit mode with form fields
   - Profile picture upload (optional)
   - Form validation and error handling
   - Save/cancel functionality

3. Profile editing with:
   - Form validation (client and server-side)
   - Real-time validation feedback
   - Optimistic updates
   - Error handling and recovery

Ensure responsive design and smooth user experience.
```

### Advanced Frontend Features

**Prompt 13: UI/UX Enhancement and Responsive Design**
```
Enhance the React application with advanced UI/UX features:

1. Implement responsive design with Tailwind CSS:
   - Mobile-first approach
   - Tablet and desktop breakpoints
   - Flexible grid layouts
   - Responsive navigation

2. Add interactive elements:
   - Loading spinners and skeletons
   - Toast notifications for user feedback
   - Confirmation dialogs
   - Form field animations
   - Hover effects and transitions

3. Accessibility improvements:
   - ARIA labels and roles
   - Keyboard navigation support
   - Screen reader compatibility
   - Color contrast compliance

4. Performance optimizations:
   - Component lazy loading
   - Image optimization
   - Code splitting
   - Memoization where appropriate
```

**Prompt 14: State Management and API Integration**
```
Implement comprehensive state management and API integration:

1. Create API service layer with:
   - Centralized Axios configuration
   - Request/response interceptors
   - Error handling utilities
   - API endpoint constants
   - Retry logic for failed requests

2. Implement global state management:
   - Authentication state context
   - User data context
   - Loading states context
   - Error handling context

3. Add caching strategies:
   - User data caching
   - API response caching
   - Optimistic updates
   - Cache invalidation

4. Implement real-time features (if needed):
   - WebSocket connection setup
   - Real-time notifications
   - Live data updates
```

---

## Database & Authentication

**Prompt 15: Database Schema Design and Implementation**
```
Design and implement a comprehensive database schema for the GetCovered application:

1. Create detailed database schema with:
   - Users table with all necessary fields
   - Indexes for performance optimization
   - Foreign key constraints
   - Check constraints for data validation

2. Implement database initialization script:
   - Table creation with proper data types
   - Default data insertion (admin user)
   - Database migration scripts
   - Backup and restore procedures

3. Add database utilities:
   - Connection pooling configuration
   - Database health check functions
   - Performance monitoring queries
   - Data cleanup procedures

Include MySQL-specific optimizations and best practices.
```

**Prompt 16: OAuth Integration and Security**
```
Implement comprehensive OAuth and security features:

1. Google OAuth 2.0 complete integration:
   - OAuth client configuration
   - Authorization flow implementation
   - User info retrieval and processing
   - Error handling for OAuth failures

2. JWT token management:
   - Token generation with proper claims
   - Token validation and expiration handling
   - Refresh token implementation
   - Token blacklisting for logout

3. Security enhancements:
   - Email domain validation
   - Rate limiting for authentication endpoints
   - Brute force protection
   - Secure cookie configuration (for production)

4. User session management:
   - Session creation and validation
   - Session cleanup and expiration
   - Concurrent session handling
```

---

## Integration & Testing

**Prompt 17: API Testing and Validation**
```
Create comprehensive testing for the GetCovered application:

1. Backend API testing:
   - Unit tests for all endpoints
   - Integration tests for authentication flow
   - Database operation tests
   - Mock testing for external services (Google OAuth)

2. Frontend component testing:
   - Unit tests for React components
   - Integration tests for user flows
   - Authentication flow testing
   - Form validation testing

3. End-to-end testing:
   - Complete user registration flow
   - Login and logout processes
   - Admin user management operations
   - Cross-browser compatibility tests

Use appropriate testing frameworks (pytest for backend, Jest/React Testing Library for frontend).
```

**Prompt 18: Frontend-Backend Integration**
```
Ensure seamless integration between frontend and backend:

1. API contract validation:
   - Consistent request/response formats
   - Error handling standardization
   - HTTP status code conventions
   - API versioning strategy

2. Authentication flow integration:
   - OAuth callback handling
   - Token passing and validation
   - Automatic token refresh
   - Session synchronization

3. Error handling coordination:
   - Backend error message formatting
   - Frontend error display and handling
   - User-friendly error messages
   - Graceful degradation for failures

4. Performance optimization:
   - API response caching
   - Request batching where appropriate
   - Loading state management
   - Optimistic UI updates
```

---

## Deployment & DevOps

**Prompt 19: Docker Containerization**
```
Create comprehensive Docker configuration for the GetCovered application:

1. Multi-stage Dockerfile for backend:
   - Python environment setup
   - Dependency installation optimization
   - Security best practices
   - Production-ready configuration

2. Dockerfile for frontend:
   - Node.js build process
   - Static file serving setup
   - Nginx configuration (if needed)
   - Asset optimization

3. Docker Compose for development:
   - Service definitions for all components
   - Network configuration
   - Volume mounting for development
   - Environment variable management

4. Production Docker setup:
   - Optimized images for production
   - Health checks for all services
   - Restart policies
   - Resource limits and monitoring
```

**Prompt 20: Heroku Deployment Configuration**
```
Configure the GetCovered application for Heroku deployment:

1. Heroku-specific configuration:
   - Procfile for process management
   - Runtime specification
   - Buildpack configuration
   - Environment variable setup

2. Database configuration:
   - Heroku PostgreSQL integration
   - Database URL handling
   - Migration scripts for deployment
   - Database backup strategies

3. Build process optimization:
   - Frontend build automation
   - Asset compilation and optimization
   - Static file serving configuration
   - Production environment variables

4. Monitoring and logging:
   - Application logging setup
   - Error tracking integration
   - Performance monitoring
   - Health check endpoints
```

**Prompt 21: CI/CD Pipeline Setup**
```
Create a CI/CD pipeline for the GetCovered application:

1. GitHub Actions workflow:
   - Automated testing on pull requests
   - Code quality checks (linting, formatting)
   - Security vulnerability scanning
   - Build process validation

2. Automated deployment:
   - Staging environment deployment
   - Production deployment triggers
   - Database migration automation
   - Rollback procedures

3. Quality assurance:
   - Code coverage reporting
   - Performance testing
   - Security testing
   - Dependency vulnerability scanning

4. Monitoring and alerts:
   - Deployment success/failure notifications
   - Performance monitoring setup
   - Error tracking and alerting
   - Uptime monitoring
```

---

## Debugging & Troubleshooting

**Prompt 22: Backend Debugging and Error Resolution**
```
Help me debug and resolve common backend issues in the GetCovered application:

1. Database connection issues:
   - MySQL connection failures
   - SQLAlchemy configuration problems
   - Database authentication errors
   - Connection pool exhaustion

2. Authentication problems:
   - Google OAuth callback failures
   - JWT token validation errors
   - Session management issues
   - User registration problems

3. API endpoint issues:
   - CORS configuration problems
   - Request validation failures
   - Response serialization errors
   - Permission and authorization bugs

4. Performance issues:
   - Slow database queries
   - Memory leaks
   - High CPU usage
   - Request timeout problems

Provide comprehensive debugging strategies and solutions for each category.
```

**Prompt 23: Frontend Debugging and Issue Resolution**
```
Help me debug and resolve frontend issues in the GetCovered React application:

1. Authentication flow problems:
   - OAuth redirect handling issues
   - Token storage and retrieval problems
   - Protected route access issues
   - Session expiration handling

2. Component rendering issues:
   - State management problems
   - Props passing errors
   - Conditional rendering bugs
   - Component lifecycle issues

3. API integration problems:
   - Network request failures
   - Response handling errors
   - Error boundary failures
   - Loading state management

4. UI/UX issues:
   - Responsive design problems
   - CSS styling conflicts
   - Form validation errors
   - Navigation and routing issues

Include debugging techniques, browser dev tools usage, and common solutions.
```

**Prompt 24: Production Environment Troubleshooting**
```
Help me troubleshoot production environment issues for the GetCovered application:

1. Deployment failures:
   - Heroku build process errors
   - Environment variable configuration issues
   - Database migration failures
   - Static file serving problems

2. Performance issues in production:
   - Slow API response times
   - Database query optimization
   - Memory usage problems
   - High server load

3. Security concerns:
   - Authentication bypass attempts
   - CORS policy violations
   - SSL certificate issues
   - Rate limiting effectiveness

4. User-reported issues:
   - Login failures
   - Data inconsistency problems
   - UI rendering issues
   - Feature accessibility problems

Provide production-specific debugging approaches and monitoring strategies.
```

---

## Optimization & Enhancements

**Prompt 25: Performance Optimization**
```
Optimize the GetCovered application for better performance:

1. Backend optimizations:
   - Database query optimization
   - API response caching strategies
   - Background task processing
   - Resource usage optimization

2. Frontend optimizations:
   - Component rendering optimization
   - Bundle size reduction
   - Image and asset optimization
   - Code splitting implementation

3. Database optimizations:
   - Index optimization
   - Query performance tuning
   - Connection pooling configuration
   - Data archiving strategies

4. Infrastructure optimizations:
   - CDN implementation for static assets
   - Load balancing configuration
   - Caching layer implementation
   - Database read replica setup

Provide specific implementation strategies and performance metrics.
```

**Prompt 26: Security Enhancements**
```
Enhance the security of the GetCovered application:

1. Authentication security:
   - Multi-factor authentication implementation
   - Password policy enforcement
   - Account lockout mechanisms
   - Session security improvements

2. API security:
   - Advanced rate limiting
   - API key management
   - Request signing and validation
   - Input sanitization enhancement

3. Data protection:
   - Data encryption at rest
   - Secure data transmission
   - Personal data anonymization
   - GDPR compliance measures

4. Infrastructure security:
   - Container security hardening
   - Network security configuration
   - Vulnerability scanning automation
   - Security monitoring and alerting

Include implementation guidelines and security best practices.
```

**Prompt 27: Feature Enhancements and Scalability**
```
Add advanced features and improve scalability for the GetCovered application:

1. New feature implementations:
   - Email notification system
   - User activity logging and analytics
   - Advanced search and filtering
   - Bulk user operations

2. Scalability improvements:
   - Microservices architecture migration
   - Database sharding strategies
   - Caching layer implementation
   - Async processing for heavy operations

3. User experience enhancements:
   - Real-time notifications
   - Progressive web app (PWA) features
   - Offline functionality
   - Mobile app development

4. Administrative features:
   - Advanced reporting and analytics
   - User behavior tracking
   - System health monitoring
   - Automated backup and recovery

Provide detailed implementation plans and architectural considerations.
```

**Prompt 28: Code Quality and Maintenance**
```
Improve code quality and maintainability for the GetCovered application:

1. Code refactoring:
   - Backend code organization and modularity
   - Frontend component architecture improvement
   - Common utility function extraction
   - Configuration management enhancement

2. Documentation improvements:
   - API documentation with OpenAPI/Swagger
   - Component documentation with Storybook
   - Deployment and setup guides
   - Contributing guidelines

3. Testing enhancements:
   - Test coverage improvement
   - Integration test automation
   - Performance testing implementation
   - Security testing automation

4. Development workflow improvements:
   - Code review process enhancement
   - Automated code formatting and linting
   - Pre-commit hooks setup
   - Development environment standardization

Include specific tools and processes for long-term maintainability.
```

---

## Evaluation and Submission Prompts

**Prompt 29: Project Documentation and README**
```
Create comprehensive documentation for the GetCovered application:

1. Detailed README.md with:
   - Project overview and features
   - Complete setup instructions
   - Technology stack documentation
   - API documentation
   - Deployment guidelines

2. Technical documentation:
   - Architecture diagrams
   - Database schema documentation
   - API endpoint specifications
   - Security implementation details

3. User documentation:
   - User guide for admin features
   - Client dashboard usage guide
   - Troubleshooting guide
   - FAQ section

4. Developer documentation:
   - Development environment setup
   - Contributing guidelines
   - Code style guide
   - Testing procedures

Ensure the documentation is suitable for technical evaluation and project submission.
```

**Prompt 30: Project Evaluation and Quality Assurance**
```
Perform a comprehensive evaluation of the GetCovered application for submission:

1. Functionality verification:
   - All features working as specified
   - User flows tested and validated
   - Error handling verification
   - Security features validation

2. Code quality assessment:
   - Code organization and structure
   - Best practices implementation
   - Comment and documentation quality
   - Performance considerations

3. Deployment readiness:
   - Production configuration validation
   - Environment variable setup
   - Database migration scripts
   - Monitoring and logging setup

4. Submission preparation:
   - Final code cleanup and organization
   - Documentation completeness check
   - Demo data preparation
   - Presentation material creation

Provide a final checklist and quality assurance report for project submission.
```

---

## Notes for Evaluation

This document contains 30 comprehensive prompts that cover the entire development lifecycle of the GetCovered application. These prompts are designed to:

1. **Demonstrate systematic thinking**: Each prompt builds upon previous ones and shows logical progression
2. **Cover all technical aspects**: From initial planning to deployment and maintenance
3. **Show debugging expertise**: Including troubleshooting and problem-solving approaches
4. **Highlight best practices**: Security, performance, and code quality considerations
5. **Prove production readiness**: Deployment, monitoring, and scalability concerns

The prompts are structured to show how a senior developer would approach building a complex full-stack application with proper planning, implementation, testing, and deployment strategies.