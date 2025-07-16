"""
Test data generators and mock scenario creators for the autonomous development system.
"""
import pytest
import json
import random
import string
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional
from faker import Faker
import factory
from factory import fuzzy
import uuid
from datetime import datetime, timedelta

class ProjectDataGenerator:
    """Generate test data for autonomous development projects."""
    
    def __init__(self, seed=None):
        self.fake = Faker()
        if seed:
            Faker.seed(seed)
            random.seed(seed)
    
    def generate_project_metadata(self) -> Dict[str, Any]:
        """Generate realistic project metadata."""
        project_types = [
            "autonomous-development",
            "web-application", 
            "api-service",
            "cli-tool",
            "data-science",
            "mobile-app"
        ]
        
        return {
            "id": str(uuid.uuid4()),
            "name": self.fake.slug(),
            "title": self.fake.catch_phrase(),
            "description": self.fake.text(max_nb_chars=200),
            "type": random.choice(project_types),
            "created_at": self.fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
            "updated_at": self.fake.date_time_between(start_date="-1m", end_date="now").isoformat(),
            "version": f"{random.randint(0, 5)}.{random.randint(0, 10)}.{random.randint(0, 20)}",
            "status": random.choice(["active", "completed", "archived", "paused"]),
            "owner": self.fake.name(),
            "repository": f"https://github.com/{self.fake.user_name()}/{self.fake.slug()}",
            "tags": [self.fake.word() for _ in range(random.randint(2, 6))]
        }
    
    def generate_claude_md_content(self, project_metadata: Dict[str, Any]) -> str:
        """Generate realistic CLAUDE.md content."""
        phases = [
            "Phase 1: Project Setup and Planning",
            "Phase 2: Development and Implementation", 
            "Phase 3: Testing and Quality Assurance",
            "Phase 4: Deployment and Monitoring",
            "Phase 5: Maintenance and Optimization"
        ]
        
        agents = [
            "Project Manager",
            "Development Agent",
            "Testing Agent", 
            "Security Agent",
            "Quality Assurance Agent",
            "DevOps Agent",
            "Documentation Agent"
        ]
        
        tools = [
            "taskmaster-ai: Project management and task automation",
            "github: Version control and collaboration",
            "fetch: Research and documentation capabilities",
            "dart: Task tracking and workflow management",
            "playwright: End-to-end testing automation",
            "docker: Containerization and deployment"
        ]
        
        return f"""# {project_metadata['title']}

## Project Overview
{project_metadata['description']}

**Project Type**: {project_metadata['type']}
**Status**: {project_metadata['status']}
**Version**: {project_metadata['version']}

## Current Phase
{random.choice(phases)}

## Active Agents
{chr(10).join(f"- {agent}" for agent in random.sample(agents, random.randint(3, 5)))}

## Tool Integration
{chr(10).join(f"- {tool}" for tool in random.sample(tools, random.randint(3, 6)))}

## Progress Metrics
- Tasks Completed: {random.randint(15, 85)}/100
- Test Coverage: {random.randint(70, 95)}%
- Code Quality Score: {random.randint(7, 10)}/10
- Security Rating: {random.choice(['A', 'A+', 'B', 'B+'])}

## Recent Updates
{self.fake.text(max_nb_chars=300)}

## Next Steps
{chr(10).join(f"- {self.fake.sentence()}" for _ in range(random.randint(3, 7)))}
"""
    
    def generate_project_structure(self, base_path: Path, project_metadata: Dict[str, Any]) -> Dict[str, str]:
        """Generate a complete project directory structure."""
        project_dir = base_path / project_metadata["name"]
        project_dir.mkdir(exist_ok=True)
        
        files_created = {}
        
        # Generate CLAUDE.md
        claude_content = self.generate_claude_md_content(project_metadata)
        claude_file = project_dir / "CLAUDE.md"
        claude_file.write_text(claude_content)
        files_created["CLAUDE.md"] = claude_content
        
        # Generate README.md
        readme_content = f"""# {project_metadata['title']}

{project_metadata['description']}

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from {project_metadata['name']} import main
main.run()
```

## Testing
```bash
pytest tests/
```

## Contributing
Pull requests welcome!
"""
        readme_file = project_dir / "README.md"
        readme_file.write_text(readme_content)
        files_created["README.md"] = readme_content
        
        # Generate requirements.txt
        requirements = [
            "pytest>=7.0.0",
            "requests>=2.28.0",
            "pydantic>=1.10.0",
            "fastapi>=0.85.0",
            "uvicorn>=0.18.0"
        ]
        requirements_content = "\n".join(requirements)
        requirements_file = project_dir / "requirements.txt"
        requirements_file.write_text(requirements_content)
        files_created["requirements.txt"] = requirements_content
        
        # Generate source code structure
        src_dir = project_dir / "src"
        src_dir.mkdir(exist_ok=True)
        
        main_py_content = f'''"""
Main module for {project_metadata['title']}.
"""

def main():
    """Main entry point."""
    print("Welcome to {project_metadata['title']}")
    return True

if __name__ == "__main__":
    main()
'''
        main_file = src_dir / "main.py"
        main_file.write_text(main_py_content)
        files_created["src/main.py"] = main_py_content
        
        # Generate test structure
        test_dir = project_dir / "tests"
        test_dir.mkdir(exist_ok=True)
        
        test_main_content = f'''"""
Tests for {project_metadata['title']}.
"""
import pytest
from src.main import main

def test_main():
    """Test main function."""
    assert main() is True

def test_integration():
    """Test integration."""
    result = main()
    assert result is not None
'''
        test_file = test_dir / "test_main.py"
        test_file.write_text(test_main_content)
        files_created["tests/test_main.py"] = test_main_content
        
        return files_created

