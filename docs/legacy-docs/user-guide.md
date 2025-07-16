# User Guide

## Getting Started

This guide walks you through using the Autonomous Development System for your first project. The system is designed to handle most development tasks automatically while giving you control over the process.

### Quick Start

#### 1. Initialize Your First Project
```bash
# Navigate to the workspace
cd /mnt/c/bmad-workspace

# Create a new web application
./ultimate-ai-orchestrator.sh my-first-app genesis

# Monitor the initialization
tail -f projects/my-first-app/orchestrator.log
```

#### 2. Enter Development Mode
```bash
# Navigate to your project
cd projects/my-first-app

# Start Claude Code with full integration
claude code --project "$(pwd)"
```

#### 3. Interact with the System
Once in Claude Code, you can:
```
# Check project status
get project status

# View available tools
list tools

# Get next recommended task
get next task

# Research a specific topic
research "React best practices for scalable applications"

# Analyze code complexity
analyze code complexity in src/
```

## Project Modes Explained

### Genesis Mode - New Applications
Perfect for creating applications from scratch:

```bash
# Web applications
./ultimate-ai-orchestrator.sh my-webapp genesis

# Mobile applications  
./ultimate-ai-orchestrator.sh my-mobile-app genesis

# API services
./ultimate-ai-orchestrator.sh my-api genesis
```

**What Genesis Mode Does:**
- Analyzes requirements and selects optimal technology stack
- Creates complete project structure
- Sets up development environment
- Implements core functionality
- Configures testing and deployment pipelines

### Phoenix Mode - Existing Applications
For modernizing or enhancing existing code:

```bash
# Point to existing project directory
./ultimate-ai-orchestrator.sh /path/to/existing/app phoenix

# Or migrate from repository
./ultimate-ai-orchestrator.sh https://github.com/user/repo phoenix
```

**What Phoenix Mode Does:**
- Analyzes existing codebase
- Identifies improvement opportunities
- Suggests modernization strategies
- Implements incremental enhancements
- Maintains backward compatibility

### SaaS Mode - Software as a Service
Specialized for building SaaS applications:

```bash
# Multi-tenant SaaS application
./ultimate-ai-orchestrator.sh my-saas-app saas
```

**What SaaS Mode Does:**
- Implements multi-tenant architecture
- Sets up subscription management
- Configures user authentication and authorization
- Implements billing and payment processing
- Creates admin dashboards and analytics

## Working with Tools

### Research and Intelligence Tools

#### Perplexity AI - Real-time Research
```bash
# Research current trends
perplexity_search_web "latest React 18 features and best practices" --recency day

# Technical deep-dive
perplexity_search_web "microservices architecture patterns 2024" --recency week
```

#### Context7 - Technical Documentation
```bash
# Find API documentation
resolve_library_id "express.js"
get_library_docs "/express/express" --topic "middleware"

# Get examples
get_library_docs "/react/react" --topic "hooks" --tokens 5000
```

#### Brave Search - Comprehensive Web Search
```bash
# Search for specific solutions
brave_web_search "PostgreSQL connection pooling Node.js" --count 10

# Find local resources
brave_local_search "web development agencies near San Francisco"
```

### Analysis and Reasoning Tools

#### Sequential Thinking - Complex Problem Solving
```bash
# Plan a complex feature
sequentialthinking "Design a real-time notification system for a social media app with 100k users"

# Architectural decisions
sequentialthinking "Choose between microservices and monolith for a startup with 5 developers"
```

#### Deep Code Reasoning - Advanced Code Analysis
```bash
# Analyze performance bottlenecks
escalate_analysis --analysis_type performance --depth_level 4

# Debug complex issues
trace_execution_path --entry_point "src/api/users.js:45"

# Test hypotheses
hypothesis_test "Memory leak is caused by event listener accumulation"
```

#### Consult7 - Multi-file Code Analysis
```bash
# Analyze entire codebase
consultation "/path/to/project" ".*\\.js$" "Identify potential security vulnerabilities" "google/gemini-2.5-pro"

# Focus on specific patterns
consultation "/path/to/project" ".*\\.(ts|tsx)$" "Find performance optimization opportunities"
```

### Project Management Tools

#### TaskMaster AI - Intelligent Task Management
```bash
# Initialize project management
initialize_project --projectRoot "/path/to/project" --name "My Project"

# Parse requirements document
parse_prd --projectRoot "/path/to/project" --input "requirements.md"

# Get next task
next_task --projectRoot "/path/to/project"

# Update task status
set_task_status --id "15" --status "in-progress"
```

#### Agentic Tools - Memory and Coordination
```bash
# Create project memory
create_memory --title "Architecture Decision" --content "Chose React over Vue for better team expertise"

# Search memories
search_memories --query "database schema decisions"

# Create task dependencies
add_dependency --id "5" --dependsOn "3"
```

