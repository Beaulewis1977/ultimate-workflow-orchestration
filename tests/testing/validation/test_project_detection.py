"""
Validation tests for project detection and parsing functionality.
"""
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import os

class ProjectDetector:
    """Project detection and validation utility."""
    
    def __init__(self):
        self.supported_project_types = [
            "autonomous-development",
            "web-application", 
            "api-service",
            "cli-tool",
            "data-science",
            "mobile-app"
        ]
        self.required_files = {
            "autonomous-development": ["CLAUDE.md", "README.md"],
            "web-application": ["package.json", "README.md"],
            "api-service": ["requirements.txt", "app.py"],
            "cli-tool": ["setup.py", "README.md"],
            "data-science": ["requirements.txt", "jupyter_notebook_config.py"],
            "mobile-app": ["pubspec.yaml", "README.md"]
        }
    
    def detect_project_type(self, project_path):
        """Detect the type of project in the given path."""
        path = Path(project_path)
        if not path.exists():
            return None, "Project path does not exist"
        
        # Check for CLAUDE.md (autonomous development project)
        if (path / "CLAUDE.md").exists():
            return "autonomous-development", "CLAUDE.md found"
        
        # Check for web application indicators
        if (path / "package.json").exists():
            return "web-application", "package.json found"
        
        # Check for Python API service
        if (path / "app.py").exists() and (path / "requirements.txt").exists():
            return "api-service", "Python API structure detected"
        
        # Check for CLI tool
        if (path / "setup.py").exists():
            return "cli-tool", "setup.py found"
        
        # Check for data science project
        if (path / "jupyter_notebook_config.py").exists():
            return "data-science", "Jupyter configuration found"
        
        # Check for mobile app
        if (path / "pubspec.yaml").exists():
            return "mobile-app", "Flutter/Dart project detected"
        
        return "unknown", "Could not determine project type"
    
    def validate_project_structure(self, project_path, expected_type=None):
        """Validate project structure against expected type."""
        path = Path(project_path)
        detected_type, reason = self.detect_project_type(project_path)
        
        if expected_type and detected_type != expected_type:
            return False, f"Expected {expected_type}, but detected {detected_type}"
        
        if detected_type == "unknown":
            return False, "Unknown project type"
        
        # Check required files
        required = self.required_files.get(detected_type, [])
        missing_files = []
        
        for file_name in required:
            if not (path / file_name).exists():
                missing_files.append(file_name)
        
        if missing_files:
            return False, f"Missing required files: {missing_files}"
        
        return True, f"Valid {detected_type} project"
    
    def get_project_metadata(self, project_path):
        """Extract project metadata."""
        path = Path(project_path)
        metadata = {
            "path": str(path.absolute()),
            "name": path.name,
            "type": None,
            "files": [],
            "directories": [],
            "size_bytes": 0
        }
        
        # Detect project type
        project_type, reason = self.detect_project_type(project_path)
        metadata["type"] = project_type
        
        # Collect files and directories
        try:
            for item in path.rglob("*"):
                if item.is_file():
                    metadata["files"].append(str(item.relative_to(path)))
                    metadata["size_bytes"] += item.stat().st_size
                elif item.is_dir():
                    metadata["directories"].append(str(item.relative_to(path)))
        except PermissionError:
            pass
        
        return metadata