class AgentDataGenerator:
    """Generate test data for autonomous agents."""
    
    def __init__(self, seed=None):
        self.fake = Faker()
        if seed:
            Faker.seed(seed)
    
    def generate_agent_config(self) -> Dict[str, Any]:
        """Generate agent configuration data."""
        agent_types = [
            "project_manager",
            "developer", 
            "tester",
            "security_specialist",
            "devops_engineer",
            "qa_analyst"
        ]
        
        capabilities = [
            "task_planning",
            "code_generation",
            "test_automation",
            "security_scanning",
            "deployment_management",
            "monitoring_setup",
            "documentation_writing"
        ]
        
        return {
            "id": str(uuid.uuid4()),
            "name": self.fake.user_name(),
            "type": random.choice(agent_types),
            "capabilities": random.sample(capabilities, random.randint(2, 4)),
            "status": random.choice(["active", "idle", "busy", "offline"]),
            "created_at": self.fake.date_time_between(start_date="-30d", end_date="now").isoformat(),
            "last_active": self.fake.date_time_between(start_date="-1d", end_date="now").isoformat(),
            "performance_metrics": {
                "tasks_completed": random.randint(10, 500),
                "success_rate": round(random.uniform(0.7, 0.99), 2),
                "average_response_time": round(random.uniform(0.1, 5.0), 2),
                "uptime_percentage": round(random.uniform(85, 99.9), 1)
            },
            "configuration": {
                "max_concurrent_tasks": random.randint(1, 10),
                "timeout_seconds": random.randint(30, 300),
                "retry_count": random.randint(1, 5),
                "priority_level": random.randint(1, 10)
            }
        }

class TaskDataGenerator:
    """Generate test data for tasks and workflows."""
    
    def __init__(self, seed=None):
        self.fake = Faker()
        if seed:
            Faker.seed(seed)
    
    def generate_task_data(self) -> Dict[str, Any]:
        """Generate realistic task data."""
        task_types = [
            "development",
            "testing", 
            "deployment",
            "documentation",
            "research",
            "security_review",
            "performance_optimization"
        ]
        
        priorities = ["low", "medium", "high", "critical"]
        statuses = ["pending", "in_progress", "review", "completed", "cancelled"]
        
        return {
            "id": str(uuid.uuid4()),
            "title": self.fake.sentence(nb_words=4),
            "description": self.fake.text(max_nb_chars=200),
            "type": random.choice(task_types),
            "priority": random.choice(priorities),
            "status": random.choice(statuses),
            "estimated_hours": random.randint(1, 40),
            "actual_hours": random.randint(0, 45) if random.random() > 0.3 else None,
            "assigned_agent": str(uuid.uuid4()),
            "created_at": self.fake.date_time_between(start_date="-60d", end_date="now").isoformat(),
            "due_date": self.fake.date_time_between(start_date="now", end_date="+30d").isoformat(),
            "completed_at": self.fake.date_time_between(start_date="-30d", end_date="now").isoformat() if random.random() > 0.6 else None,
            "dependencies": [str(uuid.uuid4()) for _ in range(random.randint(0, 3))],
            "tags": [self.fake.word() for _ in range(random.randint(1, 4))],
            "metadata": {
                "complexity": random.randint(1, 10),
                "risk_level": random.choice(["low", "medium", "high"]),
                "automation_possible": random.choice([True, False])
            }
        }
    
    def generate_subtasks(self, parent_task_id: str, count: int = None) -> List[Dict[str, Any]]:
        """Generate subtasks for a parent task."""
        if count is None:
            count = random.randint(2, 8)
        
        subtasks = []
        for i in range(count):
            subtask = {
                "id": str(uuid.uuid4()),
                "parent_id": parent_task_id,
                "title": f"Subtask {i+1}: {self.fake.sentence(nb_words=3)}",
                "description": self.fake.text(max_nb_chars=100),
                "status": random.choice(["pending", "in_progress", "completed"]),
                "estimated_hours": random.randint(1, 8),
                "order": i + 1,
                "created_at": self.fake.date_time_between(start_date="-30d", end_date="now").isoformat()
            }
            subtasks.append(subtask)
        
        return subtasks

