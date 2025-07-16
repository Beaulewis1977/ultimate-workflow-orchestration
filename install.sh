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
npm install -g @perplexity-ai/mcp-server
npm install -g @context7/mcp-server
npm install -g mcp-sequentialthinking-tools
npm install -g @brave-search/mcp-server
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-puppeteer
npm install -g @modelcontextprotocol/server-playwright
echo "✅ Global MCP tools installed"

# Set up Make-it-Heavy integration
echo "🤖 Setting up Make-it-Heavy integration..."
if [ ! -z "$OPENROUTER_API_KEY" ]; then
    bash scripts/make-it-heavy-integration.sh
    echo "✅ Make-it-Heavy integration complete"
else
    echo "⚠️  OPENROUTER_API_KEY not set, skipping Make-it-Heavy setup"
    echo "   Run 'bash scripts/make-it-heavy-integration.sh' after setting the key"
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
echo "📖 Quick Start:"
echo "1. Edit .env file with your API keys"
echo "2. Navigate to any project directory"
echo "3. Run: bash $CLAUDE_SYSTEM_DIR/scripts/auto-activate-claude-system.sh"
echo "4. Provide your project prompt to Claude Code"
echo ""
echo "🛠️  Available Commands:"
echo "• Auto-activate system: bash scripts/auto-activate-claude-system.sh"
echo "• Manual orchestrator: python3 src/autonomous-master-orchestrator.py"
echo "• Project detection: python3 src/claude-md-auto-deploy.py --project path --auto-detect"
echo ""
echo "📚 Documentation: See README.md for complete usage guide"
echo ""
echo "🔧 Troubleshooting:"
echo "• Check .env file for correct API keys"
echo "• Verify MCP server status with Claude Code"
echo "• Review logs in /tmp/ for debugging"
echo ""