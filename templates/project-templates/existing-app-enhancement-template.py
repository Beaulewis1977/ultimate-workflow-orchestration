#!/usr/bin/env python3
"""
Existing App Enhancement Template
=================================

Enhances existing applications with:
- AI-powered development tools
- Quality control system
- Modern development practices
- Testing frameworks
- Security improvements
- Performance optimizations

Usage:
    python existing-app-enhancement-template.py --path /path/to/app --type web --framework react
"""

import os
import sys
import json
import yaml
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
import logging
import ast
import re
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExistingAppEnhancementTemplate:
    """Template for enhancing existing applications with AI development tools"""
    
    def __init__(self):
        self.templates_dir = Path("/mnt/c/bmad-workspace/templates")
        self.enhancements = {
            "ai_integration": "Add AI development tools integration",
            "quality_control": "Implement CEO Quality Control Agent",
            "testing": "Add comprehensive testing framework",
            "security": "Implement security best practices",
            "ci_cd": "Add CI/CD pipeline",
            "documentation": "Generate comprehensive documentation",
            "performance": "Add performance monitoring",
            "monitoring": "Add application monitoring",
            "docker": "Add containerization",
            "typescript": "Migrate to TypeScript",
            "modern_patterns": "Implement modern development patterns"
        }
        
    def analyze_project(self, project_path: str) -> Dict:
        """Analyze existing project structure and technologies"""
        logger.info(f"🔍 Analyzing project: {project_path}")
        
        analysis = {
            "project_type": "unknown",
            "framework": "unknown",
            "language": "unknown",
            "package_manager": "unknown",
            "has_tests": False,
            "has_ci_cd": False,
            "has_docker": False,
            "has_security": False,
            "has_documentation": False,
            "technologies": [],
            "dependencies": {},
            "file_structure": {},
            "issues": [],
            "recommendations": []
        }
        
        # Analyze file structure
        analysis["file_structure"] = self._analyze_file_structure(project_path)
        
        # Detect project type and framework
        analysis.update(self._detect_project_type(project_path))
        
        # Analyze dependencies
        analysis["dependencies"] = self._analyze_dependencies(project_path)
        
        # Check for existing features
        analysis.update(self._check_existing_features(project_path))
        
        # Identify issues and recommendations
        analysis["issues"] = self._identify_issues(project_path, analysis)
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        return analysis
    
    def enhance_project(self, project_path: str, enhancements: List[str], options: Dict) -> str:
        """Enhance existing project with selected enhancements"""
        logger.info(f"🚀 Enhancing project: {project_path}")
        
        # Analyze project first
        analysis = self.analyze_project(project_path)
        
        # Create backup
        backup_path = self._create_backup(project_path)
        logger.info(f"📦 Backup created at: {backup_path}")
        
        try:
            # Apply enhancements
            for enhancement in enhancements:
                if enhancement in self.enhancements:
                    logger.info(f"⚡ Applying {enhancement}...")
                    self._apply_enhancement(project_path, enhancement, analysis, options)
                else:
                    logger.warning(f"Unknown enhancement: {enhancement}")
            
            # Generate summary report
            self._generate_enhancement_report(project_path, enhancements, analysis)
            
            logger.info("✅ Project enhancement complete!")
            return project_path
            
        except Exception as e:
            logger.error(f"Enhancement failed: {e}")
            # Restore backup
            self._restore_backup(backup_path, project_path)
            raise
    
    def _analyze_file_structure(self, project_path: str) -> Dict:
        """Analyze project file structure"""
        structure = {
            "total_files": 0,
            "code_files": 0,
            "test_files": 0,
            "config_files": 0,
            "documentation_files": 0,
            "directories": [],
            "file_types": defaultdict(int)
        }
        
        try:
            for root, dirs, files in os.walk(project_path):
                # Skip hidden directories and node_modules
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
                
                relative_root = os.path.relpath(root, project_path)
                if relative_root != '.':
                    structure["directories"].append(relative_root)
                
                for file in files:
                    if file.startswith('.'):
                        continue
                    
                    structure["total_files"] += 1
                    
                    # Analyze file type
                    file_ext = Path(file).suffix.lower()
                    structure["file_types"][file_ext] += 1
                    
                    # Categorize files
                    if file_ext in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.cpp', '.c']:
                        structure["code_files"] += 1
                    elif 'test' in file.lower() or file_ext in ['.test.js', '.spec.js', '.test.ts', '.spec.ts']:
                        structure["test_files"] += 1
                    elif file_ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
                        structure["config_files"] += 1
                    elif file_ext in ['.md', '.rst', '.txt']:
                        structure["documentation_files"] += 1
                        
        except Exception as e:
            logger.error(f"Error analyzing file structure: {e}")
        
        return structure
    
    def _detect_project_type(self, project_path: str) -> Dict:
        """Detect project type and framework"""
        detection = {
            "project_type": "unknown",
            "framework": "unknown",
            "language": "unknown",
            "package_manager": "unknown",
            "technologies": []
        }
        
        # Check for package.json (Node.js project)
        package_json_path = os.path.join(project_path, "package.json")
        if os.path.exists(package_json_path):
            detection["language"] = "javascript"
            detection["package_manager"] = "npm"
            
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    
                dependencies = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}
                
                # Detect framework
                if "react" in dependencies:
                    detection["framework"] = "react"
                    detection["project_type"] = "web"
                elif "vue" in dependencies:
                    detection["framework"] = "vue"
                    detection["project_type"] = "web"
                elif "@angular/core" in dependencies:
                    detection["framework"] = "angular"
                    detection["project_type"] = "web"
                elif "next" in dependencies:
                    detection["framework"] = "next"
                    detection["project_type"] = "web"
                elif "express" in dependencies:
                    detection["framework"] = "express"
                    detection["project_type"] = "api"
                elif "fastify" in dependencies:
                    detection["framework"] = "fastify"
                    detection["project_type"] = "api"
                elif "react-native" in dependencies:
                    detection["framework"] = "react-native"
                    detection["project_type"] = "mobile"
                elif "electron" in dependencies:
                    detection["framework"] = "electron"
                    detection["project_type"] = "desktop"
                
                # Detect technologies
                if "typescript" in dependencies:
                    detection["technologies"].append("typescript")
                if "jest" in dependencies:
                    detection["technologies"].append("jest")
                if "webpack" in dependencies:
                    detection["technologies"].append("webpack")
                if "vite" in dependencies:
                    detection["technologies"].append("vite")
                    
            except Exception as e:
                logger.error(f"Error reading package.json: {e}")
        
        # Check for Python project
        requirements_path = os.path.join(project_path, "requirements.txt")
        pyproject_path = os.path.join(project_path, "pyproject.toml")
        
        if os.path.exists(requirements_path) or os.path.exists(pyproject_path):
            detection["language"] = "python"
            detection["package_manager"] = "pip"
            
            # Try to detect Python framework
            try:
                requirements = []
                if os.path.exists(requirements_path):
                    with open(requirements_path, 'r') as f:
                        requirements = f.read().lower()
                
                if "fastapi" in requirements:
                    detection["framework"] = "fastapi"
                    detection["project_type"] = "api"
                elif "flask" in requirements:
                    detection["framework"] = "flask"
                    detection["project_type"] = "api"
                elif "django" in requirements:
                    detection["framework"] = "django"
                    detection["project_type"] = "web"
                elif "pytorch" in requirements:
                    detection["framework"] = "pytorch"
                    detection["project_type"] = "ai"
                elif "tensorflow" in requirements:
                    detection["framework"] = "tensorflow"
                    detection["project_type"] = "ai"
                    
            except Exception as e:
                logger.error(f"Error reading requirements.txt: {e}")
        
        # Check for Go project
        go_mod_path = os.path.join(project_path, "go.mod")
        if os.path.exists(go_mod_path):
            detection["language"] = "go"
            detection["package_manager"] = "go mod"
            
            try:
                with open(go_mod_path, 'r') as f:
                    go_mod_content = f.read()
                    
                if "gin-gonic/gin" in go_mod_content:
                    detection["framework"] = "gin"
                    detection["project_type"] = "api"
                elif "gorilla/mux" in go_mod_content:
                    detection["framework"] = "gorilla"
                    detection["project_type"] = "api"
                    
            except Exception as e:
                logger.error(f"Error reading go.mod: {e}")
        
        # Check for Rust project
        cargo_toml_path = os.path.join(project_path, "Cargo.toml")
        if os.path.exists(cargo_toml_path):
            detection["language"] = "rust"
            detection["package_manager"] = "cargo"
            detection["project_type"] = "cli"  # Default for Rust
            
            try:
                with open(cargo_toml_path, 'r') as f:
                    cargo_content = f.read()
                    
                if "actix-web" in cargo_content:
                    detection["framework"] = "actix"
                    detection["project_type"] = "api"
                elif "rocket" in cargo_content:
                    detection["framework"] = "rocket"
                    detection["project_type"] = "api"
                    
            except Exception as e:
                logger.error(f"Error reading Cargo.toml: {e}")
        
        return detection
    
    def _analyze_dependencies(self, project_path: str) -> Dict:
        """Analyze project dependencies"""
        dependencies = {
            "production": {},
            "development": {},
            "outdated": [],
            "vulnerable": [],
            "total_count": 0
        }
        
        # Node.js dependencies
        package_json_path = os.path.join(project_path, "package.json")
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    
                dependencies["production"] = package_data.get("dependencies", {})
                dependencies["development"] = package_data.get("devDependencies", {})
                dependencies["total_count"] = len(dependencies["production"]) + len(dependencies["development"])
                
                # Check for vulnerabilities (simplified)
                try:
                    result = subprocess.run(
                        ["npm", "audit", "--json"],
                        cwd=project_path,
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        audit_data = json.loads(result.stdout)
                        dependencies["vulnerable"] = list(audit_data.get("vulnerabilities", {}).keys())
                
                except Exception as e:
                    logger.debug(f"Could not run npm audit: {e}")
                    
            except Exception as e:
                logger.error(f"Error analyzing package.json: {e}")
        
        # Python dependencies
        requirements_path = os.path.join(project_path, "requirements.txt")
        if os.path.exists(requirements_path):
            try:
                with open(requirements_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            pkg = line.split('==')[0].split('>=')[0].split('<=')[0]
                            dependencies["production"][pkg] = line
                            
                dependencies["total_count"] = len(dependencies["production"])
                
            except Exception as e:
                logger.error(f"Error analyzing requirements.txt: {e}")
        
        return dependencies
    
    def _check_existing_features(self, project_path: str) -> Dict:
        """Check for existing features"""
        features = {
            "has_tests": False,
            "has_ci_cd": False,
            "has_docker": False,
            "has_security": False,
            "has_documentation": False,
            "has_linting": False,
            "has_formatting": False,
            "has_type_checking": False
        }
        
        # Check for tests
        test_patterns = ["test", "spec", "__tests__", "tests"]
        for pattern in test_patterns:
            test_path = os.path.join(project_path, pattern)
            if os.path.exists(test_path):
                features["has_tests"] = True
                break
        
        # Check for CI/CD
        ci_paths = [
            ".github/workflows",
            ".gitlab-ci.yml",
            ".travis.yml",
            "circle.yml",
            "jenkins.yml"
        ]
        for ci_path in ci_paths:
            if os.path.exists(os.path.join(project_path, ci_path)):
                features["has_ci_cd"] = True
                break
        
        # Check for Docker
        docker_files = ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"]
        for docker_file in docker_files:
            if os.path.exists(os.path.join(project_path, docker_file)):
                features["has_docker"] = True
                break
        
        # Check for security
        security_files = ["SECURITY.md", ".snyk", "security.txt"]
        for security_file in security_files:
            if os.path.exists(os.path.join(project_path, security_file)):
                features["has_security"] = True
                break
        
        # Check for documentation
        doc_files = ["README.md", "docs", "documentation"]
        for doc_file in doc_files:
            if os.path.exists(os.path.join(project_path, doc_file)):
                features["has_documentation"] = True
                break
        
        # Check for linting
        lint_files = [".eslintrc", ".pylintrc", "ruff.toml", "tslint.json"]
        for lint_file in lint_files:
            if os.path.exists(os.path.join(project_path, lint_file)):
                features["has_linting"] = True
                break
        
        # Check for formatting
        format_files = [".prettierrc", ".black", "pyproject.toml"]
        for format_file in format_files:
            if os.path.exists(os.path.join(project_path, format_file)):
                features["has_formatting"] = True
                break
        
        # Check for type checking
        type_files = ["tsconfig.json", "mypy.ini", ".mypy.ini"]
        for type_file in type_files:
            if os.path.exists(os.path.join(project_path, type_file)):
                features["has_type_checking"] = True
                break
        
        return features
    
    def _identify_issues(self, project_path: str, analysis: Dict) -> List[str]:
        """Identify issues in the project"""
        issues = []
        
        # Check for missing tests
        if not analysis["has_tests"]:
            issues.append("No testing framework detected")
        
        # Check for missing CI/CD
        if not analysis["has_ci_cd"]:
            issues.append("No CI/CD pipeline detected")
        
        # Check for missing documentation
        if not analysis["has_documentation"]:
            issues.append("Insufficient documentation")
        
        # Check for missing security
        if not analysis["has_security"]:
            issues.append("No security configuration detected")
        
        # Check for code quality tools
        if not analysis["has_linting"]:
            issues.append("No linting configuration detected")
        
        if not analysis["has_formatting"]:
            issues.append("No code formatting configuration detected")
        
        # Check for outdated dependencies
        if analysis["dependencies"]["vulnerable"]:
            issues.append(f"Vulnerable dependencies detected: {len(analysis['dependencies']['vulnerable'])}")
        
        # Check for large files
        large_files = self._find_large_files(project_path)
        if large_files:
            issues.append(f"Large files detected: {len(large_files)}")
        
        # Check for code smells
        code_smells = self._detect_code_smells(project_path, analysis)
        if code_smells:
            issues.extend(code_smells)
        
        return issues
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Framework-specific recommendations
        if analysis["framework"] == "react":
            recommendations.extend([
                "Consider migrating to TypeScript for better type safety",
                "Implement React Testing Library for component testing",
                "Add Storybook for component documentation",
                "Consider using React Query for data fetching"
            ])
        elif analysis["framework"] == "fastapi":
            recommendations.extend([
                "Add Pydantic models for request/response validation",
                "Implement async database operations",
                "Add OpenAPI documentation",
                "Consider using SQLAlchemy for database ORM"
            ])
        
        # General recommendations
        if not analysis["has_tests"]:
            recommendations.append("Add comprehensive testing framework")
        
        if not analysis["has_ci_cd"]:
            recommendations.append("Implement CI/CD pipeline with GitHub Actions")
        
        if not analysis["has_docker"]:
            recommendations.append("Add Docker containerization")
        
        if not analysis["has_security"]:
            recommendations.append("Implement security best practices")
        
        if analysis["dependencies"]["total_count"] > 50:
            recommendations.append("Consider dependency audit and cleanup")
        
        return recommendations
    
    def _find_large_files(self, project_path: str) -> List[str]:
        """Find files larger than 1MB"""
        large_files = []
        
        try:
            for root, dirs, files in os.walk(project_path):
                # Skip hidden directories and node_modules
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.getsize(file_path) > 1024 * 1024:  # 1MB
                            large_files.append(os.path.relpath(file_path, project_path))
                    except OSError:
                        continue
                        
        except Exception as e:
            logger.error(f"Error finding large files: {e}")
        
        return large_files
    
    def _detect_code_smells(self, project_path: str, analysis: Dict) -> List[str]:
        """Detect code smells in the project"""
        smells = []
        
        # Check for long files
        long_files = self._find_long_files(project_path)
        if long_files:
            smells.append(f"Long files detected: {len(long_files)}")
        
        # Check for duplicate code
        if analysis["language"] == "python":
            duplicate_code = self._find_python_duplicates(project_path)
            if duplicate_code:
                smells.append(f"Potential duplicate code detected: {len(duplicate_code)}")
        
        # Check for complex functions
        complex_functions = self._find_complex_functions(project_path, analysis["language"])
        if complex_functions:
            smells.append(f"Complex functions detected: {len(complex_functions)}")
        
        return smells
    
    def _find_long_files(self, project_path: str) -> List[str]:
        """Find files longer than 500 lines"""
        long_files = []
        
        try:
            for root, dirs, files in os.walk(project_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
                
                for file in files:
                    if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                line_count = sum(1 for line in f)
                                if line_count > 500:
                                    long_files.append(os.path.relpath(file_path, project_path))
                        except (UnicodeDecodeError, OSError):
                            continue
                            
        except Exception as e:
            logger.error(f"Error finding long files: {e}")
        
        return long_files
    
    def _find_python_duplicates(self, project_path: str) -> List[str]:
        """Find potential duplicate Python code"""
        duplicates = []
        
        # This is a simplified version - in practice, you'd use a proper duplicate detection tool
        try:
            function_signatures = {}
            
            for root, dirs, files in os.walk(project_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
                
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                tree = ast.parse(content)
                                
                                for node in ast.walk(tree):
                                    if isinstance(node, ast.FunctionDef):
                                        # Simple signature based on name and arg count
                                        signature = f"{node.name}_{len(node.args.args)}"
                                        
                                        if signature in function_signatures:
                                            duplicates.append(f"{file_path}:{node.lineno}")
                                        else:
                                            function_signatures[signature] = file_path
                                            
                        except (SyntaxError, UnicodeDecodeError, OSError):
                            continue
                            
        except Exception as e:
            logger.error(f"Error finding Python duplicates: {e}")
        
        return duplicates
    
    def _find_complex_functions(self, project_path: str, language: str) -> List[str]:
        """Find complex functions (simplified cyclomatic complexity)"""
        complex_functions = []
        
        if language == "python":
            complex_functions = self._find_complex_python_functions(project_path)
        elif language == "javascript":
            complex_functions = self._find_complex_js_functions(project_path)
        
        return complex_functions
    
    def _find_complex_python_functions(self, project_path: str) -> List[str]:
        """Find complex Python functions"""
        complex_functions = []
        
        try:
            for root, dirs, files in os.walk(project_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
                
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                                # Simple complexity check based on keywords
                                complexity_keywords = ['if', 'elif', 'for', 'while', 'try', 'except', 'with']
                                
                                for line_num, line in enumerate(content.split('\n'), 1):
                                    if 'def ' in line:
                                        # Check next 20 lines for complexity
                                        function_lines = content.split('\n')[line_num-1:line_num+19]
                                        complexity = sum(1 for l in function_lines 
                                                       for keyword in complexity_keywords 
                                                       if keyword in l)
                                        
                                        if complexity > 10:
                                            complex_functions.append(f"{file_path}:{line_num}")
                                            
                        except (UnicodeDecodeError, OSError):
                            continue
                            
        except Exception as e:
            logger.error(f"Error finding complex Python functions: {e}")
        
        return complex_functions
    
    def _find_complex_js_functions(self, project_path: str) -> List[str]:
        """Find complex JavaScript functions"""
        complex_functions = []
        
        try:
            for root, dirs, files in os.walk(project_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
                
                for file in files:
                    if file.endswith(('.js', '.ts', '.jsx', '.tsx')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                                # Simple complexity check
                                complexity_keywords = ['if', 'else', 'for', 'while', 'switch', 'case', 'try', 'catch']
                                
                                for line_num, line in enumerate(content.split('\n'), 1):
                                    if 'function ' in line or '=>' in line:
                                        # Check next 20 lines for complexity
                                        function_lines = content.split('\n')[line_num-1:line_num+19]
                                        complexity = sum(1 for l in function_lines 
                                                       for keyword in complexity_keywords 
                                                       if keyword in l)
                                        
                                        if complexity > 10:
                                            complex_functions.append(f"{file_path}:{line_num}")
                                            
                        except (UnicodeDecodeError, OSError):
                            continue
                            
        except Exception as e:
            logger.error(f"Error finding complex JavaScript functions: {e}")
        
        return complex_functions
    
    def _create_backup(self, project_path: str) -> str:
        """Create backup of the project"""
        backup_dir = "/mnt/c/bmad-workspace/backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        project_name = os.path.basename(project_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{project_name}_backup_{timestamp}")
        
        try:
            shutil.copytree(project_path, backup_path, ignore=shutil.ignore_patterns(
                'node_modules', '.git', '__pycache__', '*.pyc', '.venv', 'venv'
            ))
            return backup_path
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise
    
    def _restore_backup(self, backup_path: str, project_path: str):
        """Restore from backup"""
        try:
            if os.path.exists(project_path):
                shutil.rmtree(project_path)
            shutil.copytree(backup_path, project_path)
            logger.info(f"Restored from backup: {backup_path}")
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
    
    def _apply_enhancement(self, project_path: str, enhancement: str, analysis: Dict, options: Dict):
        """Apply specific enhancement to the project"""
        
        if enhancement == "ai_integration":
            self._add_ai_integration(project_path, analysis, options)
        elif enhancement == "quality_control":
            self._add_quality_control(project_path, analysis, options)
        elif enhancement == "testing":
            self._add_testing_framework(project_path, analysis, options)
        elif enhancement == "security":
            self._add_security_features(project_path, analysis, options)
        elif enhancement == "ci_cd":
            self._add_ci_cd_pipeline(project_path, analysis, options)
        elif enhancement == "documentation":
            self._add_documentation(project_path, analysis, options)
        elif enhancement == "performance":
            self._add_performance_monitoring(project_path, analysis, options)
        elif enhancement == "monitoring":
            self._add_application_monitoring(project_path, analysis, options)
        elif enhancement == "docker":
            self._add_docker_support(project_path, analysis, options)
        elif enhancement == "typescript":
            self._migrate_to_typescript(project_path, analysis, options)
        elif enhancement == "modern_patterns":
            self._implement_modern_patterns(project_path, analysis, options)
        else:
            logger.warning(f"Unknown enhancement: {enhancement}")
    
    def _add_ai_integration(self, project_path: str, analysis: Dict, options: Dict):
        """Add AI development tools integration"""
        logger.info("Adding AI integration...")
        
        # Generate CLAUDE.md configuration
        claude_config = {
            "project_name": os.path.basename(project_path),
            "project_type": analysis["project_type"],
            "framework": analysis["framework"],
            "language": analysis["language"],
            "version": "1.0.0",
            "ai_tools": [
                "sequential_thinking",
                "perplexity",
                "context7",
                "playwright",
                "github",
                "taskmaster",
                "dart",
                "agentic_tools",
                "memory"
            ],
            "workflow_triggers": [
                {
                    "event": "file_change",
                    "pattern": f"*.{analysis['language'][:2]}",
                    "action": "run_tests"
                },
                {
                    "event": "git_commit",
                    "action": "run_ci_pipeline"
                }
            ],
            "quality_standards": {
                "min_test_coverage": 0.8,
                "max_complexity": 10,
                "security_scan": True,
                "performance_threshold": 2.0
            },
            "development_phases": [
                "planning",
                "development",
                "testing",
                "security_review",
                "deployment"
            ],
            "team_structure": {
                "architect": "AI Agent",
                "frontend": "AI Agent",
                "backend": "AI Agent",
                "qa": "AI Agent",
                "devops": "AI Agent",
                "ceo": "CEO Quality Control Agent"
            }
        }
        
        claude_content = f"""---
{yaml.dump(claude_config, default_flow_style=False)}
---

# {os.path.basename(project_path)}

## AI-Enhanced Development

This project has been enhanced with AI-powered development tools:

### AI Tools Integration
- **Sequential Thinking**: Strategic planning and problem-solving
- **Perplexity**: Real-time research and intelligence gathering
- **Context7**: Documentation and best practices
- **Playwright**: Automated testing and UI interactions
- **GitHub**: Repository management and CI/CD
- **TaskMaster**: Project task management
- **Memory**: Knowledge persistence and learning

### Quality Control
- **CEO Quality Control Agent**: Ensures all work meets quality standards
- **Automated Testing**: Comprehensive test coverage
- **Security Scanning**: Continuous security monitoring
- **Performance Monitoring**: Real-time performance tracking

### Development Workflow
1. All changes are automatically monitored by the CEO Quality Control Agent
2. Quality standards are enforced on every commit
3. Tests run automatically on file changes
4. CI/CD pipeline deploys on successful builds

## Enhanced Features

### Automatic Code Review
The CEO Quality Control Agent automatically reviews all code changes and provides feedback on:
- Code quality and best practices
- Security vulnerabilities
- Performance issues
- Test coverage
- Documentation completeness

### Intelligent Development Assistance
- Real-time research and problem-solving
- Context-aware code suggestions
- Automated documentation generation
- Performance optimization recommendations

### Continuous Learning
The system learns from your development patterns and continuously improves:
- Remembers solutions to common problems
- Adapts to your coding style
- Provides personalized recommendations
- Builds project-specific knowledge base

## Getting Started with AI Development

1. Install Claude Code CLI
2. Configure your API keys
3. Run the CEO Quality Control Agent
4. Start developing with AI assistance!

The AI system will automatically monitor your work and provide guidance throughout the development process.
"""
        
        claude_path = os.path.join(project_path, "CLAUDE.md")
        with open(claude_path, 'w') as f:
            f.write(claude_content)
        
        logger.info("✅ AI integration added")
    
    def _add_quality_control(self, project_path: str, analysis: Dict, options: Dict):
        """Add CEO Quality Control Agent"""
        logger.info("Adding quality control system...")
        
        # Copy CEO Quality Control Agent
        ceo_agent_source = "/mnt/c/bmad-workspace/ceo-quality-control-agent.py"
        ceo_agent_dest = os.path.join(project_path, "scripts", "ceo-quality-control-agent.py")
        
        os.makedirs(os.path.dirname(ceo_agent_dest), exist_ok=True)
        
        if os.path.exists(ceo_agent_source):
            shutil.copy2(ceo_agent_source, ceo_agent_dest)
        
        # Create quality control configuration
        config_dir = os.path.join(project_path, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        quality_config = {
            "quality_standards": {
                "min_overall_score": 0.8,
                "auto_fix_enabled": True,
                "max_revision_attempts": 3,
                "critical_issue_threshold": 0
            },
            "monitoring": {
                "watch_directories": [project_path],
                "file_patterns": ["*.py", "*.js", "*.ts", "*.jsx", "*.tsx"],
                "exclude_patterns": ["*.pyc", "*.log", "node_modules", ".git"]
            },
            "agents": {
                "timeout_seconds": 300,
                "max_concurrent_reviews": 10,
                "escalation_threshold": 3
            },
            "reporting": {
                "daily_reports": True,
                "slack_webhook": None,
                "email_notifications": True
            }
        }
        
        config_path = os.path.join(config_dir, "quality-control-config.yaml")
        with open(config_path, 'w') as f:
            yaml.dump(quality_config, f)
        
        # Create startup script
        startup_script = f"""#!/bin/bash
# CEO Quality Control Agent Startup Script

echo "🎯 Starting CEO Quality Control Agent..."

# Set environment variables
export PROJECT_PATH="{project_path}"
export CONFIG_PATH="{config_path}"

# Start the agent
python scripts/ceo-quality-control-agent.py --config "$CONFIG_PATH"
"""
        
        startup_script_path = os.path.join(project_path, "scripts", "start-quality-control.sh")
        with open(startup_script_path, 'w') as f:
            f.write(startup_script)
        
        os.chmod(startup_script_path, 0o755)
        
        logger.info("✅ Quality control system added")
    
    def _add_testing_framework(self, project_path: str, analysis: Dict, options: Dict):
        """Add comprehensive testing framework"""
        logger.info("Adding testing framework...")
        
        if analysis["language"] == "javascript":
            self._add_javascript_testing(project_path, analysis)
        elif analysis["language"] == "python":
            self._add_python_testing(project_path, analysis)
        
        logger.info("✅ Testing framework added")
    
    def _add_javascript_testing(self, project_path: str, analysis: Dict):
        """Add JavaScript testing framework"""
        
        # Update package.json with testing dependencies
        package_json_path = os.path.join(project_path, "package.json")
        
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            # Add testing dependencies
            dev_dependencies = package_data.setdefault("devDependencies", {})
            dev_dependencies.update({
                "jest": "^29.0.0",
                "@testing-library/jest-dom": "^5.16.0",
                "@testing-library/user-event": "^14.4.0",
                "eslint": "^8.0.0",
                "prettier": "^2.8.0",
                "@typescript-eslint/eslint-plugin": "^5.0.0",
                "@typescript-eslint/parser": "^5.0.0"
            })
            
            if analysis["framework"] == "react":
                dev_dependencies["@testing-library/react"] = "^13.4.0"
            elif analysis["framework"] == "vue":
                dev_dependencies["@vue/test-utils"] = "^2.4.0"
            
            # Add testing scripts
            scripts = package_data.setdefault("scripts", {})
            scripts.update({
                "test": "jest",
                "test:watch": "jest --watch",
                "test:coverage": "jest --coverage",
                "lint": "eslint src --ext .js,.jsx,.ts,.tsx",
                "lint:fix": "eslint src --ext .js,.jsx,.ts,.tsx --fix",
                "format": "prettier --write src/**/*.{js,jsx,ts,tsx,json,css,md}"
            })
            
            with open(package_json_path, 'w') as f:
                json.dump(package_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error updating package.json: {e}")
        
        # Create Jest configuration
        jest_config = {
            "testEnvironment": "jsdom",
            "setupFilesAfterEnv": ["<rootDir>/src/setupTests.js"],
            "testMatch": [
                "**/__tests__/**/*.(js|jsx|ts|tsx)",
                "**/*.(test|spec).(js|jsx|ts|tsx)"
            ],
            "collectCoverageFrom": [
                "src/**/*.{js,jsx,ts,tsx}",
                "!src/**/*.d.ts",
                "!src/index.js"
            ],
            "coverageThreshold": {
                "global": {
                    "branches": 80,
                    "functions": 80,
                    "lines": 80,
                    "statements": 80
                }
            }
        }
        
        jest_config_path = os.path.join(project_path, "jest.config.js")
        with open(jest_config_path, 'w') as f:
            f.write(f"module.exports = {json.dumps(jest_config, indent=2)}")
        
        # Create test setup file
        setup_tests_content = """import '@testing-library/jest-dom';

// Mock common browser APIs
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

global.IntersectionObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));
"""
        
        setup_tests_path = os.path.join(project_path, "src", "setupTests.js")
        os.makedirs(os.path.dirname(setup_tests_path), exist_ok=True)
        
        with open(setup_tests_path, 'w') as f:
            f.write(setup_tests_content)
    
    def _add_python_testing(self, project_path: str, analysis: Dict):
        """Add Python testing framework"""
        
        # Create or update requirements-dev.txt
        dev_requirements = [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "ruff>=0.0.270",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0"
        ]
        
        if analysis["framework"] == "fastapi":
            dev_requirements.extend([
                "httpx>=0.24.0",
                "pytest-asyncio>=0.21.0"
            ])
        elif analysis["framework"] == "flask":
            dev_requirements.append("pytest-flask>=1.2.0")
        elif analysis["framework"] == "django":
            dev_requirements.append("pytest-django>=4.5.0")
        
        requirements_dev_path = os.path.join(project_path, "requirements-dev.txt")
        with open(requirements_dev_path, 'w') as f:
            f.write('\n'.join(dev_requirements))
        
        # Create pytest configuration
        pytest_config = """[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --cov=src --cov-report=html --cov-report=term-missing"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/venv/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
"""
        
        pyproject_path = os.path.join(project_path, "pyproject.toml")
        with open(pyproject_path, 'w') as f:
            f.write(pytest_config)
        
        # Create sample test file
        test_dir = os.path.join(project_path, "tests")
        os.makedirs(test_dir, exist_ok=True)
        
        test_content = """import pytest
from src.main import app  # Adjust import based on your structure

def test_example():
    \"\"\"Example test to verify testing framework works\"\"\"
    assert 1 + 1 == 2

class TestApplication:
    \"\"\"Test class for application-specific tests\"\"\"
    
    def test_app_exists(self):
        \"\"\"Test that the application exists\"\"\"
        assert app is not None
    
    def test_app_configuration(self):
        \"\"\"Test application configuration\"\"\"
        # Add your configuration tests here
        pass
"""
        
        test_file_path = os.path.join(test_dir, "test_main.py")
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        
        # Create __init__.py
        init_file_path = os.path.join(test_dir, "__init__.py")
        with open(init_file_path, 'w') as f:
            f.write("")
    
    def _add_security_features(self, project_path: str, analysis: Dict, options: Dict):
        """Add security features"""
        logger.info("Adding security features...")
        
        # Create security policy
        security_policy = """# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

1. **Email**: security@company.com
2. **GitHub**: Create a private security advisory

## Security Measures

This project implements the following security measures:

### Authentication & Authorization
- Secure authentication mechanisms
- Role-based access control
- Session management
- Token-based authentication

### Input Validation
- Request validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection

### Data Protection
- Encryption at rest and in transit
- Secure data storage
- Privacy compliance
- Data anonymization

### Infrastructure Security
- HTTPS enforcement
- Security headers
- Rate limiting
- Input size limits

## Security Checklist

- [ ] All inputs are validated and sanitized
- [ ] Authentication is properly implemented
- [ ] Authorization checks are in place
- [ ] Sensitive data is encrypted
- [ ] Security headers are configured
- [ ] Dependencies are up to date
- [ ] Security tests are included
- [ ] Logging and monitoring are in place

## Dependencies

We regularly update dependencies to address security vulnerabilities:

- Automated dependency updates
- Security scanning in CI/CD
- Vulnerability monitoring
- Regular security audits
"""
        
        security_policy_path = os.path.join(project_path, "SECURITY.md")
        with open(security_policy_path, 'w') as f:
            f.write(security_policy)
        
        # Create security workflow
        workflows_dir = os.path.join(project_path, ".github", "workflows")
        os.makedirs(workflows_dir, exist_ok=True)
        
        security_workflow = """name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 1'  # Weekly Monday at 2 AM

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run CodeQL Analysis
      uses: github/codeql-action/analyze@v2
"""
        
        security_workflow_path = os.path.join(workflows_dir, "security.yml")
        with open(security_workflow_path, 'w') as f:
            f.write(security_workflow)
        
        logger.info("✅ Security features added")
    
    def _add_ci_cd_pipeline(self, project_path: str, analysis: Dict, options: Dict):
        """Add CI/CD pipeline"""
        logger.info("Adding CI/CD pipeline...")
        
        workflows_dir = os.path.join(project_path, ".github", "workflows")
        os.makedirs(workflows_dir, exist_ok=True)
        
        if analysis["language"] == "javascript":
            workflow_content = self._get_javascript_workflow(analysis)
        elif analysis["language"] == "python":
            workflow_content = self._get_python_workflow(analysis)
        else:
            workflow_content = self._get_generic_workflow()
        
        workflow_path = os.path.join(workflows_dir, "ci-cd.yml")
        with open(workflow_path, 'w') as f:
            f.write(workflow_content)
        
        logger.info("✅ CI/CD pipeline added")
    
    def _get_javascript_workflow(self, analysis: Dict) -> str:
        """Get JavaScript CI/CD workflow"""
        return f"""name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18, 20]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: ${{{{ matrix.node-version }}}}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint
    
    - name: Run tests
      run: npm run test:coverage
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info
    
    - name: Build application
      run: npm run build

  security:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Run security audit
      run: npm audit --audit-level moderate

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Deploy to production
      run: echo "Add your deployment commands here"
"""
    
    def _get_python_workflow(self, analysis: Dict) -> str:
        """Get Python CI/CD workflow"""
        return f"""name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{{{ matrix.python-version }}}}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linter
      run: |
        ruff check src
        black --check src
    
    - name: Run type checker
      run: mypy src
    
    - name: Run tests
      run: pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Run security scan
      run: |
        pip install safety bandit
        safety check
        bandit -r src

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Deploy to production
      run: echo "Add your deployment commands here"
"""
    
    def _get_generic_workflow(self) -> str:
        """Get generic CI/CD workflow"""
        return """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Build and test
      run: |
        echo "Add your build and test commands here"
    
    - name: Security scan
      run: |
        echo "Add your security scan commands here"
    
    - name: Deploy
      if: github.ref == 'refs/heads/main'
      run: |
        echo "Add your deployment commands here"
"""
    
    def _add_documentation(self, project_path: str, analysis: Dict, options: Dict):
        """Add comprehensive documentation"""
        logger.info("Adding documentation...")
        
        # Create docs directory
        docs_dir = os.path.join(project_path, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        
        # Enhanced README
        readme_content = f"""# {os.path.basename(project_path)}

## Overview

This is a {analysis['framework']} application enhanced with AI-powered development tools.

## Features

- 🚀 Modern {analysis['framework']} architecture
- 🧠 AI-powered development with Claude Code
- 🔍 Automated quality control
- 🧪 Comprehensive testing suite
- 🔒 Security scanning and monitoring
- 📈 Performance optimization
- 🚢 CI/CD pipeline

## Quick Start

### Prerequisites

- {analysis['language'].title()} runtime
- Package manager ({analysis['package_manager']})
- Git

### Installation

1. Clone the repository
2. Install dependencies: `{self._get_install_command(analysis)}`
3. Start development server: `{self._get_dev_command(analysis)}`

## Development

### Project Structure

```
{os.path.basename(project_path)}/
├── src/                 # Source code
├── tests/              # Test files
├── docs/               # Documentation
├── scripts/            # Build scripts
├── .github/            # CI/CD workflows
├── CLAUDE.md          # AI configuration
└── README.md          # This file
```

### Development Workflow

1. Make changes to your code
2. The CEO Quality Control Agent automatically reviews your work
3. Address any quality issues
4. Tests run automatically
5. CI/CD pipeline handles deployment

### Testing

Run tests: `{self._get_test_command(analysis)}`

### Quality Control

This project uses the CEO Quality Control Agent to ensure code quality:

- Automatic code review
- Quality standard enforcement
- Security scanning
- Performance monitoring

## Architecture

The application follows modern architectural principles:

- Separation of concerns
- Single responsibility principle
- Dependency injection
- Test-driven development

## API Documentation

[Add API documentation here]

## Deployment

[Add deployment instructions here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure tests pass
5. Submit a pull request

## License

[Add license information here]
"""
        
        readme_path = os.path.join(project_path, "README.md")
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        logger.info("✅ Documentation added")
    
    def _get_install_command(self, analysis: Dict) -> str:
        """Get installation command based on language"""
        commands = {
            "javascript": "npm install",
            "python": "pip install -r requirements.txt",
            "go": "go mod download",
            "rust": "cargo build"
        }
        return commands.get(analysis["language"], "# Add install command")
    
    def _get_dev_command(self, analysis: Dict) -> str:
        """Get development command based on language"""
        commands = {
            "javascript": "npm run dev",
            "python": "python main.py",
            "go": "go run main.go",
            "rust": "cargo run"
        }
        return commands.get(analysis["language"], "# Add dev command")
    
    def _get_test_command(self, analysis: Dict) -> str:
        """Get test command based on language"""
        commands = {
            "javascript": "npm test",
            "python": "pytest",
            "go": "go test ./...",
            "rust": "cargo test"
        }
        return commands.get(analysis["language"], "# Add test command")
    
    def _add_performance_monitoring(self, project_path: str, analysis: Dict, options: Dict):
        """Add performance monitoring"""
        logger.info("Adding performance monitoring...")
        
        # Create performance monitoring configuration
        perf_config = {
            "monitoring": {
                "enabled": True,
                "metrics": ["response_time", "memory_usage", "cpu_usage"],
                "alerts": {
                    "response_time_threshold": 2.0,
                    "memory_usage_threshold": 0.8,
                    "cpu_usage_threshold": 0.8
                }
            },
            "logging": {
                "level": "INFO",
                "format": "json",
                "destination": "stdout"
            }
        }
        
        config_dir = os.path.join(project_path, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        perf_config_path = os.path.join(config_dir, "performance.yaml")
        with open(perf_config_path, 'w') as f:
            yaml.dump(perf_config, f)
        
        logger.info("✅ Performance monitoring added")
    
    def _add_application_monitoring(self, project_path: str, analysis: Dict, options: Dict):
        """Add application monitoring"""
        logger.info("Adding application monitoring...")
        
        # Create monitoring configuration
        monitoring_config = {
            "monitoring": {
                "health_check": {
                    "enabled": True,
                    "endpoint": "/health",
                    "interval": 30
                },
                "metrics": {
                    "enabled": True,
                    "endpoint": "/metrics",
                    "collectors": ["default", "custom"]
                },
                "alerts": {
                    "enabled": True,
                    "channels": ["email", "slack"],
                    "rules": [
                        {
                            "name": "high_error_rate",
                            "condition": "error_rate > 0.05",
                            "severity": "warning"
                        }
                    ]
                }
            }
        }
        
        config_dir = os.path.join(project_path, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        monitoring_config_path = os.path.join(config_dir, "monitoring.yaml")
        with open(monitoring_config_path, 'w') as f:
            yaml.dump(monitoring_config, f)
        
        logger.info("✅ Application monitoring added")
    
    def _add_docker_support(self, project_path: str, analysis: Dict, options: Dict):
        """Add Docker support"""
        logger.info("Adding Docker support...")
        
        # Create Dockerfile
        if analysis["language"] == "javascript":
            dockerfile_content = self._get_node_dockerfile(analysis)
        elif analysis["language"] == "python":
            dockerfile_content = self._get_python_dockerfile(analysis)
        else:
            dockerfile_content = self._get_generic_dockerfile()
        
        dockerfile_path = os.path.join(project_path, "Dockerfile")
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        # Create docker-compose.yml
        docker_compose_content = self._get_docker_compose_content(analysis)
        
        compose_path = os.path.join(project_path, "docker-compose.yml")
        with open(compose_path, 'w') as f:
            f.write(docker_compose_content)
        
        # Create .dockerignore
        dockerignore_content = """node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.env.local
.env.production
.env.staging
coverage
.nyc_output
*.log
"""
        
        dockerignore_path = os.path.join(project_path, ".dockerignore")
        with open(dockerignore_path, 'w') as f:
            f.write(dockerignore_content)
        
        logger.info("✅ Docker support added")
    
    def _get_node_dockerfile(self, analysis: Dict) -> str:
        """Get Node.js Dockerfile"""
        return """# Multi-stage build for Node.js
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S appuser -u 1001

# Change ownership
RUN chown -R appuser:nodejs /app
USER appuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:3000/health || exit 1

# Start application
CMD ["npm", "start"]
"""
    
    def _get_python_dockerfile(self, analysis: Dict) -> str:
        """Get Python Dockerfile"""
        return """# Python application Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements*.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "main.py"]
"""
    
    def _get_generic_dockerfile(self) -> str:
        """Get generic Dockerfile"""
        return """# Generic Dockerfile
FROM alpine:latest

WORKDIR /app

# Copy application
COPY . .

# Install dependencies
RUN echo "Add your build commands here"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD echo "Add your health check here"

# Start application
CMD ["echo", "Add your start command here"]
"""
    
    def _get_docker_compose_content(self, analysis: Dict) -> str:
        """Get Docker Compose content"""
        if analysis["language"] == "python":
            return """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=1
      - DATABASE_URL=postgresql://user:password@db:5432/appdb
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
"""
        else:
            return """version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
"""
    
    def _migrate_to_typescript(self, project_path: str, analysis: Dict, options: Dict):
        """Migrate JavaScript project to TypeScript"""
        logger.info("Migrating to TypeScript...")
        
        if analysis["language"] != "javascript":
            logger.warning("TypeScript migration only supported for JavaScript projects")
            return
        
        # Add TypeScript dependencies
        package_json_path = os.path.join(project_path, "package.json")
        
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            dev_dependencies = package_data.setdefault("devDependencies", {})
            dev_dependencies.update({
                "typescript": "^5.0.0",
                "@types/node": "^20.0.0",
                "@typescript-eslint/eslint-plugin": "^5.0.0",
                "@typescript-eslint/parser": "^5.0.0"
            })
            
            if analysis["framework"] == "react":
                dev_dependencies.update({
                    "@types/react": "^18.0.0",
                    "@types/react-dom": "^18.0.0"
                })
            
            with open(package_json_path, 'w') as f:
                json.dump(package_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error updating package.json: {e}")
        
        # Create TypeScript configuration
        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "lib": ["DOM", "DOM.Iterable", "ES6"],
                "allowJs": True,
                "skipLibCheck": True,
                "esModuleInterop": True,
                "allowSyntheticDefaultImports": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "noFallthroughCasesInSwitch": True,
                "module": "esnext",
                "moduleResolution": "node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx" if analysis["framework"] == "react" else "preserve"
            },
            "include": [
                "src",
                "**/*.ts",
                "**/*.tsx"
            ],
            "exclude": [
                "node_modules",
                "build",
                "dist"
            ]
        }
        
        tsconfig_path = os.path.join(project_path, "tsconfig.json")
        with open(tsconfig_path, 'w') as f:
            json.dump(tsconfig, f, indent=2)
        
        logger.info("✅ TypeScript migration setup complete")
    
    def _implement_modern_patterns(self, project_path: str, analysis: Dict, options: Dict):
        """Implement modern development patterns"""
        logger.info("Implementing modern patterns...")
        
        # Create coding standards document
        standards_content = f"""# Coding Standards

## General Principles

- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **YAGNI**: You Aren't Gonna Need It

## {analysis['language'].title()} Specific Standards

### Code Style
- Use consistent indentation (2 spaces for JS/TS, 4 spaces for Python)
- Use meaningful variable and function names
- Keep functions small and focused
- Add comments for complex logic

### Error Handling
- Always handle errors explicitly
- Use specific error types
- Provide meaningful error messages
- Log errors appropriately

### Testing
- Write tests for all public APIs
- Use descriptive test names
- Test edge cases and error conditions
- Maintain high test coverage

### Performance
- Avoid premature optimization
- Profile before optimizing
- Use appropriate data structures
- Consider memory usage

### Security
- Validate all inputs
- Use parameterized queries
- Implement proper authentication
- Keep dependencies updated

## Code Review Guidelines

- Review for correctness
- Check for security vulnerabilities
- Verify test coverage
- Ensure code follows standards
- Provide constructive feedback

## Deployment

- Use environment variables for configuration
- Implement health checks
- Use proper logging
- Monitor application metrics
"""
        
        standards_path = os.path.join(project_path, "CODING_STANDARDS.md")
        with open(standards_path, 'w') as f:
            f.write(standards_content)
        
        logger.info("✅ Modern patterns implemented")
    
    def _generate_enhancement_report(self, project_path: str, enhancements: List[str], analysis: Dict):
        """Generate enhancement report"""
        logger.info("Generating enhancement report...")
        
        report = {
            "project_path": project_path,
            "enhancement_date": datetime.now().isoformat(),
            "applied_enhancements": enhancements,
            "project_analysis": analysis,
            "recommendations": [
                "Run the setup script to complete installation",
                "Review the generated configuration files",
                "Update environment variables",
                "Run tests to verify everything works",
                "Start the CEO Quality Control Agent",
                "Begin developing with AI assistance"
            ]
        }
        
        report_path = os.path.join(project_path, "ENHANCEMENT_REPORT.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate human-readable report
        readable_report = f"""# Enhancement Report

## Project Enhanced: {os.path.basename(project_path)}

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Applied Enhancements

{chr(10).join(f"- {enhancement}: {self.enhancements[enhancement]}" for enhancement in enhancements)}

## Project Analysis

- **Type**: {analysis['project_type']}
- **Framework**: {analysis['framework']}
- **Language**: {analysis['language']}
- **Total Files**: {analysis['file_structure']['total_files']}
- **Code Files**: {analysis['file_structure']['code_files']}
- **Test Files**: {analysis['file_structure']['test_files']}

## New Features

- 🧠 AI-powered development with Claude Code
- 🔍 CEO Quality Control Agent for automatic code review
- 🧪 Comprehensive testing framework
- 🔒 Security scanning and monitoring
- 🚢 CI/CD pipeline with GitHub Actions
- 📊 Performance and application monitoring
- 🐳 Docker containerization
- 📚 Enhanced documentation

## Next Steps

1. **Install Dependencies**: Run the setup script
2. **Configure Environment**: Update .env file with your settings
3. **Start Quality Control**: Run the CEO Quality Control Agent
4. **Run Tests**: Verify everything works
5. **Start Development**: Begin coding with AI assistance!

## Quality Control

The CEO Quality Control Agent will:
- Monitor all code changes
- Enforce quality standards
- Provide improvement suggestions
- Ensure security best practices
- Track performance metrics

## Development Workflow

1. Make changes to your code
2. AI system automatically reviews your work
3. Address any quality issues
4. Tests run automatically
5. CI/CD pipeline handles deployment

## Support

Your project is now enhanced with AI development tools! The system will guide you through the development process and ensure high-quality code.

Happy coding! 🚀
"""
        
        readable_report_path = os.path.join(project_path, "ENHANCEMENT_REPORT.md")
        with open(readable_report_path, 'w') as f:
            f.write(readable_report)
        
        logger.info("✅ Enhancement report generated")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Enhance existing application with AI development tools')
    parser.add_argument('--path', required=True, help='Path to existing project')
    parser.add_argument('--enhancements', nargs='+', required=True,
                       choices=['ai_integration', 'quality_control', 'testing', 'security', 'ci_cd', 
                               'documentation', 'performance', 'monitoring', 'docker', 'typescript', 'modern_patterns'],
                       help='Enhancements to apply')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze the project, don\'t apply enhancements')
    parser.add_argument('--backup', action='store_true', help='Create backup before enhancement')
    parser.add_argument('--force', action='store_true', help='Force enhancement without confirmation')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        logger.error(f"Project path does not exist: {args.path}")
        sys.exit(1)
    
    enhancer = ExistingAppEnhancementTemplate()
    
    try:
        if args.analyze_only:
            # Only analyze the project
            analysis = enhancer.analyze_project(args.path)
            
            logger.info(f"""
🔍 Project Analysis Complete!

📊 Project Details:
- Type: {analysis['project_type']}
- Framework: {analysis['framework']}
- Language: {analysis['language']}
- Package Manager: {analysis['package_manager']}

📁 File Structure:
- Total Files: {analysis['file_structure']['total_files']}
- Code Files: {analysis['file_structure']['code_files']}
- Test Files: {analysis['file_structure']['test_files']}
- Documentation Files: {analysis['file_structure']['documentation_files']}

✅ Existing Features:
- Tests: {'Yes' if analysis['has_tests'] else 'No'}
- CI/CD: {'Yes' if analysis['has_ci_cd'] else 'No'}
- Docker: {'Yes' if analysis['has_docker'] else 'No'}
- Security: {'Yes' if analysis['has_security'] else 'No'}
- Documentation: {'Yes' if analysis['has_documentation'] else 'No'}

⚠️ Issues Found:
{chr(10).join(f"- {issue}" for issue in analysis['issues'])}

💡 Recommendations:
{chr(10).join(f"- {rec}" for rec in analysis['recommendations'])}

🎯 Suggested Enhancements:
{chr(10).join(f"- {key}: {value}" for key, value in enhancer.enhancements.items())}
""")
        else:
            # Apply enhancements
            if not args.force:
                logger.info(f"About to enhance project: {args.path}")
                logger.info(f"Selected enhancements: {', '.join(args.enhancements)}")
                
                confirm = input("Continue? (y/N): ")
                if confirm.lower() != 'y':
                    logger.info("Enhancement cancelled")
                    sys.exit(0)
            
            options = {
                'backup': args.backup,
                'force': args.force
            }
            
            enhanced_path = enhancer.enhance_project(args.path, args.enhancements, options)
            
            logger.info(f"""
🎉 Project Enhancement Complete!

📁 Enhanced Project: {enhanced_path}
⚡ Applied Enhancements: {', '.join(args.enhancements)}

🎯 Next Steps:
1. Review the enhancement report: {os.path.join(enhanced_path, 'ENHANCEMENT_REPORT.md')}
2. Run setup script: cd {enhanced_path} && ./scripts/setup.sh
3. Configure environment variables
4. Start the CEO Quality Control Agent
5. Begin developing with AI assistance!

🧠 AI Features Now Available:
- CEO Quality Control Agent monitors your code
- Sequential thinking for complex problems
- Real-time research with Perplexity
- Automated testing with Playwright
- Continuous improvement with memory

🚀 Your project is now AI-enhanced and ready for next-level development!
""")
    
    except Exception as e:
        logger.error(f"Enhancement failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()