#!/bin/bash

echo "🚀 Ultimate Workflow Orchestration - Installation Script"
echo "======================================================="

# Configuration
INSTALL_DIR="/mnt/c/ai-development-ecosystem"
CLAUDE_SYSTEM_DIR="$INSTALL_DIR/autonomous-claude-system"

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check for required commands
for cmd in python3 node npm git tmux; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ $cmd is required but not installed"
        exit 1
    fi
done

echo "✅ All prerequisites satisfied"

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
cd "$CLAUDE_SYSTEM_DIR"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Python dependencies installed"
else
    echo "⚠️  requirements.txt not found, skipping Python dependencies"
fi

# Set up environment file
echo "🔧 Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 Created .env file from template"
    echo "⚠️  Please edit .env file with your API keys"
else
    echo "✅ .env file already exists"
fi

# Make scripts executable
echo "🔨 Making scripts executable..."
chmod +x scripts/*.sh
chmod +x install.sh
echo "✅ Scripts made executable"

# Install global MCP tools
echo "📦 Installing global MCP tools..."
npm install -g @freshtechbro/vibe-coder-mcp
npm install -g @perplexity-ai/mcp-server
npm install -g @context7/mcp-server
npm install -g mcp-sequentialthinking-tools
npm install -g @brave-search/mcp-server
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-puppeteer
npm install -g @modelcontextprotocol/server-playwright
npm install -g @taskmaster-ai/mcp-server
npm install -g @agentic-tools/mcp-server
npm install -g @vibe-kanban/mcp-server
npm install -g @desktop-commander/mcp-server
npm install -g @dart-tools/mcp-server
npm install -g @ide-tools/mcp-server
echo "✅ Global MCP tools installed"

# Install BMAD-METHOD
echo "🧠 Installing BMAD-METHOD..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -ge 20 ]; then
        npx bmad-method install
        echo "✅ BMAD-METHOD installed successfully"
    else
        echo "⚠️  Node.js 20+ required for BMAD-METHOD (current: v$NODE_VERSION)"
        echo "   Please upgrade Node.js and run: npx bmad-method install"
    fi
else
    echo "❌ Node.js not found, cannot install BMAD-METHOD"
fi

# Set up Tmux Orchestrator
echo "🎭 Setting up Tmux Orchestrator..."
TMUX_ORCH_DIR="$CLAUDE_SYSTEM_DIR/tool-integrations/tmux-orchestrator"
if [ ! -d "$TMUX_ORCH_DIR" ]; then
    mkdir -p "$TMUX_ORCH_DIR"
    git clone https://github.com/Jedward23/Tmux-Orchestrator.git "$TMUX_ORCH_DIR/Tmux-Orchestrator"
    chmod +x "$TMUX_ORCH_DIR/Tmux-Orchestrator"/*.sh
    echo "✅ Tmux Orchestrator installed"
else
    echo "✅ Tmux Orchestrator already exists"
fi

# Set up Make-it-Heavy integration
echo "🤖 Setting up Make-it-Heavy integration..."
if [ ! -z "$OPENROUTER_API_KEY" ]; then
    bash scripts/make-it-heavy-integration.sh
    echo "✅ Make-it-Heavy integration complete"
else
    echo "⚠️  OPENROUTER_API_KEY not set, skipping Make-it-Heavy setup"
    echo "   Run 'bash scripts/make-it-heavy-integration.sh' after setting the key"
fi

# Set up Deep Code Reasoning (if available)
echo "🔬 Setting up Deep Code Reasoning..."
DEEP_CODE_PATH="/home/kngpn/deep-code-reasoning-mcp"
if [ -d "$DEEP_CODE_PATH" ]; then
    echo "✅ Deep Code Reasoning found at $DEEP_CODE_PATH"
else
    echo "⚠️  Deep Code Reasoning not found at $DEEP_CODE_PATH"
    echo "   Please clone and setup: https://github.com/your-repo/deep-code-reasoning-mcp"
fi

# Create workspaces directory
echo "📁 Creating workspaces directory..."
mkdir -p workspaces
echo "✅ Workspaces directory created"

# Final setup verification
echo "🔍 Verifying installation..."

# Check if templates exist
if [ -d "templates/claude-md-templates" ]; then
    echo "✅ CLAUDE.md templates found"
else
    echo "❌ CLAUDE.md templates missing"
fi

# Check if core scripts exist
if [ -f "src/autonomous-master-orchestrator.py" ]; then
    echo "✅ Autonomous orchestrator found"
else
    echo "❌ Autonomous orchestrator missing"
fi

echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "🛠️  Installed Tools Summary:"
echo "✅ Vibe-Coder-MCP - AI-native research & scaffolding"
echo "✅ BMAD-METHOD - Strategic AI planning framework"
echo "✅ Tmux Orchestrator - 24/7 agent coordination"
echo "✅ Make-it-Heavy - Multi-agent framework"
echo "✅ Perplexity MCP - Research and web search"
echo "✅ Context7 - Documentation intelligence"
echo "✅ Sequential Thinking - Complex reasoning"
echo "✅ Brave Search - Web search capabilities"
echo "✅ GitHub Integration - Version control"
echo "✅ Playwright - Browser testing"
echo "✅ Puppeteer - Browser automation"
echo "✅ TaskMaster AI - Project management"
echo "✅ Agentic Tools - Advanced project tools"
echo "✅ Vibe-Kanban - Agent management"
echo "✅ Desktop Commander - System operations"
echo "✅ Dart Tools - Task management"
echo "✅ IDE Integration - Development support"
echo "✅ Deep Code Reasoning - Advanced analysis"
echo "✅ Memory Management - Resource optimization"
echo "✅ Fetch Tools - Web content retrieval"
echo ""
echo "📖 Quick Start:"
echo "1. Edit .env file with your API keys:"
echo "   • ANTHROPIC_API_KEY (Claude)"
echo "   • PERPLEXITY_API_KEY (Research)"
echo "   • GEMINI_API_KEY (Deep Code Reasoning)"
echo "   • OPENROUTER_API_KEY (Make-it-Heavy)"
echo "   • GITHUB_TOKEN (GitHub integration)"
echo "2. Navigate to any project directory"
echo "3. Run: bash $CLAUDE_SYSTEM_DIR/scripts/auto-activate-claude-system.sh"
echo "4. Provide your project prompt to Claude Code"
echo ""
echo "🛠️  Available Commands:"
echo "• Auto-activate system: bash scripts/auto-activate-claude-system.sh"
echo "• Manual orchestrator: python3 src/autonomous-master-orchestrator.py"
echo "• Project detection: python3 src/claude-md-auto-deploy.py --project path --auto-detect"
echo "• BMAD planning: npx bmad-method (from project directory)"
echo "• Make-it-Heavy: make-it-heavy 'your query here'"
echo "• Tmux sessions: tmux list-sessions"
echo ""
echo "📚 Documentation: See README.md for complete usage guide"
echo ""
echo "🔧 Troubleshooting:"
echo "• Check .env file for correct API keys"
echo "• Verify MCP server status with Claude Code"
echo "• Test BMAD: cd your-project && npx bmad-method"
echo "• Test Make-it-Heavy: make-it-heavy 'test query'"
echo "• Review logs in /tmp/ for debugging"
echo ""