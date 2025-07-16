# Quick Reference Guide: Autonomous AI Development System

## 🚀 Essential Commands

### System Initialization
```bash
# Initialize new autonomous workspace
./initialize-workspace.sh

# Start autonomous development session
./start-autonomous-session.sh

# End development session with reporting
./end-autonomous-session.sh
```

### Project Management
```bash
# Create new SaaS project
./templates/saas-app-template.py --project-name="my-saas"

# Enhance existing application
./templates/existing-app-enhancement-template.py --project-path="/path/to/app"

# Start research and development project
./research-development-workflow.sh --project="innovation" --domain="ai"
```

### Tool Operations
```bash
# Test all tool connections
./test-tool-connections.sh

# Diagnose tool issues
./diagnose-tool-connections.sh

# Restart specific tool
./restart-tool.sh --tool="vibe_coder"
```

## 🔧 Core Tool Quick Reference

### Vibe-Coder (Project Management)
```python
# Create task
mcp__vibe_kanban__create_task(
    project_id="my-project",
    title="Feature Development",
    description="Implement new feature"
)

# Update task status
mcp__vibe_kanban__update_task(
    project_id="my-project",
    task_id="task-123",
    status="done"
)

# List project tasks
mcp__vibe_kanban__list_tasks(project_id="my-project")
```

### Deep Reasoning (Problem Solving)
```python
# Escalate complex analysis
mcp__deep_code_reasoning__escalate_analysis(
    analysis_type="execution_trace",
    claude_context={
        "stuck_description": "Complex algorithm optimization",
        "code_scope": {"files": ["src/algorithm.py"]}
    }
)

# Start reasoning conversation
mcp__deep_code_reasoning__start_conversation(
    claude_context=problem_context,
    analysis_type="hypothesis_test"
)

# Run hypothesis tournament
mcp__deep_code_reasoning__run_hypothesis_tournament(
    claude_context=complex_issue,
    issue="Performance bottleneck analysis"
)
```

### Sequential Thinking (Planning)
```python
# Start structured thinking process
mcp__sequential_thinking__sequentialthinking_tools(
    thought="Plan feature implementation strategy",
    total_thoughts=10,
    thought_number=1,
    next_thought_needed=True,
    current_step={
        "step_description": "Initial analysis and planning",
        "recommended_tools": [
            {
                "tool_name": "mcp__context7__resolve-library-id",
                "confidence": 0.9,
                "rationale": "Need technical documentation"
            }
        ]
    }
)
```

### Research Trinity (Information Gathering)
```python
# Perplexity research
mcp__perplexity_mcp__perplexity_search_web(
    query="modern web development best practices",
    recency="month"
)

# Context7 documentation
library_id = mcp__context7__resolve_library_id(libraryName="react")
docs = mcp__context7__get_library_docs(
    context7CompatibleLibraryID=library_id,
    topic="hooks"
)

# Brave Search
mcp__brave_search__brave_web_search(
    query="React 2025 trends",
    count=10
)
```

### Context7 (Documentation)
```python
# Resolve library documentation
mcp__context7__resolve_library_id(libraryName="nextjs")

# Get specific documentation
mcp__context7__get_library_docs(
    context7CompatibleLibraryID="/vercel/next.js",
    topic="routing",
    tokens=10000
)
```

## 🔄 Workflow Patterns

### Standard Development Workflow
```yaml
1. Research Phase:
   - Use Research Trinity for domain knowledge
   - Context7 for technical documentation
   - Sequential Thinking for planning

2. Development Phase:
   - BMAD lifecycle implementation
   - Continuous quality monitoring
   - Automated testing and validation

3. Validation Phase:
   - Quality gate evaluation
   - Heavy mode validation (if critical)
   - Security and performance testing

4. Deployment Phase:
   - Automated deployment pipeline
   - Monitoring and alerting setup
   - Post-deployment validation
```

### Emergency Response Workflow
```yaml
1. Issue Detection:
   - Automated monitoring alerts
   - Quality gate failures
   - Performance degradation

2. Immediate Response:
   - Stop autonomous processes
   - Save current state
   - Assess damage level

3. Recovery Actions:
   - Rollback to stable state
   - Fix identified issues
   - Validate recovery

4. Post-Incident:
   - Generate incident report
   - Update prevention measures
   - Learn from incident
```

## ⚙️ Configuration Quick Reference

### Essential Environment Variables
```bash
# Core API Keys
export ANTHROPIC_API_KEY="your_anthropic_key"
export PERPLEXITY_API_KEY="your_perplexity_key"
export BRAVE_API_KEY="your_brave_search_key"
export VIBE_KANBAN_TOKEN="your_vibe_token"

# System Configuration
export BMAD_ENVIRONMENT="production"
export AUTONOMY_LEVEL="supervised"
export HEAVY_MODE_ENABLED="true"
export QUALITY_THRESHOLD="95"
```

### CLAUDE.md Minimal Configuration
```markdown
# Autonomous Development Agent Configuration

## Project Context
- **Project Type**: [Your Project Type]
- **Technology Stack**: [Your Stack]
- **Development Stage**: [Current Stage]

## Autonomous Behavior Settings
- **Auto-commit**: Enabled
- **Auto-testing**: Enabled
- **Quality gates**: Enabled

## Tool Integration Preferences
```yaml
tools:
  vibe_coder:
    auto_task_creation: true
  deep_reasoning:
    escalation_mode: automatic
  research_trinity:
    auto_research: enabled
