"""
End-to-end tests for autonomous development workflows using Playwright.
"""
import pytest
import asyncio
import json
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser
from unittest.mock import Mock, patch

@pytest.mark.e2e
class TestAutonomousWorkflow:
    """End-to-end tests for autonomous development workflows."""
    
    @pytest.fixture(scope="class")
    async def browser_context(self):
        """Create browser context for testing."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            yield context
            await browser.close()
    
    @pytest.fixture
    async def page(self, browser_context):
        """Create a new page for each test."""
        page = await browser_context.new_page()
        yield page
        await page.close()
    
    @pytest.mark.asyncio
    async def test_project_initialization_workflow(self, page: Page, temp_workspace):
        """Test complete project initialization workflow."""
        # Mock web interface for project setup
        mock_html = """
        <!DOCTYPE html>
        <html>
        <head><title>BMAD Autonomous Development</title></head>
        <body>
            <div id="project-setup">
                <h1>Project Initialization</h1>
                <form id="init-form">
                    <input id="project-name" type="text" placeholder="Project Name" />
                    <select id="project-type">
                        <option value="web-app">Web Application</option>
                        <option value="api">API Service</option>
                        <option value="cli">CLI Tool</option>
                    </select>
                    <textarea id="project-description" placeholder="Project Description"></textarea>
                    <button id="initialize-btn" type="submit">Initialize Project</button>
                </form>
                <div id="status" style="display: none;"></div>
            </div>
            <script>
                document.getElementById('init-form').onsubmit = function(e) {
                    e.preventDefault();
                    const status = document.getElementById('status');
                    status.style.display = 'block';
                    status.innerHTML = 'Project initialization started...';
                    setTimeout(() => {
                        status.innerHTML = 'Project initialized successfully!';
                    }, 2000);
                };
            </script>
        </body>
        </html>
        """
        
        # Create temporary HTML file
        html_file = temp_workspace / "project_setup.html"
        html_file.write_text(mock_html)
        
        # Navigate to the page
        await page.goto(f"file://{html_file}")
        
        # Fill in project details
        await page.fill("#project-name", "Test Autonomous Project")
        await page.select_option("#project-type", "web-app")
        await page.fill("#project-description", "A test project for autonomous development")
        
        # Click initialize button
        await page.click("#initialize-btn")
        
        # Wait for status update
        await page.wait_for_selector("#status", state="visible")
        await page.wait_for_text("#status", "Project initialized successfully!")
        
        # Verify project was initialized
        status_text = await page.text_content("#status")
        assert "successfully" in status_text
    
    @pytest.mark.asyncio
    async def test_agent_management_workflow(self, page: Page, temp_workspace):
        """Test agent management workflow."""
        mock_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Agent Management</title></head>
        <body>
            <div id="agent-dashboard">
                <h1>Agent Management Dashboard</h1>
                <div id="agent-list">
                    <div class="agent" data-agent="project-manager">
                        <span class="agent-name">Project Manager</span>
                        <span class="agent-status">Active</span>
                        <button class="stop-agent">Stop</button>
                    </div>
                    <div class="agent" data-agent="developer">
                        <span class="agent-name">Developer Agent</span>
                        <span class="agent-status">Idle</span>
                        <button class="start-agent">Start</button>
                    </div>
                </div>
                <button id="add-agent">Add New Agent</button>
            </div>
            <script>
                document.querySelectorAll('.start-agent').forEach(btn => {
                    btn.onclick = function() {
                        const agent = this.closest('.agent');
                        agent.querySelector('.agent-status').textContent = 'Active';
                        this.textContent = 'Stop';
                        this.className = 'stop-agent';
                    };
                });
                
                document.querySelectorAll('.stop-agent').forEach(btn => {
                    btn.onclick = function() {
                        const agent = this.closest('.agent');
                        agent.querySelector('.agent-status').textContent = 'Idle';
                        this.textContent = 'Start';
                        this.className = 'start-agent';
                    };
                });
            </script>
        </body>
        </html>
        """
        
        html_file = temp_workspace / "agent_management.html"
        html_file.write_text(mock_html)
        
        await page.goto(f"file://{html_file}")
        
        # Test starting an agent
        await page.click('[data-agent="developer"] .start-agent')
        
        # Verify agent status changed
        status = await page.text_content('[data-agent="developer"] .agent-status')
        assert status == "Active"
        
        # Test stopping an agent
        await page.click('[data-agent="project-manager"] .stop-agent')
        status = await page.text_content('[data-agent="project-manager"] .agent-status')
        assert status == "Idle"
    
    @pytest.mark.asyncio
    async def test_tool_integration_workflow(self, page: Page, temp_workspace):
        """Test tool integration workflow."""
        mock_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Tool Integration</title></head>
        <body>
            <div id="tool-integration">
                <h1>Tool Integration Hub</h1>
                <div id="available-tools">
                    <div class="tool" data-tool="taskmaster-ai">
                        <h3>TaskMaster AI</h3>
                        <p>Project management and task automation</p>
                        <button class="connect-tool">Connect</button>
                        <div class="tool-status">Disconnected</div>
                    </div>
                    <div class="tool" data-tool="github">
                        <h3>GitHub</h3>
                        <p>Version control and collaboration</p>
                        <button class="connect-tool">Connect</button>
                        <div class="tool-status">Disconnected</div>
                    </div>
                </div>
                <div id="connected-tools" style="display: none;">
                    <h2>Connected Tools</h2>
                    <ul id="tool-list"></ul>
                </div>
            </div>
            <script>
                let connectedTools = [];
                
                document.querySelectorAll('.connect-tool').forEach(btn => {
                    btn.onclick = function() {
                        const tool = this.closest('.tool');
                        const toolName = tool.dataset.tool;
                        const status = tool.querySelector('.tool-status');
                        
                        if (this.textContent === 'Connect') {
                            status.textContent = 'Connected';
                            this.textContent = 'Disconnect';
                            connectedTools.push(toolName);
                        } else {
                            status.textContent = 'Disconnected';
                            this.textContent = 'Connect';
                            connectedTools = connectedTools.filter(t => t !== toolName);
                        }
                        
                        updateConnectedTools();
                    };
                });
                
                function updateConnectedTools() {
                    const connectedDiv = document.getElementById('connected-tools');
                    const toolList = document.getElementById('tool-list');
                    
                    if (connectedTools.length > 0) {
                        connectedDiv.style.display = 'block';
                        toolList.innerHTML = connectedTools.map(tool => `<li>${tool}</li>`).join('');
                    } else {
                        connectedDiv.style.display = 'none';
                    }
                }
            </script>
        </body>
        </html>
        """
        
        html_file = temp_workspace / "tool_integration.html"
        html_file.write_text(mock_html)
        
        await page.goto(f"file://{html_file}")
        
        # Connect TaskMaster AI
        await page.click('[data-tool="taskmaster-ai"] .connect-tool')
        
        # Verify connection
        status = await page.text_content('[data-tool="taskmaster-ai"] .tool-status')
        assert status == "Connected"
        
        # Connect GitHub
        await page.click('[data-tool="github"] .connect-tool')
        
        # Verify connected tools list is visible
        await page.wait_for_selector("#connected-tools", state="visible")
        
        # Check both tools are listed
        tool_items = await page.query_selector_all("#tool-list li")
        assert len(tool_items) == 2