#### Dart - Kanban Project Tracking
```bash
# Create tasks
create_task --project_id "proj_123" --title "Implement user authentication" --description "JWT-based auth system"

# Update task status
update_task --project_id "proj_123" --task_id "task_456" --status "inprogress"

# Add comments
add_task_comment --taskId "task_456" --text "Implemented basic JWT validation"
```

### Development and Automation Tools

#### Make-it-Heavy - Multi-agent Orchestration
```bash
# Install and configure agents
install_repo_mcp_server --name "@makeiteavy/agents"

# Coordinate multiple agents
escalate_analysis --analysis_type "cross_system"
```

#### Desktop Commander - System Automation
```bash
# File operations
read_file --path "/path/to/file.js" --offset 10 --length 50
write_file --path "/path/to/new-file.js" --content "console.log('Hello');"

# Search operations
search_files --path "/project/src" --pattern "*.component.js"
search_code --path "/project" --pattern "useState|useEffect"

# Execute commands
execute_command --command "npm test" --timeout_ms 30000
```

#### GitHub Integration
```bash
# Repository operations
create_repository --name "my-new-repo" --description "Autonomous development test"

# File management
create_or_update_file --owner "username" --repo "my-repo" --path "src/app.js" --content "..." --message "Add main application file"

# Pull requests
create_pull_request --owner "username" --repo "my-repo" --title "Feature: User authentication" --head "feature/auth" --base "main"
```

### Testing and Quality Tools

#### Playwright - End-to-End Testing
```bash
# Navigate and test
browser_navigate --url "http://localhost:3000"
browser_snapshot  # Get accessibility snapshot
browser_click --element "Login button" --ref "button-login"
browser_type --element "Email input" --ref "input-email" --text "test@example.com"

# Generate tests
browser_generate_playwright_test --name "User Login Flow" --description "Test complete login process"
```

#### Puppeteer - Browser Automation
```bash
# Basic navigation
puppeteer_navigate --url "https://myapp.com"
puppeteer_screenshot --name "homepage"

# Interactions
puppeteer_click --selector "#submit-button"
puppeteer_fill --selector "input[name='email']" --value "user@example.com"
```

#### IDE Integration - Real-time Diagnostics
```bash
# Get language diagnostics
getDiagnostics --uri "file:///path/to/file.js"

# Execute code (for Jupyter notebooks)
executeCode --code "print('Testing Python integration')"
```

## Workflows and Examples

### Example 1: Building a React Dashboard

```bash
# 1. Initialize project
./ultimate-ai-orchestrator.sh react-dashboard genesis

# 2. Enter development mode
cd projects/react-dashboard
claude code --project "$(pwd)"

# 3. Research best practices
perplexity_search_web "React dashboard component libraries 2024" --recency week

# 4. Get technical documentation
resolve_library_id "react"
get_library_docs "/facebook/react" --topic "components" --tokens 3000

# 5. Create tasks
create_task --project_id "proj_dashboard" --title "Setup React Router" --description "Configure routing for dashboard sections"

# 6. Analyze existing code (if any)
consultation "src/" ".*\\.(js|jsx)$" "Review component structure and suggest improvements"

# 7. Generate tests
browser_generate_playwright_test --name "Dashboard Navigation" --description "Test all dashboard menu items"

# 8. Deploy to GitHub
create_repository --name "react-dashboard" --description "Autonomous React dashboard"
push_files --owner "username" --repo "react-dashboard" --branch "main" --message "Initial dashboard implementation"
```

### Example 2: API Development with Node.js

```bash
# 1. Initialize API project
./ultimate-ai-orchestrator.sh my-api genesis

# 2. Research API patterns
perplexity_search_web "Node.js REST API best practices 2024" --recency month

# 3. Get documentation
resolve_library_id "express"
get_library_docs "/expressjs/express" --topic "middleware routing" --tokens 4000

# 4. Plan the architecture
sequentialthinking "Design a RESTful API for a task management system with user authentication, task CRUD, and real-time updates"

# 5. Create comprehensive tasks
parse_prd --projectRoot "$(pwd)" --input "api-requirements.md" --numTasks 12

# 6. Implement with testing
create_task --title "Setup Express middleware" --description "Configure CORS, logging, error handling"
create_task --title "Implement JWT authentication" --description "User login/register with JWT tokens"

# 7. Test endpoints
# (After implementation)
execute_command --command "npm run test:api" --timeout_ms 60000

# 8. Deploy
create_pull_request --title "Complete API implementation" --description "Full CRUD API with authentication"
```

### Example 3: Mobile App Development

