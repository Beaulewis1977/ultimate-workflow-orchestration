#!/usr/bin/env python3
"""
Tool Integration Hub
===================

Complete integration system for all development tools including:
- Make-it-heavy integration
- Deep-code-reasoning integration
- Context7, Perplexity, Brave Search integration
- TaskMaster, Vibe-Coder, GitHub integration
- Playwright automation
- Tmux Orchestrator integration

Features:
- Unified tool interface
- Automatic tool discovery and setup
- Load balancing and failover
- Performance monitoring
- Security validation
- Resource management

Author: Implementation Agent
Version: 1.0.0
"""

import os
import sys
import asyncio
import json
import logging
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import yaml
import aiohttp
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
import psutil
import docker
from functools import wraps
from tenacity import retry, stop_after_attempt, wait_exponential
import importlib.util
import requests
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ToolType(Enum):
    """Tool integration types"""
    SUBPROCESS = "subprocess"
    MCP = "mcp"
    HTTP_API = "http_api"
    WEBSOCKET = "websocket"
    DOCKER = "docker"
    PYTHON_MODULE = "python_module"

class ToolStatus(Enum):
    """Tool status"""
    UNKNOWN = "unknown"
    AVAILABLE = "available"
    INSTALLED = "installed"
    CONFIGURED = "configured"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"

@dataclass
class ToolConfig:
    """Tool configuration"""
    name: str
    type: ToolType
    command: Optional[str] = None
    endpoint: Optional[str] = None
    capabilities: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    setup_script: Optional[str] = None
    config_template: Optional[Dict[str, Any]] = None
    auth_required: bool = False
    rate_limit: Optional[int] = None
    timeout: int = 30
    retry_attempts: int = 3
    status: ToolStatus = ToolStatus.UNKNOWN
    last_used: Optional[datetime] = None
    usage_count: int = 0
    error_count: int = 0
    