```
```

### Integration Configuration
```json
{
  "tools": {
    "vibe_coder": {"enabled": true, "auto_create_tasks": true},
    "deep_reasoning": {"enabled": true, "default_depth": 3},
    "sequential_thinking": {"enabled": true, "default_thoughts": 10},
    "research_trinity": {"enabled": true, "auto_synthesis": true}
  },
  "workflows": {
    "auto_documentation": true,
    "continuous_validation": true,
    "heavy_mode_gates": ["deploy", "release"]
  }
}
```

## 🚨 Troubleshooting Quick Fixes

### Tool Connection Issues
```bash
# Quick diagnosis
./diagnose-tool-connections.sh

# Restart all tools
./restart-all-tools.sh

# Check API keys
./validate-api-keys.sh

# Test individual tool
./test-single-tool.sh --tool="deep_reasoning"
```

### Performance Issues
```bash
# Check system resources
./check-system-resources.sh

# Optimize performance
./optimize-performance.sh --mode="automatic"

# Reduce load
./reduce-system-load.sh --level="conservative"

# Monitor real-time
./monitor-performance.sh --live
```

### Quality Gate Failures
```bash
# Analyze failures
./analyze-quality-failures.sh --gate="security"

# Fix common issues
./fix-quality-issues.sh --automatic

# Validate fixes
./validate-quality-fixes.sh

# Update thresholds
./update-quality-thresholds.sh --file="config.yaml"
```

### Workflow Issues
```bash
# Check workflow status
./check-workflow-status.sh --workflow-id="abc123"

# Restart stuck workflow
./restart-workflow.sh --workflow-id="abc123" --from-checkpoint

# Emergency workflow stop
./emergency-stop-workflow.sh --workflow-id="abc123"

# Workflow recovery
./recover-workflow.sh --workflow-id="abc123" --strategy="automatic"
```

## 📊 Status Commands

### System Health
```bash
# Overall system status
./system-status.sh

# Tool status summary
./tool-status-summary.sh

# Performance metrics
./performance-metrics.sh

# Quality metrics
./quality-metrics.sh
```

### Workflow Monitoring
```bash
# Active workflows
./list-active-workflows.sh

# Workflow details
./workflow-details.sh --workflow-id="abc123"

# Workflow logs
./workflow-logs.sh --workflow-id="abc123" --tail=100

# Workflow metrics
./workflow-metrics.sh --workflow-id="abc123"
```

## 🔐 Security Quick Reference

### Security Validation
```bash
# Security scan
./security-scan.sh --comprehensive

# Vulnerability check
./vulnerability-check.sh --severity="high"

# Compliance validation
./compliance-check.sh --framework="SOC2"

# Security report
./security-report.sh --format="detailed"
```

### Access Control
```bash
# Check permissions
./check-permissions.sh --user="username"

# Update access
./update-access.sh --user="username" --role="developer"

# Audit access
./audit-access.sh --timeframe="7d"

# Revoke access
./revoke-access.sh --user="username" --immediate
```

## 📈 Optimization Commands

### Performance Optimization
```bash
# Auto-optimize system
./auto-optimize.sh --level="aggressive"

# Cache optimization
./optimize-cache.sh --strategy="intelligent"

# Resource optimization
./optimize-resources.sh --target="memory"

# Workflow optimization
./optimize-workflows.sh --focus="speed"
```

### Quality Optimization
```bash
# Quality improvement
./improve-quality.sh --automatic

# Code optimization
./optimize-code.sh --target="performance"

# Test optimization
./optimize-tests.sh --coverage="increase"

# Documentation optimization
./optimize-docs.sh --completeness="100"
```

## 🆘 Emergency Commands

### Emergency Procedures
```bash
# Emergency stop
./emergency-stop.sh --confirm

# Emergency backup
./emergency-backup.sh --full

# Emergency recovery
./emergency-recovery.sh --strategy="automatic"

# Emergency rollback
./emergency-rollback.sh --to-checkpoint="stable"
```

### System Recovery
```bash
# Assess damage
./assess-damage.sh --comprehensive

# Recovery planning
./plan-recovery.sh --damage-level="moderate"

# Execute recovery
./execute-recovery.sh --plan="recovery-plan.json"

# Validate recovery
./validate-recovery.sh --full-check
```

---

## 📚 Key Documentation Links

- **[Complete Workflow Guide](workflows/complete-workflow-guide.md)** - Comprehensive workflows
- **[User Guide](user-guide-comprehensive.md)** - Complete user manual
- **[Advanced Patterns](workflows/advanced-workflow-patterns.md)** - Advanced AI patterns
- **[Technical Documentation](technical-documentation.md)** - Technical reference
- **[Troubleshooting](troubleshooting/)** - Issue resolution guides

## 🎯 Getting Help

- **Quick Issues**: Check this reference guide first
- **Complex Issues**: Refer to full documentation
- **Community**: Join Discord for community support
- **Enterprise**: Contact professional support team

**Remember**: This system is designed to be autonomous and self-healing. Most issues resolve automatically, but these commands provide manual override capabilities when needed.