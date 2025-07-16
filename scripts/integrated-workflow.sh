#!/bin/bash

# Integrated Workflow: BMAD + Vibe-Coder + Tmux-Orchestrator
# This script demonstrates how to combine all three tools for autonomous development

set -e

PROJECT_NAME="ai-saas-platform"
WORKSPACE="/mnt/c/ai-development-ecosystem/autonomous-claude-system"
PROJECT_DIR="$WORKSPACE/projects/$PROJECT_NAME"
ORCHESTRATOR_DIR="$WORKSPACE/Tmux-Orchestrator"

echo "🚀 Starting Integrated AI Development Workflow"
echo "Project: $PROJECT_NAME"
echo "Workspace: $WORKSPACE"
echo ""

# Phase 1: Setup Project Structure
echo "📁 Phase 1: Setting up project structure..."
mkdir -p "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/docs"
mkdir -p "$PROJECT_DIR/src"
mkdir -p "$PROJECT_DIR/tests"

# Copy project specification
cp "$WORKSPACE/orchestrator-configs/sample-saas-project.md" "$PROJECT_DIR/project-spec.md"

echo "✅ Project structure created"
echo ""

# Phase 2: Initialize Git Repository
echo "📝 Phase 2: Initializing git repository..."
cd "$PROJECT_DIR"
git init
git add .
git commit -m "Initial project setup with BMAD + Orchestrator integration

🤖 Generated with integrated AI development workflow
- BMAD-METHOD for strategic planning
- Vibe-Coder-MCP for research and context
- Tmux-Orchestrator for autonomous execution

Co-Authored-By: Claude <noreply@anthropic.com>"

echo "✅ Git repository initialized"
echo ""

# Phase 3: Tmux Session Setup
echo "🖥️  Phase 3: Setting up tmux sessions for autonomous development..."

# Create main orchestrator session
tmux new-session -d -s "$PROJECT_NAME-orchestrator" -c "$PROJECT_DIR"
tmux send-keys -t "$PROJECT_NAME-orchestrator" "echo 'Orchestrator session started for $PROJECT_NAME'" Enter

# Create project manager session
tmux new-session -d -s "$PROJECT_NAME-pm" -c "$PROJECT_DIR"
tmux send-keys -t "$PROJECT_NAME-pm" "echo 'Project Manager session ready'" Enter

# Create development sessions
tmux new-session -d -s "$PROJECT_NAME-backend" -c "$PROJECT_DIR"
tmux send-keys -t "$PROJECT_NAME-backend" "echo 'Backend development session ready'" Enter

tmux new-session -d -s "$PROJECT_NAME-frontend" -c "$PROJECT_DIR"
tmux send-keys -t "$PROJECT_NAME-frontend" "echo 'Frontend development session ready'" Enter

tmux new-session -d -s "$PROJECT_NAME-qa" -c "$PROJECT_DIR"
tmux send-keys -t "$PROJECT_NAME-qa" "echo 'QA and testing session ready'" Enter

echo "✅ Tmux sessions created:"
tmux list-sessions | grep "$PROJECT_NAME"
echo ""

# Phase 4: Create Integration Instructions
echo "📋 Phase 4: Creating integration instructions..."

cat > "$PROJECT_DIR/autonomous-workflow.md" << 'EOF'
# Autonomous Development Workflow

## How to Use This Integrated Setup

### 1. Research Phase (Vibe-Coder-MCP)
```bash
# Use Claude Code with Vibe-Coder tools
research "SaaS architecture best practices 2024"
generate-prd "AI-powered task management platform"
curate-context "Gather implementation examples and patterns"
```

### 2. Planning Phase (BMAD-METHOD Agents)
```bash
# Use BMAD slash commands in Claude Code
/analyst "Analyze market for AI-powered SaaS platforms"
/pm "Create comprehensive project roadmap and sprint backlog"
/architect "Design scalable microservices architecture"
/ux-expert "Design modern, responsive user interface"
```

