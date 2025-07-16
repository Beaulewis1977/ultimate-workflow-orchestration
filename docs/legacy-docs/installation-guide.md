# Installation and Setup Guide

## Prerequisites

### System Requirements

#### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS (10.15+), or Windows with WSL2
- **CPU**: 4 cores
- **Memory**: 8GB RAM
- **Storage**: 100GB available space
- **Network**: Stable internet connection

#### Recommended Requirements
- **OS**: Linux (Ubuntu 22.04+) or macOS (12.0+)
- **CPU**: 8 cores
- **Memory**: 16GB RAM
- **Storage**: 500GB SSD
- **Network**: High-speed internet (100Mbps+)

### Required Software

#### Core Dependencies
```bash
# Node.js (v18+ recommended)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python (3.9+ required)
sudo apt-get install python3 python3-pip python3-venv

# Git
sudo apt-get install git

# Docker (for containerized deployments)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Claude Code CLI
```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-cli

# Verify installation
claude --version
```

## Installation Steps

### 1. Clone the Repository
```bash
# Clone the main repository
git clone https://github.com/your-org/autonomous-dev-system.git
cd autonomous-dev-system

# Set up workspace directory
export BMAD_WORKSPACE="/mnt/c/bmad-workspace"
mkdir -p "$BMAD_WORKSPACE"
cd "$BMAD_WORKSPACE"
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

#### Required Environment Variables
```bash
# AI Service API Keys
OPENAI_API_KEY="sk-your-openai-key"
ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
PERPLEXITY_API_KEY="pplx-your-perplexity-key"

# Development Tools
GITHUB_TOKEN="ghp_your-github-token"
DOCKER_USERNAME="your-docker-username"
DOCKER_PASSWORD="your-docker-password"

# System Configuration
DEBUG_MODE="false"
LOG_LEVEL="info"
MEMORY_LIMIT="8GB"
MAX_CONCURRENT_AGENTS="5"

# Database Configuration (if using)
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
REDIS_URL="redis://localhost:6379"

# Cloud Provider Credentials (optional)
AWS_ACCESS_KEY_ID="your-aws-key"
AWS_SECRET_ACCESS_KEY="your-aws-secret"
AZURE_CLIENT_ID="your-azure-client-id"
AZURE_CLIENT_SECRET="your-azure-secret"
GCP_PROJECT_ID="your-gcp-project"
```

### 3. MCP Server Installation

#### Install Core MCP Servers
```bash
# Create MCP servers directory
mkdir -p ~/.mcp-servers

# Install TaskMaster AI
npm install -g @taskmaster/mcp-server

# Install Perplexity MCP
npm install -g @perplexity/mcp-server

# Install Context7
npm install -g @context7/mcp-server

# Install Deep Code Reasoning
npm install -g @deepcode/mcp-server

# Install Agentic Tools
npm install -g @agentic/mcp-server

# Install GitHub MCP
npm install -g @github/mcp-server

# Install Desktop Commander
npm install -g @desktop/commander-mcp

# Install Playwright MCP
npm install -g @playwright/mcp-server

# Install Dart (Kanban) MCP
npm install -g @dart/mcp-server

# Install Vibe Kanban MCP
npm install -g @vibe/kanban-mcp

# Install Make-it-Heavy MCP
npm install -g @makeiteavy/mcp-server

# Install Sequential Thinking MCP
npm install -g @sequential/thinking-mcp

# Install Consult7 MCP
npm install -g @consult7/mcp-server

# Install Fetch MCP
npm install -g @fetch/mcp-server

# Install Brave Search MCP
npm install -g @brave/search-mcp

# Install Everything MCP (utilities)
npm install -g @everything/mcp-server

# Install IDE Integration MCP
npm install -g @ide/integration-mcp

# Install MCP Installer
npm install -g @mcp/installer-server
```

### 4. Claude Code Configuration

