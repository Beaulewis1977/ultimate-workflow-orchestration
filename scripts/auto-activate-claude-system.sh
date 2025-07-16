#!/bin/bash

# 🤖 AUTO-ACTIVATE CLAUDE SYSTEM
# Automatically detects project type and activates the autonomous development system
# Place this in your shell profile or run manually when entering any directory

echo "🤖 Autonomous AI Development System - Auto Activation"
echo "=================================================="

# Get current directory
CURRENT_DIR="$(pwd)"
echo "📁 Analyzing directory: $CURRENT_DIR"

# Check if CLAUDE.md already exists
if [ -f "$CURRENT_DIR/CLAUDE.md" ]; then
    echo "✅ CLAUDE.md already exists - system is active"
    echo "💡 You can now provide prompts for autonomous development"
    exit 0
fi

# Run auto-deployment system
echo "🔍 Detecting project type..."
python3 /mnt/c/ai-development-ecosystem/autonomous-claude-system/src/claude-md-auto-deploy.py --project "$CURRENT_DIR" --auto-detect

# Check if deployment was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Autonomous development system is now active!"
    echo ""
    echo "📖 Quick Start:"
    echo "   • Provide your project prompt (e.g., 'Create a React e-commerce app')"
    echo "   • The system will handle everything autonomously"
    echo "   • All 20+ AI tools are now integrated and ready"
    echo ""
    echo "🛠️  Available Commands:"
    echo "   • python3 /mnt/c/ai-development-ecosystem/autonomous-claude-system/src/autonomous-master-orchestrator.py"
    echo "   • make-it-heavy 'your analysis request'"
    echo "   • View CLAUDE.md for complete instructions"
    echo ""
else
    echo "❌ Auto-deployment failed. Check logs for details."
    exit 1
fi