```bash
# 1. Initialize mobile project
./ultimate-ai-orchestrator.sh mobile-app genesis

# 2. Research mobile frameworks
perplexity_search_web "React Native vs Flutter 2024 comparison" --recency month

# 3. Architecture planning
sequentialthinking "Choose the best mobile development approach for a social media app targeting iOS and Android"

# 4. Setup project structure
initialize_project --projectRoot "$(pwd)" --name "Mobile Social App"

# 5. Create mobile-specific tasks
create_task --title "Setup navigation" --description "Implement tab-based navigation with React Navigation"
create_task --title "User authentication flow" --description "Login/register screens with biometric auth"

# 6. Test on devices
# (After initial development)
browser_navigate --url "http://localhost:19006"  # Expo web
browser_take_screenshot --filename "mobile-preview"
```

## Advanced Features

### Custom CLAUDE.md Configuration

Create a `CLAUDE.md` file in your project root for custom behavior:

```markdown
# Project: E-commerce Platform

## Project Type
web-application

## Technologies
- React 18
- Node.js
- PostgreSQL
- Redis
- Docker

## Architecture Preferences
- Microservices architecture
- Event-driven communication
- CQRS pattern for complex domains

## Development Preferences
- TypeScript for all code
- Test-driven development
- Comprehensive error handling
- Performance monitoring

## Security Requirements
- OWASP compliance
- Input validation
- SQL injection prevention
- XSS protection

## Performance Requirements
- < 2s page load time
- 99.9% uptime
- Horizontal scaling support

## Testing Strategy
- Unit tests (Jest)
- Integration tests (Supertest)
- E2E tests (Playwright)
- Performance tests (k6)

## Deployment
- Docker containers
- Kubernetes orchestration
- Blue-green deployment
- Automated rollback
```

### Memory Management

The system automatically manages context and memory:

```bash
# Create persistent memories
create_memory --title "Database Schema" --content "User table: id, email, password_hash, created_at, updated_at" --category "database"

# Search memories by context
search_memories --query "authentication implementation" --category "security"

# Update existing memories
update_memory --id "mem_123" --content "Updated user schema with profile fields"
```

### Tool Coordination

Multiple tools can work together seamlessly:

```bash
# 1. Research with Perplexity
perplexity_search_web "PostgreSQL indexing strategies for large datasets"

# 2. Get technical docs with Context7
get_library_docs "/postgresql/postgresql" --topic "indexing performance"

# 3. Analyze with Sequential Thinking
sequentialthinking "Design an optimal indexing strategy for a user table with 10M records"

# 4. Save insights to memory
create_memory --title "Indexing Strategy" --content "Composite index on (email, created_at) for login queries"

# 5. Create implementation task
create_task --title "Optimize database indexes" --description "Implement indexing strategy for performance"
```

## Monitoring and Troubleshooting

### System Health Monitoring

```bash
# Check system status
./scripts/health-check.sh

# Monitor active processes
list_processes

# Check MCP server status
claude mcp status

# View system logs
tail -f ~/.config/claude/claude.log
```

### Performance Optimization

```bash
# Monitor memory usage
get_memory_usage

# Check task performance
list_tasks --status "in-progress" --includeCompleted false

# Optimize tool usage
analyze_tool_performance
```

### Common Issues and Solutions

#### 1. Slow Response Times
```bash
# Check concurrent agent limit
echo $MAX_CONCURRENT_AGENTS

# Reduce parallel tasks
export MAX_CONCURRENT_AGENTS=3

# Clear memory cache
clear_memory_cache
```

#### 2. API Rate Limits
```bash
# Check API usage
check_api_limits

# Implement backoff strategy
export API_RETRY_DELAY=2000

# Use alternative providers
switch_to_backup_provider
```

#### 3. Tool Integration Issues
```bash
# Restart MCP servers
claude mcp restart-all

# Verify tool configuration
check_tool_config --tool "perplexity"

# Test individual tools
test_tool_integration --tool "github"
```

## Best Practices

### 1. Project Organization
- Use descriptive project names
- Maintain consistent directory structures
- Document architectural decisions in CLAUDE.md
- Use version control from the beginning

### 2. Task Management
- Break large tasks into smaller subtasks
- Use descriptive task titles and descriptions
- Set realistic deadlines and priorities
- Track progress with regular updates

### 3. Tool Usage
- Use the right tool for each task
- Combine tools for complex operations
- Monitor tool performance and usage
- Keep tool configurations updated

### 4. Code Quality
- Follow established coding standards
- Implement comprehensive testing
- Use automated code analysis
- Regular security scans

### 5. Performance
- Monitor resource usage
- Optimize memory management
- Use caching where appropriate
- Regular performance testing

## Next Steps

- Explore [Workflow Documentation](workflows/) for specific use cases
- Review [Tool Documentation](tools/) for detailed tool guides
- Check [Troubleshooting Guide](troubleshooting/) for common issues
- Join the community for support and updates

The autonomous development system is designed to grow with your needs and continuously improve your development workflow. Happy coding! 🚀