#### Create Claude Configuration
```bash
# Create Claude config directory
mkdir -p ~/.config/claude

# Create main configuration file
cat > ~/.config/claude/config.json << 'EOF'
{
  "mcp": {
    "servers": {
      "taskmaster-ai": {
        "command": "taskmaster-mcp-server",
        "args": [],
        "env": {
          "TASKMASTER_API_KEY": "${TASKMASTER_API_KEY}"
        }
      },
      "perplexity-mcp": {
        "command": "perplexity-mcp-server",
        "args": [],
        "env": {
          "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
        }
      },
      "context7": {
        "command": "context7-mcp-server",
        "args": [],
        "env": {
          "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
        }
      },
      "deep-code-reasoning": {
        "command": "deep-code-reasoning-mcp-server",
        "args": []
      },
      "agentic-tools": {
        "command": "agentic-tools-mcp-server",
        "args": []
      },
      "github": {
        "command": "github-mcp-server",
        "args": [],
        "env": {
          "GITHUB_TOKEN": "${GITHUB_TOKEN}"
        }
      },
      "desktop-commander": {
        "command": "desktop-commander-mcp-server",
        "args": []
      },
      "playwright": {
        "command": "playwright-mcp-server",
        "args": []
      },
      "dart": {
        "command": "dart-mcp-server",
        "args": [],
        "env": {
          "DART_API_KEY": "${DART_API_KEY}"
        }
      },
      "vibe-kanban": {
        "command": "vibe-kanban-mcp-server",
        "args": []
      },
      "make-it-heavy": {
        "command": "make-it-heavy-mcp-server",
        "args": []
      },
      "sequential-thinking": {
        "command": "sequential-thinking-mcp-server",
        "args": []
      },
      "consult7": {
        "command": "consult7-mcp-server",
        "args": []
      },
      "fetch": {
        "command": "fetch-mcp-server",
        "args": []
      },
      "brave-search": {
        "command": "brave-search-mcp-server",
        "args": [],
        "env": {
          "BRAVE_API_KEY": "${BRAVE_API_KEY}"
        }
      },
      "everything": {
        "command": "everything-mcp-server",
        "args": []
      },
      "ide": {
        "command": "ide-integration-mcp-server",
        "args": []
      },
      "mcp-installer": {
        "command": "mcp-installer-server",
        "args": []
      }
    }
  },
  "logging": {
    "level": "info",
    "file": "~/.config/claude/claude.log"
  },
  "features": {
    "auto_memory_management": true,
    "tool_integration": true,
    "project_detection": true
  }
}
EOF
```

### 5. System Initialization

#### Make Scripts Executable
```bash
# Navigate to workspace
cd "$BMAD_WORKSPACE"

# Make all shell scripts executable
find . -name "*.sh" -type f -exec chmod +x {} \;

# Verify key scripts
ls -la *.sh
```

#### Initialize System Components
```bash
# Initialize Tmux Orchestrator
cd Tmux-Orchestrator
./setup.sh

# Return to workspace root
cd "$BMAD_WORKSPACE"

# Test orchestrator
./ultimate-ai-orchestrator.sh test-project genesis --dry-run
```

### 6. Database Setup (Optional)

#### PostgreSQL Setup
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql << 'EOF'
CREATE DATABASE autonomous_dev;
CREATE USER dev_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE autonomous_dev TO dev_user;
\q
EOF

# Update connection string in .env
echo 'DATABASE_URL="postgresql://dev_user:secure_password@localhost:5432/autonomous_dev"' >> .env
```

#### Redis Setup
```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis service
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test Redis connection
redis-cli ping
```

### 7. Testing Installation

#### Verify Core Components
```bash
# Test Claude Code installation
claude --version

# Test MCP servers
claude mcp list-servers

# Test environment variables
claude code --test-environment

# Test system dependencies
./scripts/verify-installation.sh
```

#### Run Basic Test
```bash
# Create a test project
./ultimate-ai-orchestrator.sh installation-test genesis

# Verify project creation
ls -la projects/installation-test/

# Check logs for errors
tail -f projects/installation-test/orchestrator.log
```

## Configuration Verification

### Health Check Script
```bash
#!/bin/bash
# Create health check script

cat > scripts/health-check.sh << 'EOF'
#!/bin/bash

