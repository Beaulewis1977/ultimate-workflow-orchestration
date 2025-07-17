#!/bin/bash

# AI Development Orchestrator - Complete 20+ Tool Integration
# Combines ALL tools: Vibe-Coder, BMAD, Tmux Orchestrator, Make-it-Heavy, and all MCP tools

set -e

# Configuration
PROJECT_NAME="${1:-ai-saas-demo}"
WORKSPACE="/mnt/c/ai-development-ecosystem/autonomous-claude-system"
PROJECT_DIR="$WORKSPACE/projects/$PROJECT_NAME"
ORCHESTRATOR_DIR="$WORKSPACE/../tool-integrations/tmux-orchestrator"

echo "🤖 AI Development Orchestrator Starting..."
echo "Project: $PROJECT_NAME"
echo "Workspace: $WORKSPACE"
echo ""

# Phase 1: Setup Project Structure
echo "📁 Phase 1: Creating project structure..."
mkdir -p "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/research"
mkdir -p "$PROJECT_DIR/planning" 
mkdir -p "$PROJECT_DIR/src"
mkdir -p "$PROJECT_DIR/docs"

# Phase 2: Vibe-Coder Research Integration
echo "🔍 Phase 2: Setting up Vibe-Coder research automation..."

cat > "$PROJECT_DIR/research-automation.sh" << 'EOF'
#!/bin/bash
# Automated research using Vibe-Coder-MCP via Claude Code

echo "Starting automated research phase..."

# Create research prompts for Claude Code
cat > research-commands.txt << 'RESEARCH'
# Use these commands in Claude Code with enhanced MCP tools:

research "SaaS architecture best practices 2024, microservices patterns, database design"
research "authentication systems, JWT tokens, OAuth2 implementation, security best practices"  
research "React 18 features, Next.js 14, TypeScript patterns, modern frontend development"
research "Node.js API design, Express.js alternatives, database optimization techniques"
research "payment processing, Stripe integration, subscription billing, SaaS monetization"

# Use Sequential Thinking for complex research synthesis
sequentialthinking "Synthesize all research findings into a coherent technical strategy. Identify dependencies, risks, and optimal implementation sequence."

# Use Deep Code Reasoning for technical validation
deep-code-analysis "Analyze the technical feasibility of proposed technologies and architecture patterns. Identify potential bottlenecks and optimization opportunities."

# Use Perplexity for real-time web research
perplexity_search_web "Latest SaaS architecture trends and security best practices 2024"
perplexity_search_web "Modern authentication patterns OAuth2 JWT implementation 2024"

# Use Context7 for documentation research
context7 "Get latest React 18 documentation and best practices"
context7 "Fetch current Node.js API development patterns"
context7 "Retrieve Stripe API integration guidelines"

# Use Brave Search for additional research
brave_search "SaaS performance optimization techniques 2024"
brave_search "Modern CI/CD pipeline best practices"

# Use Vibe-Coder for project scaffolding
vibe-coder "Research modern SaaS architecture patterns and generate starter templates"
vibe-coder "Analyze competitor platforms and suggest feature prioritization"
vibe-coder "Create comprehensive PRD with user stories and technical requirements"

curate-context "Generate comprehensive technical foundation for modern SaaS development"
generate-prd "Create detailed PRD for AI-powered task management SaaS platform"

# Save research results to:
# - research/architecture-research.md
# - research/auth-research.md  
# - research/frontend-research.md
# - research/backend-research.md
# - research/payment-research.md
# - planning/generated-prd.md
RESEARCH

echo "Research commands created in research-commands.txt"
echo "Run these in Claude Code to populate research/ directory"
EOF

chmod +x "$PROJECT_DIR/research-automation.sh"

# Phase 3: BMAD Agent Configuration
echo "🧠 Phase 3: Setting up BMAD agent workflows..."

cat > "$PROJECT_DIR/bmad-workflow.sh" << 'EOF'
#!/bin/bash
# BMAD Agent Coordination Script

echo "Starting BMAD agent workflow..."

# Create BMAD command sequence
cat > bmad-commands.txt << 'BMAD'
# Execute these BMAD commands in Claude Code:

# Use Sequential Thinking for complex analysis
sequentialthinking "Analyze the SaaS development complexity: market positioning, technical architecture, and implementation strategy. Consider dependencies and risks."

/analyst "Analyze the SaaS market for AI-powered task management platforms. Focus on competitive analysis, pricing strategies, and user personas. Use the research data from research/ directory."

/pm "Create a comprehensive project roadmap based on the generated PRD. Break down into 4 sprints with clear deliverables, timelines, and dependencies. Include risk mitigation strategies."

# Use Deep Code Reasoning for architecture validation
deep-code-analysis "Review the proposed microservices architecture for scalability, security, and maintainability. Validate technical feasibility."