### 3. Autonomous Execution (Tmux-Orchestrator)
```bash
# Connect to orchestrator session
tmux attach-session -t ai-saas-platform-orchestrator

# In the orchestrator session, coordinate BMAD agents:
# "You are the Orchestrator. Coordinate the following BMAD agents across tmux sessions:
#  - Project Manager in session 'ai-saas-platform-pm' 
#  - Backend Developer in session 'ai-saas-platform-backend'
#  - Frontend Developer in session 'ai-saas-platform-frontend' 
#  - QA Engineer in session 'ai-saas-platform-qa'
#  
#  Use the project specification and coordinate autonomous development.
#  Schedule check-ins every 30 minutes and ensure regular git commits."
```

### 4. Monitoring and Control
```bash
# View all project sessions
tmux list-sessions | grep ai-saas-platform

# Attach to specific agent session
tmux attach-session -t ai-saas-platform-pm

# Send messages to agents
./Tmux-Orchestrator/send-claude-message.sh ai-saas-platform-pm "Status update request"

# Schedule automatic check-ins
./Tmux-Orchestrator/schedule_with_note.sh 30 "Check project progress"
```

### 5. Cross-Platform Access
- **WSL**: Monitor tmux sessions and agent activity
- **Windows**: Access files at `C:\bmad-workspace\projects\ai-saas-platform\`
- **Claude Code**: Use BMAD slash commands and Vibe-Coder tools
- **Git**: Track progress with automated commits every 30 minutes

## Agent Coordination Strategy

### Orchestrator Role
- Monitors overall project progress
- Coordinates between specialized agents
- Escalates complex decisions to human oversight
- Manages project timeline and deliverables

### BMAD Agent Specialization
- **Project Manager**: Sprint planning, task assignment, progress tracking
- **Backend Developer**: API development, database design, infrastructure
- **Frontend Developer**: UI/UX implementation, component development
- **QA Engineer**: Testing strategy, quality assurance, security validation

### Integration Benefits
- **24/7 Development**: Agents work continuously in persistent sessions
- **Research-Informed**: Decisions based on latest best practices
- **Quality-First**: Built-in testing and validation workflows
- **Human Oversight**: Regular check-ins and decision points
- **Cross-Platform**: Seamless access from Windows and WSL
EOF

echo "✅ Integration instructions created"
echo ""

# Phase 5: Summary and Next Steps
echo "🎉 Integration Setup Complete!"
echo ""
echo "📍 Your integrated AI development environment is ready:"
echo "   Project Location: $PROJECT_DIR"
echo "   Windows Access: C:\\bmad-workspace\\projects\\$PROJECT_NAME\\"
echo ""
echo "🔧 Available Tools:"
echo "   ✅ BMAD-METHOD agents via Claude Code slash commands"
echo "   ✅ Vibe-Coder-MCP research and context tools"
echo "   ✅ Tmux-Orchestrator autonomous execution"
echo ""
echo "📊 Active tmux sessions:"
tmux list-sessions | grep "$PROJECT_NAME" || echo "   (Run this script to see active sessions)"
echo ""
echo "🚀 Next Steps:"
echo "   1. Use Claude Code for research and planning:"
echo "      research \"SaaS development best practices\""
echo "      /analyst \"Market analysis for AI SaaS\""
echo ""
echo "   2. Start autonomous development:"
echo "      tmux attach-session -t $PROJECT_NAME-orchestrator"
echo ""
echo "   3. Monitor progress from Windows:"
echo "      Open C:\\bmad-workspace\\projects\\$PROJECT_NAME\\"
echo ""
echo "💡 The integrated workflow combines the best of all three tools:"
echo "   - Strategic AI agents (BMAD)"
echo "   - Deep research capabilities (Vibe-Coder)"  
echo "   - Autonomous 24/7 operation (Tmux-Orchestrator)"
echo ""
echo "Happy autonomous development! 🤖✨"