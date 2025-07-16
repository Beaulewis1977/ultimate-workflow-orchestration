"""
Global pytest configuration and fixtures for the autonomous development system testing.
"""
import os
import sys
import tempfile
import shutil
import asyncio
import pytest
import docker
from pathlib import Path
from unittest.mock import Mock, patch
from typing import Generator, Dict, Any
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def docker_client():
    """Docker client for testing."""
    try:
        client = docker.from_env()
        yield client
        client.close()
    except Exception:
        pytest.skip("Docker not available")

@pytest.fixture
def temp_workspace() -> Generator[Path, None, None]:
    """Create a temporary workspace for testing."""
    temp_dir = tempfile.mkdtemp(prefix="bmad_test_")
    workspace = Path(temp_dir)
    yield workspace
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        "workspace_path": "/tmp/test_workspace",
        "claude_config": {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4096
        },
        "tools": {
            "enabled": ["taskmaster-ai", "github", "fetch", "dart"],
            "timeout": 30
        },
        "orchestrator": {
            "tmux_session": "test_session",
            "max_agents": 5,
            "check_interval": 10
        },
        "validation": {
            "strict_mode": True,
            "memory_limit": "1GB",
            "performance_threshold": 0.95
        }
    }

@pytest.fixture
def sample_claude_md():
    """Sample CLAUDE.md content for testing."""
    return """# Autonomous Development Project

## Project Overview
Test project for autonomous development system validation.

## Current Phase
Phase 1: Setup and Configuration

## Active Agents
- Project Manager
- Development Agent
- Testing Agent

## Tool Integration
- taskmaster-ai: Project management
- github: Version control
- fetch: Research capabilities

## Validation Requirements
- Memory usage < 1GB
- Response time < 5s
- Test coverage > 90%
"""

@pytest.fixture
def mock_tmux_session():
    """Mock tmux session for testing."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "test_session\nother_session"
        yield mock_run

@pytest.fixture
def sample_project_structure(temp_workspace):
    """Create a sample project structure for testing."""
    project_dir = temp_workspace / "test_project"
    project_dir.mkdir()
    
    # Create CLAUDE.md
    claude_md = project_dir / "CLAUDE.md"
    claude_md.write_text("""# Test Project
## Phase: Development
## Agents: 3
""")
    
    # Create src directory
    src_dir = project_dir / "src"
    src_dir.mkdir()
    
    # Create test files
    test_file = src_dir / "main.py"
    test_file.write_text("print('Hello, World!')")
    
    return project_dir

@pytest.fixture
def memory_monitor():
    """Memory monitoring fixture."""
    import psutil
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    def get_memory_usage():
        current_memory = process.memory_info().rss
        return current_memory - initial_memory
    
    return get_memory_usage

@pytest.fixture
def performance_tracker():
    """Performance tracking fixture."""
    import time
    metrics = {}
    
    def track(operation_name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                metrics[operation_name] = end_time - start_time
                return result
            return wrapper
        return decorator
    
    return track, metrics

@pytest.fixture
def validation_rules():
    """Standard validation rules for testing."""
    return {
        "max_memory_mb": 1024,
        "max_response_time_seconds": 5.0,
        "min_test_coverage": 0.90,
        "max_error_rate": 0.01,
        "required_files": ["CLAUDE.md", "README.md"],
        "prohibited_patterns": ["TODO", "FIXME", "XXX"]
    }

@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Setup test environment variables."""
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("BMAD_WORKSPACE", "/tmp/test_workspace")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")