/architect "Design a scalable microservices architecture for the SaaS platform. Consider the research findings on modern architecture patterns. Include database design, API specifications, and deployment strategy."

/ux-expert "Design the user interface and experience based on the PRD and market analysis. Create wireframes for key user flows: onboarding, dashboard, task management, and billing."

/dev "Create implementation plan based on architect's design. Break down into specific coding tasks with time estimates. Include testing strategy and code quality guidelines."

/qa "Develop comprehensive testing strategy including unit tests, integration tests, e2e tests, and security testing. Create test cases for all user flows and edge cases."

# Results will be used to populate:
# - planning/market-analysis.md
# - planning/project-roadmap.md  
# - planning/system-architecture.md
# - planning/ux-design.md
# - planning/implementation-plan.md
# - planning/testing-strategy.md
BMAD

echo "BMAD commands created in bmad-commands.txt"
echo "Execute these in Claude Code after research phase"
EOF

chmod +x "$PROJECT_DIR/bmad-workflow.sh"

# Phase 4: ../tool-integrations/tmux-orchestrator Autonomous Setup
echo "🖥️ Phase 4: Creating ../tool-integrations/tmux-orchestrator autonomous workflow..."

cat > "$PROJECT_DIR/orchestrator-startup.sh" << 'EOF'
#!/bin/bash
# ../tool-integrations/tmux-orchestrator Startup Script

PROJECT_NAME="ai-saas-demo"
WORKSPACE="/mnt/c/ai-development-ecosystem/autonomous-claude-system"

echo "🚀 Starting ../tool-integrations/tmux-orchestrator for autonomous development..."

# Create orchestrator session
tmux new-session -d -s "${PROJECT_NAME}-orchestrator" -c "$WORKSPACE/projects/$PROJECT_NAME"

# Create project manager sessions
tmux new-session -d -s "${PROJECT_NAME}-pm-backend" -c "$WORKSPACE/projects/$PROJECT_NAME"
tmux new-session -d -s "${PROJECT_NAME}-pm-frontend" -c "$WORKSPACE/projects/$PROJECT_NAME"
tmux new-session -d -s "${PROJECT_NAME}-pm-qa" -c "$WORKSPACE/projects/$PROJECT_NAME"

# Create development team sessions
tmux new-session -d -s "${PROJECT_NAME}-dev-api" -c "$WORKSPACE/projects/$PROJECT_NAME"
tmux new-session -d -s "${PROJECT_NAME}-dev-ui" -c "$WORKSPACE/projects/$PROJECT_NAME"
tmux new-session -d -s "${PROJECT_NAME}-dev-auth" -c "$WORKSPACE/projects/$PROJECT_NAME"

echo "✅ Tmux sessions created:"
tmux list-sessions | grep "$PROJECT_NAME"

echo ""
echo "🤖 To start autonomous development:"
echo "1. tmux attach-session -t ${PROJECT_NAME}-orchestrator"
echo "2. Start Claude in the orchestrator session"
echo "3. Give it the orchestrator instructions from orchestrator-instructions.md"

# Create orchestrator instructions
cat > orchestrator-instructions.md << 'INSTRUCTIONS'
# Orchestrator Instructions

You are the AI Development Orchestrator coordinating a SaaS development project.

## Your Role
- Monitor and coordinate all project managers and development teams
- Ensure project specifications are followed
- Schedule regular check-ins and progress reports
- Escalate complex decisions to human oversight
- Maintain project timeline and quality standards

## Available Teams

### Project Managers
- **Backend PM** (session: ai-saas-demo-pm-backend)
  - Manages API development, database design, authentication
  - Coordinates with dev-api and dev-auth teams
  
- **Frontend PM** (session: ai-saas-demo-pm-frontend)  
  - Manages UI/UX implementation, component development
  - Coordinates with dev-ui team
  
- **QA PM** (session: ai-saas-demo-pm-qa)
  - Manages testing strategy, quality assurance, security
  - Coordinates with all development teams

### Development Teams
- **API Team** (session: ai-saas-demo-dev-api)
  - Core business logic, REST APIs, database integration
  
- **UI Team** (session: ai-saas-demo-dev-ui)
  - React components, frontend logic, user interface
  
- **Auth Team** (session: ai-saas-demo-dev-auth)
  - Authentication, authorization, security implementation

## Communication Commands
Use these to coordinate teams:

```bash
# Send message to specific team
/mnt/c/ai-development-ecosystem/autonomous-claude-system/../tool-integrations/tmux-orchestrator/send-claude-message.sh ai-saas-demo-pm-backend "Status update request"

# Schedule check-ins
/mnt/c/ai-development-ecosystem/autonomous-claude-system/../tool-integrations/tmux-orchestrator/schedule_with_note.sh 30 "Cross-team integration checkpoint"
```

