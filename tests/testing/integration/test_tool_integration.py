"""
Integration tests for tool interactions in the autonomous development system.
"""
import pytest
import asyncio
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

class MockToolIntegration:
    """Mock tool integration manager for testing."""
    
    def __init__(self):
        self.tools = {}
        self.active_sessions = {}
        self.tool_history = []
    
    def register_tool(self, tool_name, tool_config):
        """Register a tool with the integration manager."""
        self.tools[tool_name] = {
            "name": tool_name,
            "config": tool_config,
            "status": "registered",
            "last_used": None
        }
        return True
    
    async def invoke_tool(self, tool_name, method, params=None):
        """Invoke a tool method."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not registered")
        
        # Mock tool responses
        mock_responses = {
            "taskmaster-ai": {
                "get_tasks": {"tasks": [{"id": 1, "title": "Test Task"}]},
                "create_task": {"id": 2, "title": "New Task"},
                "update_task": {"success": True}
            },
            "github": {
                "create_repository": {"id": 123, "name": "test-repo"},
                "create_pull_request": {"number": 1, "title": "Test PR"},
                "get_file_contents": {"content": "test content"}
            },
            "fetch": {
                "fetch": {"content": "fetched content", "url": "https://example.com"}
            }
        }
        
        tool_response = mock_responses.get(tool_name, {}).get(method, {"success": True})
        
        # Record tool usage
        self.tool_history.append({
            "tool": tool_name,
            "method": method,
            "params": params,
            "response": tool_response,
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        return tool_response
    
    def get_tool_status(self, tool_name):
        """Get the status of a specific tool."""
        return self.tools.get(tool_name, {"status": "not_found"})
    
    def list_available_tools(self):
        """List all available tools."""
        return list(self.tools.keys())

@pytest.mark.integration
class TestToolIntegration:
    """Test suite for tool integration functionality."""
    
    @pytest.fixture
    def tool_manager(self):
        """Create a tool integration manager for testing."""
        return MockToolIntegration()
    
    def test_tool_registration(self, tool_manager):
        """Test registering tools with the integration manager."""
        config = {"timeout": 30, "retries": 3}
        
        result = tool_manager.register_tool("taskmaster-ai", config)
        assert result is True
        assert "taskmaster-ai" in tool_manager.tools
        assert tool_manager.tools["taskmaster-ai"]["config"] == config
    
    @pytest.mark.asyncio
    async def test_taskmaster_integration(self, tool_manager):
        """Test TaskMaster AI tool integration."""
        # Register the tool
        tool_manager.register_tool("taskmaster-ai", {})
        
        # Test getting tasks
        response = await tool_manager.invoke_tool("taskmaster-ai", "get_tasks")
        assert "tasks" in response
        assert len(response["tasks"]) > 0
        
        # Test creating a task
        params = {"title": "Test Task", "description": "Test Description"}
        response = await tool_manager.invoke_tool("taskmaster-ai", "create_task", params)
        assert "id" in response
        assert response["title"] == "New Task"
    
    @pytest.mark.asyncio
    async def test_github_integration(self, tool_manager):
        """Test GitHub tool integration."""
        # Register the tool
        tool_manager.register_tool("github", {})
        
        # Test creating repository
        params = {"name": "test-repo", "description": "Test repository"}
        response = await tool_manager.invoke_tool("github", "create_repository", params)
        assert "id" in response
        assert response["name"] == "test-repo"
        
        # Test creating pull request
        params = {"title": "Test PR", "body": "Test description"}
        response = await tool_manager.invoke_tool("github", "create_pull_request", params)
        assert "number" in response
        assert response["title"] == "Test PR"
    
    @pytest.mark.asyncio
    async def test_fetch_integration(self, tool_manager):
        """Test Fetch tool integration."""
        # Register the tool
        tool_manager.register_tool("fetch", {})
        
        # Test fetching content
        params = {"url": "https://example.com"}
        response = await tool_manager.invoke_tool("fetch", "fetch", params)
        assert "content" in response
        assert "url" in response
    
    @pytest.mark.asyncio
    async def test_tool_chain_workflow(self, tool_manager):
        """Test a complete workflow using multiple tools."""
        # Register all tools
        tool_manager.register_tool("taskmaster-ai", {})
        tool_manager.register_tool("github", {})
        tool_manager.register_tool("fetch", {})
        
        # Step 1: Create a task
        task_response = await tool_manager.invoke_tool(
            "taskmaster-ai", "create_task", 
            {"title": "Implement feature", "description": "Add new feature"}
        )
        
        # Step 2: Research the feature
        research_response = await tool_manager.invoke_tool(
            "fetch", "fetch",
            {"url": "https://docs.example.com/feature"}
        )
        
        # Step 3: Create GitHub repository
        repo_response = await tool_manager.invoke_tool(
            "github", "create_repository",
            {"name": "feature-implementation"}
        )
        
        # Step 4: Update task with progress
        update_response = await tool_manager.invoke_tool(
            "taskmaster-ai", "update_task",
            {"id": task_response["id"], "status": "in_progress"}
        )
        
        # Verify all steps completed
        assert len(tool_manager.tool_history) == 4
        assert all(step["response"] for step in tool_manager.tool_history)
    
    @pytest.mark.asyncio
    async def test_tool_error_handling(self, tool_manager):
        """Test error handling in tool integration."""
        # Test invoking unregistered tool
        with pytest.raises(ValueError, match="Tool nonexistent not registered"):
            await tool_manager.invoke_tool("nonexistent", "method")
    
    def test_tool_status_reporting(self, tool_manager):
        """Test tool status reporting."""
        # Register a tool
        tool_manager.register_tool("test-tool", {"version": "1.0"})
        
        # Check status
        status = tool_manager.get_tool_status("test-tool")
        assert status["status"] == "registered"
        assert status["config"]["version"] == "1.0"
        
        # Check non-existent tool
        status = tool_manager.get_tool_status("nonexistent")
        assert status["status"] == "not_found"
    
    def test_list_available_tools(self, tool_manager):
        """Test listing available tools."""
        # Register multiple tools
        tool_manager.register_tool("tool1", {})
        tool_manager.register_tool("tool2", {})
        tool_manager.register_tool("tool3", {})
        
        tools = tool_manager.list_available_tools()
        assert len(tools) == 3
        assert "tool1" in tools
        assert "tool2" in tools
        assert "tool3" in tools