class ClaudeMDParser:
    """Parser for CLAUDE.md files in autonomous development projects."""
    
    def __init__(self):
        self.required_sections = [
            "Project Overview",
            "Current Phase", 
            "Active Agents",
            "Tool Integration"
        ]
    
    def parse_claude_md(self, file_path):
        """Parse CLAUDE.md file and extract structured data."""
        path = Path(file_path)
        if not path.exists():
            return None, "CLAUDE.md file not found"
        
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            return None, f"Error reading file: {e}"
        
        parsed_data = {
            "sections": {},
            "agents": [],
            "tools": [],
            "phase": None,
            "validation_errors": []
        }
        
        current_section = None
        current_content = []
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            # Detect section headers
            if line.startswith('##') and not line.startswith('###'):
                # Save previous section
                if current_section and current_content:
                    parsed_data["sections"][current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = line[2:].strip()
                current_content = []
            
            elif current_section:
                current_content.append(line)
                
                # Extract specific data
                if current_section == "Current Phase" and line:
                    parsed_data["phase"] = line
                
                elif current_section == "Active Agents" and line.startswith('-'):
                    agent_name = line[1:].strip()
                    if agent_name:
                        parsed_data["agents"].append(agent_name)
                
                elif current_section == "Tool Integration" and ':' in line:
                    tool_info = line.split(':', 1)
                    if len(tool_info) == 2:
                        parsed_data["tools"].append({
                            "name": tool_info[0].strip(),
                            "description": tool_info[1].strip()
                        })
        
        # Save last section
        if current_section and current_content:
            parsed_data["sections"][current_section] = '\n'.join(current_content)
        
        # Validate required sections
        for section in self.required_sections:
            if section not in parsed_data["sections"]:
                parsed_data["validation_errors"].append(f"Missing required section: {section}")
        
        return parsed_data, "Parsing completed"
    
    def validate_claude_md(self, parsed_data):
        """Validate parsed CLAUDE.md data."""
        if not parsed_data:
            return False, "No data to validate"
        
        errors = parsed_data.get("validation_errors", [])
        
        # Additional validations
        if not parsed_data.get("phase"):
            errors.append("No current phase specified")
        
        if not parsed_data.get("agents"):
            errors.append("No active agents specified")
        
        if not parsed_data.get("tools"):
            errors.append("No tool integrations specified")
        
        if errors:
            return False, f"Validation errors: {errors}"
        
        return True, "CLAUDE.md is valid"

@pytest.mark.validation
class TestProjectDetection:
    """Test suite for project detection and validation."""
    
    @pytest.fixture
    def project_detector(self):
        """Create project detector instance."""
        return ProjectDetector()
    
    @pytest.fixture
    def claude_parser(self):
        """Create CLAUDE.md parser instance."""
        return ClaudeMDParser()
    
    def test_autonomous_project_detection(self, project_detector, temp_workspace):
        """Test detection of autonomous development projects."""
        # Create autonomous project structure
        project_dir = temp_workspace / "autonomous_project"
        project_dir.mkdir()
        
        # Create CLAUDE.md
        claude_md = project_dir / "CLAUDE.md"
        claude_md.write_text("""# Autonomous Development Project

## Project Overview
Test autonomous development project.

## Current Phase
Phase 1: Development

## Active Agents
- Project Manager
- Development Agent

## Tool Integration
- taskmaster-ai: Task management
""")
        
        # Create README.md
        readme = project_dir / "README.md"
        readme.write_text("# Autonomous Project\nTest project")
        
        # Test detection
        project_type, reason = project_detector.detect_project_type(project_dir)
        assert project_type == "autonomous-development"
        assert "CLAUDE.md" in reason
    
    def test_web_application_detection(self, project_detector, temp_workspace):
        """Test detection of web applications."""
        # Create web app structure
        project_dir = temp_workspace / "web_app"
        project_dir.mkdir()
        
        # Create package.json
        package_json = project_dir / "package.json"
        package_json.write_text(json.dumps({
            "name": "test-web-app",
            "version": "1.0.0",
            "dependencies": {"react": "^18.0.0"}
        }))
        
        # Create README.md
        readme = project_dir / "README.md"
        readme.write_text("# Web Application")
        
        # Test detection
        project_type, reason = project_detector.detect_project_type(project_dir)
        assert project_type == "web-application"
        assert "package.json" in reason
    
    def test_api_service_detection(self, project_detector, temp_workspace):
        """Test detection of API services."""
        # Create API service structure
        project_dir = temp_workspace / "api_service"
        project_dir.mkdir()
        
        # Create app.py
        app_py = project_dir / "app.py"
        app_py.write_text("from flask import Flask\napp = Flask(__name__)")
        
        # Create requirements.txt
        requirements = project_dir / "requirements.txt"
        requirements.write_text("flask==2.0.1\nrequests==2.28.0")
        
        # Test detection
        project_type, reason = project_detector.detect_project_type(project_dir)
        assert project_type == "api-service"
        assert "API structure" in reason
    
    def test_unknown_project_detection(self, project_detector, temp_workspace):
        """Test detection of unknown project types."""
        # Create generic directory
        project_dir = temp_workspace / "unknown_project"
        project_dir.mkdir()
        
        # Create some random files
        (project_dir / "random.txt").write_text("random content")
        
        # Test detection
        project_type, reason = project_detector.detect_project_type(project_dir)
        assert project_type == "unknown"
        assert "Could not determine" in reason
    
    def test_project_structure_validation(self, project_detector, temp_workspace):
        """Test project structure validation."""
        # Create valid autonomous project
        project_dir = temp_workspace / "valid_project"
        project_dir.mkdir()
        
        (project_dir / "CLAUDE.md").write_text("# Test Project")
        (project_dir / "README.md").write_text("# README")
        
        # Test validation
        is_valid, message = project_detector.validate_project_structure(
            project_dir, expected_type="autonomous-development"
        )
        assert is_valid is True
        assert "Valid autonomous-development" in message
    
    def test_project_structure_validation_missing_files(self, project_detector, temp_workspace):
        """Test validation with missing required files."""
        # Create incomplete project
        project_dir = temp_workspace / "incomplete_project"
        project_dir.mkdir()
        
        (project_dir / "CLAUDE.md").write_text("# Test Project")
        # Missing README.md
        
        # Test validation
        is_valid, message = project_detector.validate_project_structure(project_dir)
        assert is_valid is False
        assert "Missing required files" in message
        assert "README.md" in message
    
    def test_project_metadata_extraction(self, project_detector, temp_workspace):
        """Test project metadata extraction."""
        # Create project with various files
        project_dir = temp_workspace / "metadata_project"
        project_dir.mkdir()
        
        (project_dir / "CLAUDE.md").write_text("# Test Project")
        (project_dir / "README.md").write_text("# README")
        
        src_dir = project_dir / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("print('hello')")
        
        # Get metadata
        metadata = project_detector.get_project_metadata(project_dir)
        
        assert metadata["type"] == "autonomous-development"
        assert metadata["name"] == "metadata_project"
        assert "CLAUDE.md" in metadata["files"]
        assert "README.md" in metadata["files"]
        assert "src/main.py" in metadata["files"]
        assert "src" in metadata["directories"]
        assert metadata["size_bytes"] > 0
    
    def test_claude_md_parsing(self, claude_parser, temp_workspace):
        """Test CLAUDE.md parsing functionality."""
        # Create CLAUDE.md file
        claude_md = temp_workspace / "CLAUDE.md"
        claude_md.write_text("""# Test Autonomous Project

## Project Overview
This is a test project for autonomous development.

## Current Phase
Phase 2: Implementation

## Active Agents
- Project Manager
- Development Agent
- Testing Agent

## Tool Integration
- taskmaster-ai: Project management and task automation
- github: Version control and collaboration
- fetch: Research and documentation

## Notes
Additional project notes here.
""")
        
        # Parse the file
        parsed_data, message = claude_parser.parse_claude_md(claude_md)
        
        assert parsed_data is not None
        assert parsed_data["phase"] == "Phase 2: Implementation"
        assert len(parsed_data["agents"]) == 3
        assert "Project Manager" in parsed_data["agents"]
        assert len(parsed_data["tools"]) == 3
        assert parsed_data["tools"][0]["name"] == "taskmaster-ai"
        assert "Project Overview" in parsed_data["sections"]
    
    def test_claude_md_validation(self, claude_parser, temp_workspace):
        """Test CLAUDE.md validation."""
        # Create valid CLAUDE.md
        claude_md = temp_workspace / "valid_claude.md"
        claude_md.write_text("""# Valid Project

## Project Overview
Valid project overview.

## Current Phase
Phase 1: Setup

## Active Agents
- Test Agent

## Tool Integration
- test-tool: Testing functionality
""")
        
        # Parse and validate
        parsed_data, _ = claude_parser.parse_claude_md(claude_md)
        is_valid, message = claude_parser.validate_claude_md(parsed_data)
        
        assert is_valid is True
        assert "valid" in message.lower()
    
    def test_claude_md_validation_errors(self, claude_parser, temp_workspace):
        """Test CLAUDE.md validation with errors."""
        # Create incomplete CLAUDE.md
        claude_md = temp_workspace / "invalid_claude.md"
        claude_md.write_text("""# Invalid Project

## Project Overview
Just an overview, missing other sections.
""")
        
        # Parse and validate
        parsed_data, _ = claude_parser.parse_claude_md(claude_md)
        is_valid, message = claude_parser.validate_claude_md(parsed_data)
        
        assert is_valid is False
        assert "Validation errors" in message
    
    def test_nonexistent_file_handling(self, claude_parser):
        """Test handling of non-existent files."""
        # Try to parse non-existent file
        parsed_data, message = claude_parser.parse_claude_md("/nonexistent/path.md")
        
        assert parsed_data is None
        assert "not found" in message