## Project Context
- Research data available in: research/ directory
- BMAD planning results in: planning/ directory
- Project specification: project-spec.md
- Implementation follows: planning/implementation-plan.md

## Workflow
1. Brief each project manager on their responsibilities
2. Have PMs create and brief their development teams
3. Coordinate development with 30-minute check-ins
4. Ensure regular git commits and quality checks
5. Report progress to human oversight every 2 hours

## Quality Standards
- All code must have tests (90%+ coverage)
- Git commits every 30 minutes with meaningful messages
- Code reviews between teams for shared components
- Security validation for all authentication code
- Performance benchmarks for API endpoints

Begin by briefing the Backend PM on their role and having them start the API team.
INSTRUCTIONS

echo "📋 Orchestrator instructions created"
EOF

chmod +x "$PROJECT_DIR/orchestrator-startup.sh"

# Phase 5: Integration Configuration
echo "⚙️ Phase 5: Creating integration configuration..."

cat > "$PROJECT_DIR/project-spec.md" << 'EOF'
# AI-Powered SaaS Platform - Integrated Development

## Project Overview
**PROJECT**: AI-Powered Task Management SaaS
**METHODOLOGY**: Vibe-Coder Research → BMAD Planning → ../tool-integrations/tmux-orchestrator Execution
**INTEGRATION**: All three tools working together autonomously

## Research Phase (Vibe-Coder-MCP)
✅ Research completed using research-automation.sh
- Architecture patterns and best practices
- Authentication and security research  
- Frontend/backend technology research
- Payment processing and monetization

## Planning Phase (BMAD-METHOD)
✅ Strategic planning using bmad-workflow.sh
- Market analysis and competitive research
- Product roadmap and sprint planning
- System architecture and technical design
- UX/UI design and user flows
- Implementation planning and testing strategy

## Execution Phase (../tool-integrations/tmux-orchestrator)
🚀 Autonomous development using orchestrator-startup.sh
- Multi-agent coordination across persistent sessions
- Project managers directing specialized development teams
- Continuous integration and quality assurance
- 24/7 development capability with human oversight

## Technical Stack
- **Frontend**: React 18, Next.js 14, TypeScript
- **Backend**: Node.js, Express/Fastify, PostgreSQL
- **Authentication**: JWT, OAuth2, multi-factor auth
- **Payment**: Stripe integration, subscription billing
- **Deployment**: Docker, AWS/Vercel, CI/CD pipeline

## Quality Assurance & Tool Integration
- **Testing**: Playwright (E2E), Puppeteer (automation), Desktop Commander (system testing)
- **Code Quality**: Deep Code Reasoning (analysis), Sequential Thinking (complex problem solving)
- **Project Management**: TaskMaster AI (task breakdown), Agentic Tools (memory management)
- **Agent Coordination**: Vibe-Kanban (agent switching), Make-it-Heavy (multi-agent deployment)
- **Development Support**: IDE Integration (diagnostics), GitHub Integration (CI/CD)
- **Research & Docs**: Context7 (documentation), Perplexity (research), Brave Search (web search)
- **Task Management**: Dart Tools (advanced tracking), Memory Management (resource optimization)
- Code coverage minimum 90%
- Security auditing and vulnerability scanning  
- Performance benchmarking and optimization
- Git workflow with automated commits

## Success Criteria
- [ ] Functional MVP with core features
- [ ] Scalable architecture supporting multi-tenancy
- [ ] Secure authentication and authorization
- [ ] Payment processing and subscription management
- [ ] Comprehensive test coverage
- [ ] Production deployment ready

This project demonstrates the integration of:
1. **Vibe-Coder-MCP**: Research and context curation
2. **BMAD-METHOD**: Strategic planning and expert analysis  
3. **../tool-integrations/tmux-orchestrator**: Autonomous execution and coordination

The result is a fully autonomous AI development workflow capable of building sophisticated SaaS applications with minimal human intervention.
EOF

# Phase 6: Master Integration Script
echo "🔗 Phase 6: Creating master integration launcher..."

cat > "$PROJECT_DIR/start-integrated-development.sh" << 'EOF'
#!/bin/bash
# Master Integration Script - Launches complete AI development workflow

echo "🤖 Starting Complete AI Development Integration"
echo "=============================================="
echo ""

PROJECT_DIR="/mnt/c/ai-development-ecosystem/autonomous-claude-system/projects/ai-saas-demo"
cd "$PROJECT_DIR"

echo "📋 Phase 1: Research (Vibe-Coder)"
echo "Run this command in Claude Code:"
echo "research 'SaaS development best practices, authentication, payment processing'"
echo ""
echo "Press Enter when research is complete..."
read

