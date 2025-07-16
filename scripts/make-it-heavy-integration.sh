#!/bin/bash

echo "🚀 Make-It-Heavy Integration Setup"
echo "================================="

# Configuration
MAKE_IT_HEAVY_DIR="$HOME/.make-it-heavy"
OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-}"

# Check if OpenRouter API key exists
if [[ -z "$OPENROUTER_API_KEY" ]]; then
    echo "⚠️  OpenRouter API key not found. Please set OPENROUTER_API_KEY environment variable."
    echo "You can get one from: https://openrouter.ai/"
    exit 1
fi

echo "📦 Installing Make-It-Heavy..."

# Clone repository
if [[ ! -d "$MAKE_IT_HEAVY_DIR" ]]; then
    git clone https://github.com/Doriandarko/make-it-heavy.git "$MAKE_IT_HEAVY_DIR"
fi

cd "$MAKE_IT_HEAVY_DIR"

# Setup virtual environment
echo "🔧 Setting up virtual environment..."
uv venv
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
uv pip install -r requirements.txt

# Configure API key
echo "🔑 Configuring API key..."
sed -i.bak "s/YOUR API KEY HERE/$OPENROUTER_API_KEY/g" config.yaml

# Create global wrapper scripts
echo "🌐 Creating global wrapper scripts..."

# Single agent mode
sudo tee /usr/local/bin/make-it-heavy-single << 'EOF'
#!/bin/bash
cd ~/.make-it-heavy
source .venv/bin/activate
python main.py "$@"
EOF

# Multi-agent mode
sudo tee /usr/local/bin/make-it-heavy << 'EOF'
#!/bin/bash
cd ~/.make-it-heavy
source .venv/bin/activate
python make_it_heavy.py "$@"
EOF

# Make executable
sudo chmod +x /usr/local/bin/make-it-heavy-single
sudo chmod +x /usr/local/bin/make-it-heavy

# Create integration functions for existing scripts
echo "🔗 Creating integration functions..."

cat > "$MAKE_IT_HEAVY_DIR/integration-functions.sh" << 'EOF'
#!/bin/bash

# Integration function for ultimate-ai-orchestrator.sh
integrate_heavy_mode() {
    local query="$1"
    local context="$2"
    
    echo "🧠 Activating Heavy Mode Multi-Agent Analysis..."
    make-it-heavy "$query - Context: $context"
}

# Integration function for omniscient-coordinator.sh
omniscient_heavy_analysis() {
    local project_name="$1"
    local mode="$2"
    local query="$3"
    
    echo "🌟 Omniscient Heavy Mode Analysis for $project_name..."
    make-it-heavy "Project: $project_name, Mode: $mode, Query: $query"
}

# Integration with sequential thinking
sequential_heavy_combo() {
    local query="$1"
    
    echo "🤔 Sequential + Heavy Mode Analysis..."
    echo "Step 1: Sequential breakdown..."
    # This would typically call your sequential thinking tool
    
    echo "Step 2: Heavy mode validation..."
    make-it-heavy "$query - Please validate and enhance this analysis from multiple expert perspectives"
}

# Integration with research trinity
research_heavy_synthesis() {
    local research_topic="$1"
    
    echo "🔍 Research Trinity + Heavy Mode Synthesis..."
    # This would collect research from perplexity, context7, brave search
    
    echo "Synthesizing with Heavy Mode..."
    make-it-heavy "Synthesize research on $research_topic into comprehensive strategic recommendations"
}
EOF

source "$MAKE_IT_HEAVY_DIR/integration-functions.sh"

echo "✅ Make-It-Heavy integration complete!"
echo ""
echo "🎯 Usage Examples:"
echo "  make-it-heavy 'Analyze my React application architecture'"
echo "  make-it-heavy-single 'Research best practices for API design'"
echo "  integrate_heavy_mode 'Design user authentication' 'SaaS application'"
echo ""
echo "🔧 Integration functions available:"
echo "  - integrate_heavy_mode"
echo "  - omniscient_heavy_analysis"
echo "  - sequential_heavy_combo"
echo "  - research_heavy_synthesis"
echo ""
echo "💡 Add to your .bashrc or .zshrc:"
echo "  source ~/.make-it-heavy/integration-functions.sh"