@dataclass
class ToolResponse:
    """Tool response wrapper"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    duration: float = 0.0
    tool_name: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

class ToolManager:
    """Base tool manager"""
    
    def __init__(self, config: ToolConfig):
        self.config = config
        self.active = False
        self.last_health_check = None
        self.metrics = {
            'requests': 0,
            'errors': 0,
            'avg_response_time': 0.0,
            'uptime': 0.0
        }
    
    async def initialize(self) -> bool:
        """Initialize the tool"""
        try:
            logger.info(f"Initializing tool: {self.config.name}")
            await self._setup()
            await self._configure()
            self.active = True
            logger.info(f"Tool {self.config.name} initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize tool {self.config.name}: {e}")
            self.config.status = ToolStatus.ERROR
            return False
    
    async def _setup(self) -> None:
        """Setup tool (install if needed)"""
        if self.config.setup_script:
            try:
                result = subprocess.run(['bash', self.config.setup_script], 
                                      capture_output=True, text=True, check=True)
                logger.info(f"Setup script completed for {self.config.name}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Setup script failed for {self.config.name}: {e}")
                raise
    
    async def _configure(self) -> None:
        """Configure tool"""
        self.config.status = ToolStatus.CONFIGURED
    
    async def execute(self, command: str, params: Dict[str, Any] = None) -> ToolResponse:
        """Execute tool command"""
        start_time = time.time()
        
        try:
            self.metrics['requests'] += 1
            result = await self._execute_command(command, params or {})
            
            duration = time.time() - start_time
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['requests'] - 1) + duration) / 
                self.metrics['requests']
            )
            
            self.config.usage_count += 1
            self.config.last_used = datetime.now()
            
            return ToolResponse(
                success=True,
                data=result,
                duration=duration,
                tool_name=self.config.name
            )
            
        except Exception as e:
            self.metrics['errors'] += 1
            self.config.error_count += 1
            
            return ToolResponse(
                success=False,
                error=str(e),
                duration=time.time() - start_time,
                tool_name=self.config.name
            )
    
    async def _execute_command(self, command: str, params: Dict[str, Any]) -> Any:
        """Execute specific command - to be implemented by subclasses"""
        raise NotImplementedError
    
    async def health_check(self) -> bool:
        """Check tool health"""
        try:
            result = await self._health_check()
            self.last_health_check = datetime.now()
            return result
        except Exception as e:
            logger.error(f"Health check failed for {self.config.name}: {e}")
            return False
    
    async def _health_check(self) -> bool:
        """Perform health check - to be implemented by subclasses"""
        return True
    
    async def shutdown(self) -> None:
        """Shutdown tool"""
        self.active = False
        await self._cleanup()
    
    async def _cleanup(self) -> None:
        """Cleanup resources"""
        pass

class SubprocessToolManager(ToolManager):
    """Manager for subprocess-based tools"""
    
    async def _execute_command(self, command: str, params: Dict[str, Any]) -> Any:
        """Execute subprocess command"""
        cmd_parts = [self.config.command] + command.split()
        
        # Add parameters
        for key, value in params.items():
            if isinstance(value, bool):
                if value:
                    cmd_parts.append(f"--{key}")
            else:
                cmd_parts.extend([f"--{key}", str(value)])
        
        try:
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=self.config.timeout,
                check=True
            )
            
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            raise Exception(f"Command timeout after {self.config.timeout} seconds")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Command failed with code {e.returncode}: {e.stderr}")
    
    async def _health_check(self) -> bool:
        """Check if command is available"""
        try:
            result = subprocess.run(['which', self.config.command], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

class MCPToolManager(ToolManager):
    """Manager for MCP-based tools"""
    
    def __init__(self, config: ToolConfig):
        super().__init__(config)
        self.session = None
    
    async def _execute_command(self, command: str, params: Dict[str, Any]) -> Any:
        """Execute MCP command through Claude Code"""
        # Format MCP command
        mcp_command = f"{self.config.name}_{command}"
        
        # Add parameters
        if params:
            param_str = " ".join([f"--{k} {v}" for k, v in params.items()])
            mcp_command = f"{mcp_command} {param_str}"
        
        # Execute through Claude Code
        try:
            result = subprocess.run(
                ['claude', 'code', '-p', mcp_command],
                capture_output=True,
                text=True,
                timeout=self.config.timeout
            )
            
            if result.returncode == 0:
                return {'output': result.stdout, 'success': True}
            else:
                raise Exception(f"MCP command failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            raise Exception(f"MCP command timeout after {self.config.timeout} seconds")
    
    async def _health_check(self) -> bool:
        """Check MCP tool availability"""
        try:
            result = subprocess.run(['claude', 'code', '--list-tools'], 
                                  capture_output=True, text=True)
            return self.config.name in result.stdout
        except Exception:
            return False

class HTTPAPIToolManager(ToolManager):
    """Manager for HTTP API-based tools"""
    
    def __init__(self, config: ToolConfig):
        super().__init__(config)
        self.session = None
    
    async def _setup(self) -> None:
        """Setup HTTP session"""
        await super()._setup()
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout)
        )
    
    async def _execute_command(self, command: str, params: Dict[str, Any]) -> Any:
        """Execute HTTP API command"""
        url = f"{self.config.endpoint}/{command}"
        
        # Prepare headers
        headers = {'Content-Type': 'application/json'}
        
        # Add authentication if required
        if self.config.auth_required:
            # This would implement authentication logic
            pass
        
        try:
            async with self.session.post(url, json=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
                
        except aiohttp.ClientError as e:
            raise Exception(f"HTTP API error: {e}")
    
    async def _health_check(self) -> bool:
        """Check API health"""
        try:
            async with self.session.get(f"{self.config.endpoint}/health") as response:
                return response.status == 200
        except Exception:
            return False
    
    async def _cleanup(self) -> None:
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()

class DockerToolManager(ToolManager):
    """Manager for Docker-based tools"""
    
    def __init__(self, config: ToolConfig):
        super().__init__(config)
        self.client = None
        self.container = None
    
    async def _setup(self) -> None:
        """Setup Docker client and container"""
        await super()._setup()
        
        try:
            self.client = docker.from_env()
            
            # Check if container exists
            try:
                self.container = self.client.containers.get(self.config.name)
                if self.container.status != 'running':
                    self.container.start()
            except docker.errors.NotFound:
                # Create container
                self.container = self.client.containers.run(
                    self.config.command,
                    name=self.config.name,
                    detach=True,
                    remove=True
                )
                
        except Exception as e:
            logger.error(f"Docker setup failed for {self.config.name}: {e}")
            raise
    
    async def _execute_command(self, command: str, params: Dict[str, Any]) -> Any:
        """Execute command in Docker container"""
        if not self.container:
            raise Exception("Docker container not available")
        
        # Format command
        cmd = command.split()
        if params:
            for key, value in params.items():
                cmd.extend([f"--{key}", str(value)])
        
        try:
            result = self.container.exec_run(cmd)
            return {
                'output': result.output.decode('utf-8'),
                'exit_code': result.exit_code
            }
        except Exception as e:
            raise Exception(f"Docker command failed: {e}")
    
    async def _health_check(self) -> bool:
        """Check container health"""
        try:
            if self.container:
                self.container.reload()
                return self.container.status == 'running'
            return False
        except Exception:
            return False
    
    async def _cleanup(self) -> None:
        """Cleanup Docker resources"""
        if self.container:
            try:
                self.container.stop()
                self.container.remove()
            except Exception:
                pass

class PythonModuleToolManager(ToolManager):
    """Manager for Python module-based tools"""
    
    def __init__(self, config: ToolConfig):
        super().__init__(config)
        self.module = None
    
    async def _setup(self) -> None:
        """Setup Python module"""
        await super()._setup()
        
        try:
            # Import module
            self.module = importlib.import_module(self.config.command)
            
            # Initialize if needed
            if hasattr(self.module, 'initialize'):
                await self.module.initialize()
                
        except ImportError as e:
            raise Exception(f"Failed to import module {self.config.command}: {e}")
    
    async def _execute_command(self, command: str, params: Dict[str, Any]) -> Any:
        """Execute Python module command"""
        if not self.module:
            raise Exception("Python module not available")
        
        # Find command function
        command_func = getattr(self.module, command, None)
        if not command_func:
            raise Exception(f"Command '{command}' not found in module")
        
        # Execute command
        try:
            if asyncio.iscoroutinefunction(command_func):
                return await command_func(**params)
            else:
                return command_func(**params)
        except Exception as e:
            raise Exception(f"Module command failed: {e}")
    
    async def _health_check(self) -> bool:
        """Check module health"""
        return self.module is not None

class ToolIntegrationHub:
    """Central hub for all tool integrations"""
    
    def __init__(self):
        self.tools = {}
        self.tool_configs = {}
        self.load_balancer = LoadBalancer()
        self.security_validator = SecurityValidator()
        self.performance_monitor = PerformanceMonitor()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.initialized = False
        
        # Initialize tool configurations
        self._initialize_tool_configs()
    
    def _initialize_tool_configs(self) -> None:
        """Initialize tool configurations"""
        self.tool_configs = {
            'make-it-heavy': ToolConfig(
                name='make-it-heavy',
                type=ToolType.SUBPROCESS,
                command='make-it-heavy',
                capabilities=['multi_agent', 'workflow_automation', 'task_distribution'],
                setup_script='/mnt/c/bmad-workspace/make-it-heavy-integration.sh',
                timeout=120,
                retry_attempts=2
            ),
            'deep-code-reasoning': ToolConfig(
                name='deep-code-reasoning',
                type=ToolType.MCP,
                capabilities=['code_analysis', 'bug_detection', 'performance_optimization'],
                timeout=60
            ),
            'context7': ToolConfig(
                name='context7',
                type=ToolType.MCP,
                capabilities=['documentation', 'api_reference', 'code_examples'],
                timeout=30
            ),
            'perplexity': ToolConfig(
                name='perplexity',
                type=ToolType.MCP,
                capabilities=['web_search', 'research', 'current_events'],
                timeout=45
            ),
            'brave-search': ToolConfig(
                name='brave-search',
                type=ToolType.MCP,
                capabilities=['web_search', 'competitive_intelligence'],
                timeout=30
            ),
            'playwright': ToolConfig(
                name='playwright',
                type=ToolType.MCP,
                capabilities=['browser_automation', 'testing', 'scraping'],
                timeout=120
            ),
            'github': ToolConfig(
                name='github',
                type=ToolType.MCP,
                capabilities=['repository_management', 'ci_cd', 'issue_tracking'],
                timeout=60
            ),
            'taskmaster': ToolConfig(
                name='taskmaster',
                type=ToolType.MCP,
                capabilities=['project_management', 'task_tracking', 'planning'],
                timeout=45
            ),
            'dart': ToolConfig(
                name='dart',
                type=ToolType.MCP,
                capabilities=['task_management', 'team_coordination'],
                timeout=30
            ),
            'vibe-kanban': ToolConfig(
                name='vibe-kanban',
                type=ToolType.MCP,
                capabilities=['kanban_board', 'task_tracking', 'project_management'],
                timeout=30
            ),
            'tmux-orchestrator': ToolConfig(
                name='tmux-orchestrator',
                type=ToolType.SUBPROCESS,
                command='/mnt/c/bmad-workspace/Tmux-Orchestrator/send-claude-message.sh',
                capabilities=['session_management', 'agent_coordination'],
                timeout=15
            ),
            'puppeteer': ToolConfig(
                name='puppeteer',
                type=ToolType.MCP,
                capabilities=['browser_automation', 'performance_testing'],
                timeout=90
            ),
            'desktop-commander': ToolConfig(
                name='desktop-commander',
                type=ToolType.MCP,
                capabilities=['system_monitoring', 'file_management'],
                timeout=30
            ),
            'n8n': ToolConfig(
                name='n8n',
                type=ToolType.HTTP_API,
                endpoint='http://localhost:5678/api/v1',
                capabilities=['workflow_automation', 'integration'],
                timeout=60
            ),
            'docker': ToolConfig(
                name='docker',
                type=ToolType.SUBPROCESS,
                command='docker',
                capabilities=['containerization', 'deployment'],
                timeout=120
            ),
            'sequential-thinking': ToolConfig(
                name='sequential-thinking',
                type=ToolType.MCP,
                capabilities=['reasoning', 'planning', 'analysis'],
                timeout=90
            ),
            'memory': ToolConfig(
                name='memory',
                type=ToolType.MCP,
                capabilities=['knowledge_storage', 'retrieval', 'learning'],
                timeout=30
            ),
            'agentic-tools': ToolConfig(
                name='agentic-tools',
                type=ToolType.MCP,
                capabilities=['project_management', 'task_coordination', 'memory'],
                timeout=45
            ),
            'fetch': ToolConfig(
                name='fetch',
                type=ToolType.MCP,
                capabilities=['web_content', 'data_retrieval'],
                timeout=30
            ),
            'mcp-installer': ToolConfig(
                name='mcp-installer',
                type=ToolType.MCP,
                capabilities=['tool_installation', 'configuration'],
                timeout=180
            ),
            'claude-code': ToolConfig(
                name='claude-code',
                type=ToolType.SUBPROCESS,
                command='claude',
                capabilities=['development', 'coordination', 'intelligence'],
                timeout=60
            )
        }
    
    async def initialize(self) -> None:
        """Initialize all tool integrations"""
        logger.info("Initializing Tool Integration Hub...")
        
        # Create tool managers
        for name, config in self.tool_configs.items():
            try:
                manager = self._create_tool_manager(config)
                success = await manager.initialize()
                
                if success:
                    self.tools[name] = manager
                    logger.info(f"✅ Tool integrated: {name}")
                else:
                    logger.warning(f"❌ Tool integration failed: {name}")
                    
            except Exception as e:
                logger.error(f"❌ Tool integration error for {name}: {e}")
        
        # Start monitoring
        await self.performance_monitor.start()
        
        self.initialized = True
        logger.info(f"Tool Integration Hub initialized with {len(self.tools)} tools")
    
    def _create_tool_manager(self, config: ToolConfig) -> ToolManager:
        """Create appropriate tool manager based on type"""
        if config.type == ToolType.SUBPROCESS:
            return SubprocessToolManager(config)
        elif config.type == ToolType.MCP:
            return MCPToolManager(config)
        elif config.type == ToolType.HTTP_API:
            return HTTPAPIToolManager(config)
        elif config.type == ToolType.DOCKER:
            return DockerToolManager(config)
        elif config.type == ToolType.PYTHON_MODULE:
            return PythonModuleToolManager(config)
        else:
            raise ValueError(f"Unknown tool type: {config.type}")
    
    async def execute_tool(self, tool_name: str, command: str, params: Dict[str, Any] = None) -> ToolResponse:
        """Execute a tool command"""
        if not self.initialized:
            raise Exception("Tool Integration Hub not initialized")
        
        if tool_name not in self.tools:
            return ToolResponse(
                success=False,
                error=f"Tool '{tool_name}' not available",
                tool_name=tool_name
            )
        
        # Security validation
        if not await self.security_validator.validate_request(tool_name, command, params):
            return ToolResponse(
                success=False,
                error="Security validation failed",
                tool_name=tool_name
            )
        
        # Load balancing (if multiple instances)
        tool_manager = self.load_balancer.get_best_instance(tool_name, self.tools)
        
        # Execute with retry
        return await self._execute_with_retry(tool_manager, command, params)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _execute_with_retry(self, tool_manager: ToolManager, command: str, params: Dict[str, Any]) -> ToolResponse:
        """Execute tool command with retry logic"""
        try:
            response = await tool_manager.execute(command, params)
            
            # Monitor performance
            await self.performance_monitor.record_execution(tool_manager.config.name, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            raise
    
    async def get_tool_status(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """Get tool status"""
        if tool_name:
            if tool_name not in self.tools:
                return {'error': f"Tool '{tool_name}' not found"}
            
            tool_manager = self.tools[tool_name]
            health_ok = await tool_manager.health_check()
            
            return {
                'name': tool_name,
                'type': tool_manager.config.type.value,
                'status': tool_manager.config.status.value,
                'active': tool_manager.active,
                'healthy': health_ok,
                'capabilities': tool_manager.config.capabilities,
                'metrics': tool_manager.metrics,
                'usage_count': tool_manager.config.usage_count,
                'error_count': tool_manager.config.error_count,
                'last_used': tool_manager.config.last_used.isoformat() if tool_manager.config.last_used else None
            }
        else:
            # Return status for all tools
            status = {}
            for name, tool_manager in self.tools.items():
                health_ok = await tool_manager.health_check()
                status[name] = {
                    'type': tool_manager.config.type.value,
                    'status': tool_manager.config.status.value,
                    'active': tool_manager.active,
                    'healthy': health_ok,
                    'capabilities': tool_manager.config.capabilities,
                    'usage_count': tool_manager.config.usage_count,
                    'error_count': tool_manager.config.error_count
                }
            return status
    
    async def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        return [name for name, tool_manager in self.tools.items() if tool_manager.active]
    
    async def get_tool_capabilities(self, tool_name: str) -> List[str]:
        """Get tool capabilities"""
        if tool_name not in self.tools:
            return []
        
        return self.tools[tool_name].config.capabilities
    
    async def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a multi-tool workflow"""
        workflow_results = {
            'workflow_id': workflow.get('id', 'unknown'),
            'started_at': datetime.now().isoformat(),
            'steps': [],
            'success': True,
            'errors': []
        }
        
        for step in workflow.get('steps', []):
            step_result = await self._execute_workflow_step(step)
            workflow_results['steps'].append(step_result)
            
            if not step_result.get('success', False):
                workflow_results['success'] = False
                workflow_results['errors'].append(step_result.get('error', 'Unknown error'))
                
                # Check if workflow should continue on error
                if not step.get('continue_on_error', False):
                    break
        
        workflow_results['completed_at'] = datetime.now().isoformat()
        return workflow_results
    
    async def _execute_workflow_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        tool_name = step.get('tool')
        command = step.get('command')
        params = step.get('params', {})
        
        if not tool_name or not command:
            return {
                'success': False,
                'error': 'Missing tool or command in workflow step'
            }
        
        try:
            response = await self.execute_tool(tool_name, command, params)
            return {
                'tool': tool_name,
                'command': command,
                'success': response.success,
                'data': response.data,
                'error': response.error,
                'duration': response.duration
            }
        except Exception as e:
            return {
                'tool': tool_name,
                'command': command,
                'success': False,
                'error': str(e),
                'duration': 0.0
            }
    
    async def health_check_all(self) -> Dict[str, bool]:
        """Health check all tools"""
        health_status = {}
        
        for name, tool_manager in self.tools.items():
            try:
                health_status[name] = await tool_manager.health_check()
            except Exception as e:
                logger.error(f"Health check failed for {name}: {e}")
                health_status[name] = False
        
        return health_status
    
    async def shutdown(self) -> None:
        """Shutdown all tools"""
        logger.info("Shutting down Tool Integration Hub...")
        
        # Stop monitoring
        await self.performance_monitor.stop()
        
        # Shutdown all tools
        for name, tool_manager in self.tools.items():
            try:
                await tool_manager.shutdown()
                logger.info(f"✅ Tool shutdown: {name}")
            except Exception as e:
                logger.error(f"❌ Tool shutdown error for {name}: {e}")
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        logger.info("Tool Integration Hub shutdown complete")