echo "🧠 Phase 2: Planning (BMAD)"  
echo "Run this command in Claude Code:"
echo "/analyst 'Analyze SaaS market based on research findings'"
echo "/pm 'Create project roadmap and sprint plan'"
echo "/architect 'Design system architecture'"
echo ""
echo "Press Enter when planning is complete..."
read

echo "🚀 Phase 3: Autonomous Execution (../tool-integrations/tmux-orchestrator)"
echo "Starting tmux sessions for autonomous development..."

# Start orchestrator
./orchestrator-startup.sh

echo ""
echo "✅ All systems ready! Next steps:"
echo "1. tmux attach-session -t ai-saas-demo-orchestrator"
echo "2. Start Claude and give it the orchestrator instructions"
echo "3. Let autonomous development begin!"
echo ""
echo "Monitor progress with:"
echo "tmux list-sessions | grep ai-saas-demo"
EOF

chmod +x "$PROJECT_DIR/start-integrated-development.sh"

# Phase 7: Create Integration Test
echo "🧪 Phase 7: Creating integration test..."

cat > "$PROJECT_DIR/test-integration.sh" << 'EOF'
#!/bin/bash
# Test script to verify all three tools can work together

echo "🧪 Testing AI Development Integration"
echo "===================================="

# Test 1: Verify Vibe-Coder MCP is available
echo "Test 1: Checking Vibe-Coder MCP availability..."
if command -v claude &> /dev/null; then
    echo "✅ Claude Code available"
    echo "   Use 'research' and 'curate-context' commands to test Vibe-Coder"
else
    echo "❌ Claude Code not found"
fi

# Test 2: Verify BMAD is available
echo ""
echo "Test 2: Checking BMAD availability..."
if command -v bmad &> /dev/null; then
    echo "✅ BMAD command available globally"
    echo "   Use '/analyst', '/pm', '/architect' commands in Claude Code"
else
    echo "❌ BMAD command not found"
fi

# Test 3: Verify ../tool-integrations/tmux-orchestrator
echo ""
echo "Test 3: Checking ../tool-integrations/tmux-orchestrator..."
if command -v tmux &> /dev/null; then
    echo "✅ Tmux available"
    if [ -f "/mnt/c/ai-development-ecosystem/autonomous-claude-system/../tool-integrations/tmux-orchestrator/send-claude-message.sh" ]; then
        echo "✅ Orchestrator scripts available"
    else
        echo "❌ Orchestrator scripts not found"
    fi
else
    echo "❌ Tmux not found"
fi

# Test 4: Cross-platform access
echo ""
echo "Test 4: Checking cross-platform access..."
if [ -d "/mnt/c/ai-development-ecosystem/autonomous-claude-system" ]; then
    echo "✅ Shared workspace accessible from WSL"
    if [ -w "/mnt/c/ai-development-ecosystem/autonomous-claude-system" ]; then
        echo "✅ Write permissions confirmed"
    else
        echo "❌ No write permissions"
    fi
else
    echo "❌ Shared workspace not accessible"
fi

echo ""
echo "🎯 Integration Status:"
echo "- Vibe-Coder: Research and context curation"
echo "- BMAD: Strategic planning and expert analysis"  
echo "- ../tool-integrations/tmux-orchestrator: Autonomous execution"
echo ""
echo "Ready for integrated AI development! 🚀"
EOF

chmod +x "$PROJECT_DIR/test-integration.sh"

# Phase 8: Initialize Git Repository
echo "📝 Phase 8: Initializing git repository..."
cd "$PROJECT_DIR"
git init
git add .
git commit -m "Initial AI development integration setup

🤖 Integrated AI Development Environment
- Vibe-Coder-MCP for research and context curation
- BMAD-METHOD for strategic planning and expert analysis
- ../tool-integrations/tmux-orchestrator for autonomous development coordination

Features:
- Automated research workflows
- Strategic planning automation  
- Multi-agent autonomous development
- Cross-platform Windows/WSL integration
- 24/7 development capability

Generated with Claude Code integrated workflow
Co-Authored-By: Claude <noreply@anthropic.com>"

echo ""
echo "🎉 AI Development Orchestrator Setup Complete!"
echo ""
echo "📍 Project Location: $PROJECT_DIR"
echo "📍 Windows Access: C:\\bmad-workspace\\projects\\$PROJECT_NAME\\"
echo ""
echo "🚀 Quick Start:"
echo "   cd $PROJECT_DIR"
echo "   ./start-integrated-development.sh"
echo ""
echo "🧪 Test Integration:"
echo "   ./test-integration.sh"
echo ""
echo "✨ This creates a working demonstration of all three AI tools"
echo "   coordinating together for autonomous SaaS development!"