echo "🔍 Autonomous Development System Health Check"
echo "============================================="

# Check Claude Code
echo -n "Claude Code: "
if command -v claude &> /dev/null; then
    echo "✅ Installed ($(claude --version))"
else
    echo "❌ Not found"
fi

# Check Node.js
echo -n "Node.js: "
if command -v node &> /dev/null; then
    echo "✅ Installed ($(node --version))"
else
    echo "❌ Not found"
fi

# Check Python
echo -n "Python: "
if command -v python3 &> /dev/null; then
    echo "✅ Installed ($(python3 --version))"
else
    echo "❌ Not found"
fi

# Check Docker
echo -n "Docker: "
if command -v docker &> /dev/null; then
    echo "✅ Installed ($(docker --version | cut -d' ' -f3 | cut -d',' -f1))"
else
    echo "❌ Not found"
fi

# Check environment variables
echo ""
echo "Environment Variables:"
echo -n "ANTHROPIC_API_KEY: "
[ -n "$ANTHROPIC_API_KEY" ] && echo "✅ Set" || echo "❌ Missing"

echo -n "OPENAI_API_KEY: "
[ -n "$OPENAI_API_KEY" ] && echo "✅ Set" || echo "❌ Missing"

echo -n "PERPLEXITY_API_KEY: "
[ -n "$PERPLEXITY_API_KEY" ] && echo "✅ Set" || echo "❌ Missing"

echo -n "GITHUB_TOKEN: "
[ -n "$GITHUB_TOKEN" ] && echo "✅ Set" || echo "❌ Missing"

# Check MCP servers
echo ""
echo "MCP Servers:"
claude mcp list-servers 2>/dev/null | while read -r server; do
    echo "✅ $server"
done

echo ""
echo "System ready for autonomous development! 🚀"
EOF

chmod +x scripts/health-check.sh
```

### Run Health Check
```bash
./scripts/health-check.sh
```

## Troubleshooting Installation

### Common Issues

#### 1. Permission Denied Errors
```bash
# Fix script permissions
find . -name "*.sh" -exec chmod +x {} \;

# Fix directory permissions
chmod -R 755 scripts/
```

#### 2. Missing Dependencies
```bash
# Update package lists
sudo apt-get update

# Install missing packages
sudo apt-get install -y curl wget unzip jq
```

#### 3. API Key Issues
```bash
# Verify API keys are set
echo $ANTHROPIC_API_KEY | cut -c1-10

# Test API connectivity
curl -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.anthropic.com/v1/messages
```

#### 4. MCP Server Connection Issues
```bash
# Check MCP server status
claude mcp status

# Restart MCP servers
claude mcp restart-all

# Check logs
tail -f ~/.config/claude/claude.log
```

### Advanced Configuration

#### Custom Tool Integration
```bash
# Add custom MCP server
mkdir -p ~/.mcp-servers/custom

# Create custom server configuration
cat > ~/.mcp-servers/custom/config.json << 'EOF'
{
  "name": "custom-tool",
  "version": "1.0.0",
  "description": "Custom tool integration",
  "main": "./server.js",
  "dependencies": {}
}
EOF
```

#### Performance Tuning
```bash
# Increase memory limits
export NODE_OPTIONS="--max-old-space-size=8192"

# Configure concurrent limits
echo 'MAX_CONCURRENT_AGENTS="10"' >> .env

# Enable high-performance mode
echo 'PERFORMANCE_MODE="high"' >> .env
```

## Next Steps

After successful installation:

1. **Read the User Guide**: [user-guide.md](user-guide.md)
2. **Explore Workflows**: [workflows/](workflows/)
3. **Review Tool Documentation**: [tools/](tools/)
4. **Run Example Projects**: [guides/examples.md](guides/examples.md)

## Getting Help

If you encounter issues during installation:

1. Check the [Troubleshooting Guide](troubleshooting/)
2. Review logs in `~/.config/claude/claude.log`
3. Verify all prerequisites are met
4. Run the health check script
5. Submit detailed issue reports with logs and system information

The autonomous development system is now ready for use! 🎉