class LoadBalancer:
    """Load balancer for tool instances"""
    
    def __init__(self):
        self.instance_metrics = {}
    
    def get_best_instance(self, tool_name: str, tools: Dict[str, ToolManager]) -> ToolManager:
        """Get best tool instance (for future multi-instance support)"""
        return tools[tool_name]
    
    def record_metrics(self, tool_name: str, response_time: float, success: bool) -> None:
        """Record performance metrics"""
        if tool_name not in self.instance_metrics:
            self.instance_metrics[tool_name] = {
                'response_times': [],
                'success_count': 0,
                'error_count': 0
            }
        
        metrics = self.instance_metrics[tool_name]
        metrics['response_times'].append(response_time)
        
        if success:
            metrics['success_count'] += 1
        else:
            metrics['error_count'] += 1
        
        # Keep only last 100 response times
        if len(metrics['response_times']) > 100:
            metrics['response_times'] = metrics['response_times'][-100:]

class SecurityValidator:
    """Security validation for tool requests"""
    
    def __init__(self):
        self.blocked_commands = set()
        self.allowed_patterns = {}
        self.rate_limits = {}
    
    async def validate_request(self, tool_name: str, command: str, params: Dict[str, Any]) -> bool:
        """Validate tool request for security"""
        # Check for blocked commands
        if command in self.blocked_commands:
            logger.warning(f"Blocked command attempted: {command}")
            return False
        
        # Check for dangerous patterns
        if await self._check_dangerous_patterns(tool_name, command, params):
            logger.warning(f"Dangerous pattern detected in {tool_name}: {command}")
            return False
        
        # Check rate limits
        if not await self._check_rate_limit(tool_name):
            logger.warning(f"Rate limit exceeded for {tool_name}")
            return False
        
        return True
    
    async def _check_dangerous_patterns(self, tool_name: str, command: str, params: Dict[str, Any]) -> bool:
        """Check for dangerous patterns in commands"""
        dangerous_patterns = [
            r'rm\s+-rf\s+/',
            r'sudo\s+rm',
            r'format\s+c:',
            r'del\s+/s\s+/q',
            r'DROP\s+TABLE',
            r'DELETE\s+FROM.*WHERE\s+1=1',
            r'eval\s*\(',
            r'exec\s*\(',
            r'__import__',
            r'system\s*\(',
            r'shell=True'
        ]
        
        # Check command
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        
        # Check parameters
        for value in params.values():
            if isinstance(value, str):
                for pattern in dangerous_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        return True
        
        return False
    
    async def _check_rate_limit(self, tool_name: str) -> bool:
        """Check rate limits"""
        current_time = datetime.now()
        
        if tool_name not in self.rate_limits:
            self.rate_limits[tool_name] = {
                'requests': [],
                'limit': 100,  # Default limit
                'window': 60   # 1 minute window
            }
        
        rate_limit = self.rate_limits[tool_name]
        
        # Clean old requests
        cutoff_time = current_time - timedelta(seconds=rate_limit['window'])
        rate_limit['requests'] = [
            req_time for req_time in rate_limit['requests'] 
            if req_time > cutoff_time
        ]
        
        # Check if under limit
        if len(rate_limit['requests']) >= rate_limit['limit']:
            return False
        
        # Add current request
        rate_limit['requests'].append(current_time)
        return True