class TestScenarioGenerator:
    """Generate comprehensive test scenarios."""
    
    def __init__(self, seed=None):
        self.project_gen = ProjectDataGenerator(seed)
        self.agent_gen = AgentDataGenerator(seed)
        self.task_gen = TaskDataGenerator(seed)
    
    def generate_full_project_scenario(self, base_path: Path) -> Dict[str, Any]:
        """Generate a complete project scenario with all components."""
        # Generate project
        project_metadata = self.project_gen.generate_project_metadata()
        project_files = self.project_gen.generate_project_structure(base_path, project_metadata)
        
        # Generate agents
        agents = [self.agent_gen.generate_agent_config() for _ in range(random.randint(3, 7))]
        
        # Generate tasks
        tasks = [self.task_gen.generate_task_data() for _ in range(random.randint(10, 25))]
        
        # Generate subtasks for some tasks
        subtasks = []
        for task in random.sample(tasks, random.randint(3, 8)):
            task_subtasks = self.task_gen.generate_subtasks(task["id"])
            subtasks.extend(task_subtasks)
        
        scenario = {
            "scenario_id": str(uuid.uuid4()),
            "name": f"Test Scenario: {project_metadata['title']}",
            "project": project_metadata,
            "project_files": project_files,
            "agents": agents,
            "tasks": tasks,
            "subtasks": subtasks,
            "generated_at": datetime.now().isoformat(),
            "statistics": {
                "total_agents": len(agents),
                "total_tasks": len(tasks),
                "total_subtasks": len(subtasks),
                "active_agents": len([a for a in agents if a["status"] == "active"]),
                "completed_tasks": len([t for t in tasks if t["status"] == "completed"])
            }
        }
        
        return scenario
    
    def generate_stress_test_scenario(self, scale_factor: int = 1) -> Dict[str, Any]:
        """Generate a stress test scenario with large amounts of data."""
        agents = [self.agent_gen.generate_agent_config() for _ in range(20 * scale_factor)]
        tasks = [self.task_gen.generate_task_data() for _ in range(100 * scale_factor)]
        
        # Create complex dependency chains
        for i, task in enumerate(tasks[1:], 1):
            # Add dependencies to previous tasks
            dependency_count = min(random.randint(0, 3), i)
            task["dependencies"] = [tasks[j]["id"] for j in random.sample(range(i), dependency_count)]
        
        return {
            "scenario_type": "stress_test",
            "scale_factor": scale_factor,
            "agents": agents,
            "tasks": tasks,
            "expected_load": {
                "concurrent_agents": len(agents),
                "total_tasks": len(tasks),
                "dependency_complexity": sum(len(t["dependencies"]) for t in tasks)
            }
        }

@pytest.mark.data
class TestDataGenerators:
    """Test suite for data generators."""
    
    @pytest.fixture
    def project_generator(self):
        """Create project data generator with fixed seed."""
        return ProjectDataGenerator(seed=12345)
    
    @pytest.fixture
    def agent_generator(self):
        """Create agent data generator with fixed seed."""
        return AgentDataGenerator(seed=12345)
    
    @pytest.fixture
    def task_generator(self):
        """Create task data generator with fixed seed."""
        return TaskDataGenerator(seed=12345)
    
    @pytest.fixture
    def scenario_generator(self):
        """Create scenario generator with fixed seed."""
        return TestScenarioGenerator(seed=12345)
    
    def test_project_metadata_generation(self, project_generator):
        """Test project metadata generation."""
        metadata = project_generator.generate_project_metadata()
        
        assert "id" in metadata
        assert "name" in metadata
        assert "type" in metadata
        assert metadata["type"] in [
            "autonomous-development", "web-application", "api-service", 
            "cli-tool", "data-science", "mobile-app"
        ]
        assert "created_at" in metadata
        assert "version" in metadata
    
    def test_claude_md_generation(self, project_generator):
        """Test CLAUDE.md content generation."""
        metadata = project_generator.generate_project_metadata()
        claude_content = project_generator.generate_claude_md_content(metadata)
        
        assert metadata["title"] in claude_content
        assert "## Project Overview" in claude_content
        assert "## Current Phase" in claude_content
        assert "## Active Agents" in claude_content
        assert "## Tool Integration" in claude_content
    
    def test_project_structure_generation(self, project_generator, temp_workspace):
        """Test complete project structure generation."""
        metadata = project_generator.generate_project_metadata()
        files_created = project_generator.generate_project_structure(temp_workspace, metadata)
        
        # Check that all expected files were created
        expected_files = ["CLAUDE.md", "README.md", "requirements.txt", "src/main.py", "tests/test_main.py"]
        
        for expected_file in expected_files:
            assert expected_file in files_created
            assert len(files_created[expected_file]) > 0
        
        # Check that actual files exist
        project_dir = temp_workspace / metadata["name"]
        assert (project_dir / "CLAUDE.md").exists()
        assert (project_dir / "README.md").exists()
        assert (project_dir / "src" / "main.py").exists()
    
    def test_agent_config_generation(self, agent_generator):
        """Test agent configuration generation."""
        agent_config = agent_generator.generate_agent_config()
        
        assert "id" in agent_config
        assert "name" in agent_config
        assert "type" in agent_config
        assert "capabilities" in agent_config
        assert "performance_metrics" in agent_config
        assert isinstance(agent_config["capabilities"], list)
        assert len(agent_config["capabilities"]) >= 2
    
    def test_task_data_generation(self, task_generator):
        """Test task data generation."""
        task_data = task_generator.generate_task_data()
        
        assert "id" in task_data
        assert "title" in task_data
        assert "type" in task_data
        assert "priority" in task_data
        assert "status" in task_data
        assert task_data["priority"] in ["low", "medium", "high", "critical"]
        assert task_data["status"] in ["pending", "in_progress", "review", "completed", "cancelled"]
    
    def test_subtask_generation(self, task_generator):
        """Test subtask generation."""
        parent_task_id = str(uuid.uuid4())
        subtasks = task_generator.generate_subtasks(parent_task_id, count=5)
        
        assert len(subtasks) == 5
        for subtask in subtasks:
            assert subtask["parent_id"] == parent_task_id
            assert "id" in subtask
            assert "title" in subtask
            assert "order" in subtask
    
    def test_full_scenario_generation(self, scenario_generator, temp_workspace):
        """Test full project scenario generation."""
        scenario = scenario_generator.generate_full_project_scenario(temp_workspace)
        
        assert "scenario_id" in scenario
        assert "project" in scenario
        assert "agents" in scenario
        assert "tasks" in scenario
        assert "statistics" in scenario
        
        # Verify statistics match data
        stats = scenario["statistics"]
        assert stats["total_agents"] == len(scenario["agents"])
        assert stats["total_tasks"] == len(scenario["tasks"])
        assert stats["total_subtasks"] == len(scenario["subtasks"])
    
    def test_stress_test_scenario_generation(self, scenario_generator):
        """Test stress test scenario generation."""
        scenario = scenario_generator.generate_stress_test_scenario(scale_factor=2)
        
        assert scenario["scenario_type"] == "stress_test"
        assert scenario["scale_factor"] == 2
        assert len(scenario["agents"]) == 40  # 20 * 2
        assert len(scenario["tasks"]) == 200  # 100 * 2
        assert "expected_load" in scenario
    
    def test_data_consistency_with_seed(self, temp_workspace):
        """Test that data generation is consistent with the same seed."""
        # Generate data with same seed twice
        gen1 = ProjectDataGenerator(seed=999)
        gen2 = ProjectDataGenerator(seed=999)
        
        metadata1 = gen1.generate_project_metadata()
        metadata2 = gen2.generate_project_metadata()
        
        # Should generate identical data
        assert metadata1["name"] == metadata2["name"]
        assert metadata1["type"] == metadata2["type"]
        assert metadata1["description"] == metadata2["description"]
    
    def test_large_dataset_generation(self, scenario_generator):
        """Test generation of large datasets for performance testing."""
        large_scenario = scenario_generator.generate_stress_test_scenario(scale_factor=5)
        
        # Should handle large datasets without issues
        assert len(large_scenario["agents"]) == 100
        assert len(large_scenario["tasks"]) == 500
        
        # Verify data structure integrity
        for agent in large_scenario["agents"]:
            assert "id" in agent
            assert "type" in agent
        
        for task in large_scenario["tasks"]:
            assert "id" in task
            assert "title" in task