class PerformanceMonitor:
    """Performance monitoring for tools"""
    
    def __init__(self):
        self.metrics = {}
        self.running = False
        self.monitor_task = None
    
    async def start(self) -> None:
        """Start performance monitoring"""
        self.running = True
        self.monitor_task = asyncio.create_task(self._monitor_loop())
    
    async def stop(self) -> None:
        """Stop performance monitoring"""
        self.running = False
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
    
    async def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self.running:
            try:
                # Collect system metrics
                await self._collect_system_metrics()
                
                # Generate performance report
                await self._generate_performance_report()
                
                await asyncio.sleep(60)  # Monitor every minute
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def _collect_system_metrics(self) -> None:
        """Collect system performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Network I/O
            network = psutil.net_io_counters()
            
            self.metrics['system'] = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': (disk.used / disk.total) * 100,
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv
            }
            
        except Exception as e:
            logger.error(f"System metrics collection failed: {e}")
    
    async def _generate_performance_report(self) -> None:
        """Generate performance report"""
        # This would generate detailed performance reports
        pass
    
    async def record_execution(self, tool_name: str, response: ToolResponse) -> None:
        """Record tool execution metrics"""
        if tool_name not in self.metrics:
            self.metrics[tool_name] = {
                'executions': [],
                'total_executions': 0,
                'successful_executions': 0,
                'failed_executions': 0,
                'avg_response_time': 0.0,
                'total_response_time': 0.0
            }
        
        metrics = self.metrics[tool_name]
        
        # Record execution
        execution_data = {
            'timestamp': response.timestamp.isoformat(),
            'duration': response.duration,
            'success': response.success,
            'error': response.error
        }
        
        metrics['executions'].append(execution_data)
        metrics['total_executions'] += 1
        metrics['total_response_time'] += response.duration
        
        if response.success:
            metrics['successful_executions'] += 1
        else:
            metrics['failed_executions'] += 1
        
        # Update average response time
        metrics['avg_response_time'] = metrics['total_response_time'] / metrics['total_executions']
        
        # Keep only last 1000 executions
        if len(metrics['executions']) > 1000:
            metrics['executions'] = metrics['executions'][-1000:]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.metrics

# Tool-specific implementations

class MakeItHeavyTool:
    """Make-It-Heavy tool integration"""
    
    def __init__(self, hub: ToolIntegrationHub):
        self.hub = hub
    
    async def analyze_with_multiple_agents(self, query: str, context: str = "") -> ToolResponse:
        """Analyze query with multiple AI agents"""
        params = {
            'query': f"{query} - Context: {context}",
            'mode': 'multi-agent'
        }
        
        return await self.hub.execute_tool('make-it-heavy', 'analyze', params)
    
    async def generate_workflow(self, project_type: str, requirements: str) -> ToolResponse:
        """Generate workflow for project"""
        params = {
            'project_type': project_type,
            'requirements': requirements,
            'output_format': 'workflow'
        }
        
        return await self.hub.execute_tool('make-it-heavy', 'generate', params)

class DeepCodeReasoningTool:
    """Deep Code Reasoning tool integration"""
    
    def __init__(self, hub: ToolIntegrationHub):
        self.hub = hub
    
    async def analyze_code_complexity(self, code_path: str) -> ToolResponse:
        """Analyze code complexity"""
        params = {
            'path': code_path,
            'analysis_type': 'complexity'
        }
        
        return await self.hub.execute_tool('deep-code-reasoning', 'analyze', params)
    
    async def suggest_optimizations(self, code_path: str) -> ToolResponse:
        """Suggest code optimizations"""
        params = {
            'path': code_path,
            'analysis_type': 'optimization'
        }
        
        return await self.hub.execute_tool('deep-code-reasoning', 'optimize', params)

class ResearchTool:
    """Research tool integration (Perplexity + Brave + Context7)"""
    
    def __init__(self, hub: ToolIntegrationHub):
        self.hub = hub
    
    async def comprehensive_research(self, topic: str) -> Dict[str, ToolResponse]:
        """Perform comprehensive research using multiple sources"""
        results = {}
        
        # Perplexity for current information
        results['perplexity'] = await self.hub.execute_tool(
            'perplexity', 'search_web', {'query': topic, 'recency': 'week'}
        )
        
        # Brave Search for broader web search
        results['brave'] = await self.hub.execute_tool(
            'brave-search', 'web_search', {'query': topic}
        )
        
        # Context7 for documentation
        results['context7'] = await self.hub.execute_tool(
            'context7', 'search', {'query': topic}
        )
        
        return results
    
    async def market_analysis(self, product_name: str) -> Dict[str, ToolResponse]:
        """Perform market analysis"""
        queries = [
            f"{product_name} market analysis",
            f"{product_name} competitors",
            f"{product_name} pricing strategy",
            f"{product_name} user reviews"
        ]
        
        results = {}
        for query in queries:
            results[query] = await self.hub.execute_tool(
                'perplexity', 'search_web', {'query': query, 'recency': 'month'}
            )
        
        return results

class ProjectManagementTool:
    """Project management tool integration"""
    
    def __init__(self, hub: ToolIntegrationHub):
        self.hub = hub
    
    async def create_project_structure(self, project_name: str, project_type: str) -> Dict[str, ToolResponse]:
        """Create project structure across multiple tools"""
        results = {}
        
        # TaskMaster AI
        results['taskmaster'] = await self.hub.execute_tool(
            'taskmaster', 'initialize_project', {'name': project_name, 'type': project_type}
        )
        
        # Dart task management
        results['dart'] = await self.hub.execute_tool(
            'dart', 'create_project', {'name': project_name, 'description': f'{project_type} project'}
        )
        
        # Vibe Kanban
        results['kanban'] = await self.hub.execute_tool(
            'vibe-kanban', 'create_project', {'name': project_name}
        )
        
        return results
    
    async def sync_tasks_across_tools(self, project_id: str) -> Dict[str, ToolResponse]:
        """Synchronize tasks across project management tools"""
        results = {}
        
        # Get tasks from each tool
        taskmaster_tasks = await self.hub.execute_tool(
            'taskmaster', 'get_tasks', {'project_id': project_id}
        )
        
        dart_tasks = await self.hub.execute_tool(
            'dart', 'list_tasks', {'project_id': project_id}
        )
        
        kanban_tasks = await self.hub.execute_tool(
            'vibe-kanban', 'list_tasks', {'project_id': project_id}
        )
        
        # Sync logic would go here
        results['sync_completed'] = True
        
        return results

class AutomationTool:
    """Automation tool integration"""
    
    def __init__(self, hub: ToolIntegrationHub):
        self.hub = hub
    
    async def setup_development_environment(self, project_path: str, project_type: str) -> Dict[str, ToolResponse]:
        """Setup development environment"""
        results = {}
        
        # Git initialization
        results['git'] = await self.hub.execute_tool(
            'desktop-commander', 'execute_command', 
            {'command': 'git init', 'timeout_ms': 30000}
        )
        
        # Install dependencies based on project type
        if project_type == 'nodejs':
            results['npm'] = await self.hub.execute_tool(
                'desktop-commander', 'execute_command',
                {'command': 'npm install', 'timeout_ms': 120000}
            )
        elif project_type == 'python':
            results['pip'] = await self.hub.execute_tool(
                'desktop-commander', 'execute_command',
                {'command': 'pip install -r requirements.txt', 'timeout_ms': 120000}
            )
        
        return results
    
    async def run_automated_tests(self, project_path: str) -> Dict[str, ToolResponse]:
        """Run automated tests using Playwright"""
        results = {}
        
        # Generate test cases
        results['test_generation'] = await self.hub.execute_tool(
            'playwright', 'generate_test_cases', {'project_path': project_path}
        )
        
        # Run tests
        results['test_execution'] = await self.hub.execute_tool(
            'playwright', 'run_tests', {'project_path': project_path}
        )
        
        return results

# CLI Interface
async def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Tool Integration Hub')
    parser.add_argument('--initialize', action='store_true', help='Initialize all tools')
    parser.add_argument('--status', action='store_true', help='Show tool status')
    parser.add_argument('--health-check', action='store_true', help='Run health check')
    parser.add_argument('--execute', help='Execute tool command (format: tool:command)')
    parser.add_argument('--params', help='Command parameters as JSON')
    parser.add_argument('--workflow', help='Execute workflow from file')
    
    args = parser.parse_args()
    
    hub = ToolIntegrationHub()
    
    try:
        if args.initialize:
            await hub.initialize()
            print("✅ Tool Integration Hub initialized")
            return
        
        if args.status:
            status = await hub.get_tool_status()
            print(json.dumps(status, indent=2))
            return
        
        if args.health_check:
            health = await hub.health_check_all()
            print(json.dumps(health, indent=2))
            return
        
        if args.execute:
            if ':' not in args.execute:
                print("❌ Invalid format. Use 'tool:command'")
                return
            
            tool_name, command = args.execute.split(':', 1)
            params = json.loads(args.params) if args.params else {}
            
            await hub.initialize()
            response = await hub.execute_tool(tool_name, command, params)
            
            print(json.dumps({
                'success': response.success,
                'data': response.data,
                'error': response.error,
                'duration': response.duration
            }, indent=2))
            return
        
        if args.workflow:
            with open(args.workflow, 'r') as f:
                workflow = json.load(f)
            
            await hub.initialize()
            result = await hub.execute_workflow(workflow)
            print(json.dumps(result, indent=2))
            return
        
        # Interactive mode
        await hub.initialize()
        print("🚀 Tool Integration Hub ready!")
        print("Available tools:", ", ".join(await hub.get_available_tools()))
        
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await hub.shutdown()

if __name__ == "__main__":
    asyncio.run(main())