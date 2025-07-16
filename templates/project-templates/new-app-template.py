#!/usr/bin/env python3
"""
New App Template Generator
==========================

Creates a complete new application project with:
- Modern project structure
- CLAUDE.md configuration
- CI/CD pipeline setup
- Testing framework
- Documentation
- Security best practices

Usage:
    python new-app-template.py --name my-app --type web --framework react
"""

import os
import sys
import json
import yaml
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewAppTemplateGenerator:
    """Generator for new application templates"""
    
    def __init__(self):
        self.templates_dir = Path("/mnt/c/bmad-workspace/templates")
        self.project_types = {
            "web": {
                "frameworks": ["react", "vue", "angular", "svelte", "next", "nuxt"],
                "backend": ["node", "python", "go", "rust", "java"]
            },
            "mobile": {
                "frameworks": ["react-native", "flutter", "ionic", "native"],
                "platforms": ["ios", "android", "cross-platform"]
            },
            "api": {
                "frameworks": ["fastapi", "express", "gin", "spring", "flask"],
                "databases": ["postgresql", "mongodb", "redis", "sqlite"]
            },
            "desktop": {
                "frameworks": ["electron", "tauri", "flutter", "qt", "gtk"],
                "platforms": ["windows", "macos", "linux", "cross-platform"]
            },
            "cli": {
                "frameworks": ["click", "commander", "cobra", "clap"],
                "languages": ["python", "javascript", "go", "rust"]
            },
            "saas": {
                "frameworks": ["next", "nuxt", "remix", "sveltekit"],
                "features": ["auth", "payments", "analytics", "monitoring"]
            },
            "ai": {
                "frameworks": ["pytorch", "tensorflow", "huggingface", "langchain"],
                "types": ["llm", "ml", "cv", "nlp", "robotics"]
            }
        }
    
    def generate_project(self, name: str, project_type: str, framework: str, options: Dict) -> str:
        """Generate a new project"""
        logger.info(f"🚀 Generating new {project_type} project: {name}")
        
        # Create project directory
        project_dir = f"/mnt/c/bmad-workspace/projects/{name}"
        os.makedirs(project_dir, exist_ok=True)
        
        # Generate project structure
        self._create_project_structure(project_dir, project_type, framework)
        
        # Generate CLAUDE.md configuration
        self._generate_claude_config(project_dir, name, project_type, framework, options)
        
        # Generate package configuration
        self._generate_package_config(project_dir, name, project_type, framework)
        
        # Generate CI/CD configuration
        self._generate_cicd_config(project_dir, project_type, framework)
        
        # Generate documentation
        self._generate_documentation(project_dir, name, project_type, framework)
        
        # Generate tests
        self._generate_tests(project_dir, project_type, framework)
        
        # Generate security configuration
        self._generate_security_config(project_dir, project_type, framework)
        
        # Generate development scripts
        self._generate_dev_scripts(project_dir, project_type, framework)
        
        # Initialize git repository
        self._initialize_git(project_dir)
        
        logger.info(f"✅ Project {name} generated successfully at {project_dir}")
        return project_dir
    
    def _create_project_structure(self, project_dir: str, project_type: str, framework: str):
        """Create the project directory structure"""
        structures = {
            "web": {
                "react": [
                    "src/components", "src/hooks", "src/utils", "src/contexts",
                    "src/pages", "src/api", "src/assets", "src/styles",
                    "public", "tests", "docs", "scripts", ".github/workflows"
                ],
                "vue": [
                    "src/components", "src/views", "src/store", "src/router",
                    "src/composables", "src/utils", "src/assets", "src/styles",
                    "public", "tests", "docs", "scripts", ".github/workflows"
                ],
                "angular": [
                    "src/app", "src/assets", "src/environments", "src/styles",
                    "src/app/components", "src/app/services", "src/app/guards",
                    "src/app/interceptors", "src/app/models", "src/app/utils",
                    "tests", "docs", "scripts", ".github/workflows"
                ],
                "next": [
                    "src/app", "src/components", "src/lib", "src/hooks",
                    "src/utils", "src/types", "src/styles", "src/api",
                    "public", "tests", "docs", "scripts", ".github/workflows"
                ]
            },
            "api": {
                "fastapi": [
                    "src/api", "src/models", "src/schemas", "src/services",
                    "src/database", "src/auth", "src/utils", "src/config",
                    "tests", "docs", "scripts", "migrations", ".github/workflows"
                ],
                "express": [
                    "src/routes", "src/controllers", "src/models", "src/middleware",
                    "src/services", "src/utils", "src/config", "src/database",
                    "tests", "docs", "scripts", ".github/workflows"
                ]
            },
            "mobile": {
                "react-native": [
                    "src/components", "src/screens", "src/navigation", "src/services",
                    "src/utils", "src/hooks", "src/contexts", "src/assets",
                    "android", "ios", "tests", "docs", "scripts", ".github/workflows"
                ],
                "flutter": [
                    "lib/screens", "lib/widgets", "lib/services", "lib/models",
                    "lib/utils", "lib/providers", "lib/constants", "lib/themes",
                    "assets", "test", "docs", "scripts", ".github/workflows"
                ]
            },
            "cli": {
                "click": [
                    "src/commands", "src/utils", "src/config", "src/models",
                    "tests", "docs", "scripts", ".github/workflows"
                ],
                "commander": [
                    "src/commands", "src/utils", "src/config", "src/lib",
                    "tests", "docs", "scripts", ".github/workflows"
                ]
            },
            "saas": {
                "next": [
                    "src/app", "src/components", "src/lib", "src/hooks",
                    "src/utils", "src/types", "src/styles", "src/api",
                    "src/auth", "src/payments", "src/analytics", "src/monitoring",
                    "public", "tests", "docs", "scripts", ".github/workflows"
                ]
            },
            "ai": {
                "pytorch": [
                    "src/models", "src/data", "src/training", "src/inference",
                    "src/utils", "src/config", "notebooks", "experiments",
                    "tests", "docs", "scripts", ".github/workflows"
                ],
                "langchain": [
                    "src/chains", "src/agents", "src/tools", "src/prompts",
                    "src/memory", "src/utils", "src/config", "src/data",
                    "tests", "docs", "scripts", ".github/workflows"
                ]
            }
        }
        
        # Get structure for project type and framework
        structure = structures.get(project_type, {}).get(framework, [
            "src", "tests", "docs", "scripts", ".github/workflows"
        ])
        
        # Create directories
        for directory in structure:
            dir_path = os.path.join(project_dir, directory)
            os.makedirs(dir_path, exist_ok=True)
            
            # Create .gitkeep for empty directories
            gitkeep_path = os.path.join(dir_path, ".gitkeep")
            if not os.listdir(dir_path):
                with open(gitkeep_path, 'w') as f:
                    f.write("")
    
    def _generate_claude_config(self, project_dir: str, name: str, project_type: str, framework: str, options: Dict):
        """Generate CLAUDE.md configuration"""
        config = {
            "project_name": name,
            "project_type": project_type,
            "framework": framework,
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
                    "pattern": "*.py",
                    "action": "run_tests"
                },
                {
                    "event": "file_change", 
                    "pattern": "*.js",
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
        
        # Add framework-specific configurations
        if framework == "react":
            config["dependencies"] = {
                "react": "^18.0.0",
                "react-dom": "^18.0.0",
                "typescript": "^5.0.0",
                "vite": "^4.0.0"
            }
            config["scripts"] = {
                "dev": "vite",
                "build": "vite build",
                "test": "vitest",
                "lint": "eslint src --ext ts,tsx"
            }
        elif framework == "fastapi":
            config["dependencies"] = {
                "fastapi": "^0.100.0",
                "uvicorn": "^0.23.0",
                "pydantic": "^2.0.0",
                "sqlalchemy": "^2.0.0"
            }
            config["scripts"] = {
                "dev": "uvicorn main:app --reload",
                "test": "pytest",
                "lint": "ruff check src"
            }
        elif framework == "next":
            config["dependencies"] = {
                "next": "^13.0.0",
                "react": "^18.0.0",
                "react-dom": "^18.0.0",
                "typescript": "^5.0.0"
            }
            config["scripts"] = {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "test": "jest",
                "lint": "next lint"
            }
        
        # Generate CLAUDE.md content
        claude_content = f"""---
{yaml.dump(config, default_flow_style=False)}
---

# {name}

## Overview

{name} is a modern {project_type} application built with {framework} and powered by AI development tools.

## Features

- Modern {framework} architecture
- Comprehensive testing suite
- CI/CD pipeline with GitHub Actions
- Security scanning and monitoring
- Performance optimization
- Automated documentation
- Quality control with CEO Agent

## Development

This project uses AI-powered development with the following tools:

### Core AI Tools
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

## Getting Started

### Prerequisites
- Node.js 18+ (for web projects)
- Python 3.9+ (for Python projects)
- Git
- Claude Code CLI
- Redis (for memory management)

### Installation
1. Clone the repository
2. Install dependencies: `npm install` or `pip install -r requirements.txt`
3. Setup environment variables
4. Run development server: `npm run dev` or `python main.py`

### Development Workflow
1. All changes are automatically monitored by the CEO Quality Control Agent
2. Quality standards are enforced on every commit
3. Tests run automatically on file changes
4. CI/CD pipeline deploys on successful builds

## Architecture

The project follows modern architectural principles:

- **Separation of Concerns**: Clear separation between layers
- **Single Responsibility**: Each component has a single purpose
- **Dependency Injection**: Loose coupling between components
- **Test-Driven Development**: Tests written before implementation
- **Continuous Integration**: Automated testing and deployment

## Contributing

This project uses AI-powered development with quality control:

1. Make changes in your local environment
2. The CEO Quality Control Agent will automatically review your work
3. Follow the feedback provided for any quality issues
4. Commit when quality standards are met
5. Create pull requests for review

## License

MIT License - see LICENSE file for details
"""
        
        claude_path = os.path.join(project_dir, "CLAUDE.md")
        with open(claude_path, 'w') as f:
            f.write(claude_content)
    
    def _generate_package_config(self, project_dir: str, name: str, project_type: str, framework: str):
        """Generate package configuration files"""
        
        if framework in ["react", "vue", "angular", "next", "svelte"]:
            # Generate package.json
            package_json = {
                "name": name,
                "version": "1.0.0",
                "description": f"Modern {project_type} application built with {framework}",
                "main": "src/index.js",
                "scripts": self._get_npm_scripts(framework),
                "dependencies": self._get_dependencies(framework),
                "devDependencies": self._get_dev_dependencies(framework),
                "keywords": [project_type, framework, "ai-powered", "modern"],
                "author": "AI Development Team",
                "license": "MIT",
                "engines": {
                    "node": ">=18.0.0",
                    "npm": ">=8.0.0"
                }
            }
            
            package_path = os.path.join(project_dir, "package.json")
            with open(package_path, 'w') as f:
                json.dump(package_json, f, indent=2)
            
            # Generate TypeScript config
            if framework in ["react", "vue", "angular", "next"]:
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
                        "jsx": "react-jsx" if framework == "react" else "preserve"
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
                
                tsconfig_path = os.path.join(project_dir, "tsconfig.json")
                with open(tsconfig_path, 'w') as f:
                    json.dump(tsconfig, f, indent=2)
        
        elif framework in ["fastapi", "flask", "django"]:
            # Generate requirements.txt
            requirements = self._get_python_requirements(framework)
            
            requirements_path = os.path.join(project_dir, "requirements.txt")
            with open(requirements_path, 'w') as f:
                f.write('\n'.join(requirements))
            
            # Generate pyproject.toml
            pyproject = {
                "build-system": {
                    "requires": ["setuptools>=45", "wheel"],
                    "build-backend": "setuptools.build_meta"
                },
                "project": {
                    "name": name,
                    "version": "1.0.0",
                    "description": f"Modern {project_type} application built with {framework}",
                    "authors": [{"name": "AI Development Team"}],
                    "license": {"text": "MIT"},
                    "requires-python": ">=3.9",
                    "dependencies": requirements,
                    "classifiers": [
                        "Development Status :: 4 - Beta",
                        "Intended Audience :: Developers",
                        "License :: OSI Approved :: MIT License",
                        "Programming Language :: Python :: 3",
                        "Programming Language :: Python :: 3.9",
                        "Programming Language :: Python :: 3.10",
                        "Programming Language :: Python :: 3.11"
                    ]
                },
                "tool": {
                    "pytest": {
                        "testpaths": ["tests"],
                        "python_files": ["test_*.py"],
                        "python_classes": ["Test*"],
                        "python_functions": ["test_*"],
                        "addopts": "--cov=src --cov-report=html --cov-report=term-missing"
                    },
                    "ruff": {
                        "line-length": 88,
                        "target-version": "py39",
                        "select": ["E", "F", "I", "N", "W", "UP"],
                        "ignore": ["E501"]
                    },
                    "black": {
                        "line-length": 88,
                        "target-version": ["py39"]
                    }
                }
            }
            
            pyproject_path = os.path.join(project_dir, "pyproject.toml")
            with open(pyproject_path, 'w') as f:
                import toml
                toml.dump(pyproject, f)
    
    def _get_npm_scripts(self, framework: str) -> Dict[str, str]:
        """Get npm scripts for framework"""
        base_scripts = {
            "test": "jest",
            "test:watch": "jest --watch",
            "test:coverage": "jest --coverage",
            "lint": "eslint src --ext .js,.jsx,.ts,.tsx",
            "lint:fix": "eslint src --ext .js,.jsx,.ts,.tsx --fix",
            "format": "prettier --write src/**/*.{js,jsx,ts,tsx,json,css,md}",
            "type-check": "tsc --noEmit"
        }
        
        framework_scripts = {
            "react": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "vue": {
                "dev": "vue-cli-service serve",
                "build": "vue-cli-service build"
            },
            "angular": {
                "dev": "ng serve",
                "build": "ng build",
                "e2e": "ng e2e"
            },
            "next": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start"
            }
        }
        
        return {**base_scripts, **framework_scripts.get(framework, {})}
    
    def _get_dependencies(self, framework: str) -> Dict[str, str]:
        """Get dependencies for framework"""
        deps = {
            "react": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "vue": {
                "vue": "^3.3.0",
                "vue-router": "^4.2.0",
                "pinia": "^2.1.0"
            },
            "angular": {
                "@angular/core": "^16.0.0",
                "@angular/common": "^16.0.0",
                "@angular/router": "^16.0.0",
                "@angular/forms": "^16.0.0"
            },
            "next": {
                "next": "^13.4.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            }
        }
        
        return deps.get(framework, {})
    
    def _get_dev_dependencies(self, framework: str) -> Dict[str, str]:
        """Get dev dependencies for framework"""
        base_deps = {
            "typescript": "^5.0.0",
            "jest": "^29.0.0",
            "eslint": "^8.0.0",
            "prettier": "^2.8.0",
            "@types/jest": "^29.0.0",
            "@typescript-eslint/eslint-plugin": "^5.0.0",
            "@typescript-eslint/parser": "^5.0.0"
        }
        
        framework_deps = {
            "react": {
                "vite": "^4.3.0",
                "@vitejs/plugin-react": "^4.0.0",
                "@testing-library/react": "^13.0.0",
                "@testing-library/jest-dom": "^5.0.0",
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0"
            },
            "vue": {
                "@vue/cli-service": "^5.0.0",
                "@vue/test-utils": "^2.0.0",
                "@types/vue": "^3.0.0"
            },
            "angular": {
                "@angular/cli": "^16.0.0",
                "@angular/core": "^16.0.0",
                "karma": "^6.0.0",
                "protractor": "^7.0.0"
            },
            "next": {
                "@types/node": "^20.0.0",
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0"
            }
        }
        
        return {**base_deps, **framework_deps.get(framework, {})}
    
    def _get_python_requirements(self, framework: str) -> List[str]:
        """Get Python requirements for framework"""
        base_requirements = [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "ruff>=0.0.270",
            "mypy>=1.0.0"
        ]
        
        framework_requirements = {
            "fastapi": [
                "fastapi>=0.100.0",
                "uvicorn[standard]>=0.23.0",
                "pydantic>=2.0.0",
                "sqlalchemy>=2.0.0",
                "alembic>=1.11.0",
                "python-multipart>=0.0.6",
                "python-jose[cryptography]>=3.3.0",
                "passlib[bcrypt]>=1.7.4",
                "python-dotenv>=1.0.0"
            ],
            "flask": [
                "flask>=2.3.0",
                "flask-sqlalchemy>=3.0.0",
                "flask-migrate>=4.0.0",
                "flask-jwt-extended>=4.5.0",
                "flask-cors>=4.0.0",
                "gunicorn>=21.0.0"
            ],
            "django": [
                "django>=4.2.0",
                "djangorestframework>=3.14.0",
                "django-cors-headers>=4.0.0",
                "django-filter>=23.0.0",
                "celery>=5.3.0",
                "redis>=4.6.0"
            ]
        }
        
        return base_requirements + framework_requirements.get(framework, [])
    
    def _generate_cicd_config(self, project_dir: str, project_type: str, framework: str):
        """Generate CI/CD configuration"""
        
        # GitHub Actions workflow
        if framework in ["react", "vue", "angular", "next"]:
            workflow_content = self._get_node_workflow(framework)
        elif framework in ["fastapi", "flask", "django"]:
            workflow_content = self._get_python_workflow(framework)
        else:
            workflow_content = self._get_generic_workflow()
        
        workflow_dir = os.path.join(project_dir, ".github/workflows")
        os.makedirs(workflow_dir, exist_ok=True)
        
        workflow_path = os.path.join(workflow_dir, "ci.yml")
        with open(workflow_path, 'w') as f:
            f.write(workflow_content)
        
        # Docker configuration
        dockerfile_content = self._get_dockerfile_content(framework)
        dockerfile_path = os.path.join(project_dir, "Dockerfile")
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        # Docker compose for development
        docker_compose_content = self._get_docker_compose_content(framework)
        compose_path = os.path.join(project_dir, "docker-compose.yml")
        with open(compose_path, 'w') as f:
            f.write(docker_compose_content)
    
    def _get_node_workflow(self, framework: str) -> str:
        """Get Node.js GitHub Actions workflow"""
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
    - uses: actions/checkout@v3
    
    - name: Use Node.js ${{{{ matrix.node-version }}}}
      uses: actions/setup-node@v3
      with:
        node-version: ${{{{ matrix.node-version }}}}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint
    
    - name: Run type check
      run: npm run type-check
    
    - name: Run tests
      run: npm run test:coverage
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info
    
    - name: Build application
      run: npm run build
    
    - name: Run E2E tests
      run: npm run test:e2e
      if: matrix.node-version == 18

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security audit
      run: npm audit --audit-level moderate
    
    - name: Run Snyk security scan
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{{{ secrets.SNYK_TOKEN }}}}

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Add your deployment commands here
"""
    
    def _get_python_workflow(self, framework: str) -> str:
        """Get Python GitHub Actions workflow"""
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
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{{{ matrix.python-version }}}}
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
    
    - name: Run type check
      run: mypy src
    
    - name: Run tests
      run: pytest --cov=src --cov-report=xml
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
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
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Add your deployment commands here
"""
    
    def _get_generic_workflow(self) -> str:
        """Get generic GitHub Actions workflow"""
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
    - uses: actions/checkout@v3
    
    - name: Build and test
      run: |
        echo "Building and testing..."
        # Add your build and test commands here
    
    - name: Security scan
      run: |
        echo "Running security scan..."
        # Add your security scan commands here
    
    - name: Deploy
      if: github.ref == 'refs/heads/main'
      run: |
        echo "Deploying..."
        # Add your deployment commands here
"""
    
    def _get_dockerfile_content(self, framework: str) -> str:
        """Get Dockerfile content for framework"""
        if framework in ["react", "vue", "angular", "next"]:
            return """# Multi-stage build for Node.js application
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
RUN adduser -S nextjs -u 1001

# Change ownership
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:3000/health || exit 1

# Start application
CMD ["npm", "start"]
"""
        elif framework in ["fastapi", "flask", "django"]:
            return """# Python application Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

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
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        else:
            return """# Generic Dockerfile
FROM alpine:latest

WORKDIR /app

# Copy application
COPY . .

# Install dependencies and build
RUN echo "Add your build commands here"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD echo "Add your health check here"

# Start application
CMD ["echo", "Add your start command here"]
"""
    
    def _get_docker_compose_content(self, framework: str) -> str:
        """Get Docker Compose content for development"""
        if framework in ["fastapi", "flask", "django"]:
            return """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /app/__pycache__
    environment:
      - DEBUG=1
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=dbname
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
    
    def _generate_documentation(self, project_dir: str, name: str, project_type: str, framework: str):
        """Generate project documentation"""
        
        # README.md
        readme_content = f"""# {name}

A modern {project_type} application built with {framework} and AI-powered development tools.

## Features

- 🚀 Modern {framework} architecture
- 🧠 AI-powered development with Claude Code
- 🔍 Automated quality control with CEO Agent
- 🧪 Comprehensive testing suite
- 🔒 Security scanning and monitoring
- 📈 Performance optimization
- 🚢 CI/CD pipeline with GitHub Actions
- 📚 Automated documentation

## Quick Start

### Prerequisites

- Node.js 18+ (for web projects)
- Python 3.9+ (for Python projects)
- Git
- Claude Code CLI
- Docker (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd {name}
   ```

2. Install dependencies:
   ```bash
   npm install  # for Node.js projects
   pip install -r requirements.txt  # for Python projects
   ```

3. Start development server:
   ```bash
   npm run dev  # for Node.js projects
   python main.py  # for Python projects
   ```

## Development

This project uses AI-powered development with automatic quality control:

### AI Tools Integration

- **Sequential Thinking**: Strategic planning and problem-solving
- **Perplexity**: Real-time research and intelligence
- **Context7**: Documentation and best practices
- **Playwright**: Automated testing and UI interactions
- **GitHub**: Repository management and CI/CD

### Quality Control

The CEO Quality Control Agent automatically:
- Reviews all code changes
- Enforces quality standards
- Provides improvement suggestions
- Ensures security best practices
- Monitors performance metrics

### Development Workflow

1. Make changes to your code
2. The CEO Agent automatically reviews your work
3. Address any quality issues highlighted
4. Commit when standards are met
5. CI/CD pipeline handles deployment

## Architecture

```
{name}/
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── scripts/                # Build and deployment scripts
├── .github/workflows/      # CI/CD pipelines
├── CLAUDE.md              # AI configuration
├── package.json           # Dependencies (Node.js)
├── requirements.txt       # Dependencies (Python)
├── Dockerfile            # Container configuration
└── docker-compose.yml    # Development environment
```

## Testing

Run the test suite:
```bash
npm test                   # Node.js projects
pytest                     # Python projects
```

Run with coverage:
```bash
npm run test:coverage      # Node.js projects
pytest --cov=src          # Python projects
```

## Deployment

### Local Development
```bash
docker-compose up
```

### Production
```bash
docker build -t {name} .
docker run -p 8000:8000 {name}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass
5. Submit a pull request

The CEO Quality Control Agent will automatically review your contributions.

## License

MIT License - see LICENSE file for details.
"""
        
        readme_path = os.path.join(project_dir, "README.md")
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        # API Documentation (for API projects)
        if project_type == "api":
            api_doc_content = f"""# API Documentation

## Overview

{name} provides a RESTful API built with {framework}.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API requests require authentication using JWT tokens.

### Get Token

```bash
POST /auth/login
Content-Type: application/json

{{
  "username": "user@example.com",
  "password": "password"
}}
```

### Use Token

```bash
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Health Check

```bash
GET /health
```

Returns the API health status.

### Users

#### Get All Users

```bash
GET /users
```

#### Get User by ID

```bash
GET /users/{{id}}
```

#### Create User

```bash
POST /users
Content-Type: application/json

{{
  "name": "John Doe",
  "email": "john@example.com"
}}
```

#### Update User

```bash
PUT /users/{{id}}
Content-Type: application/json

{{
  "name": "John Updated",
  "email": "john.updated@example.com"
}}
```

#### Delete User

```bash
DELETE /users/{{id}}
```

## Error Handling

The API returns standard HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error responses include a detailed message:

```json
{{
  "error": "User not found",
  "code": "USER_NOT_FOUND",
  "details": "No user found with ID: 123"
}}
```

## Rate Limiting

API requests are limited to 100 requests per minute per IP address.

## Examples

### Python

```python
import requests

# Get token
response = requests.post('http://localhost:8000/auth/login', json={{
    'username': 'user@example.com',
    'password': 'password'
}})
token = response.json()['token']

# Make authenticated request
headers = {{'Authorization': f'Bearer {{token}}'}}
response = requests.get('http://localhost:8000/users', headers=headers)
users = response.json()
```

### JavaScript

```javascript
// Get token
const loginResponse = await fetch('http://localhost:8000/auth/login', {{
  method: 'POST',
  headers: {{'Content-Type': 'application/json'}},
  body: JSON.stringify({{
    username: 'user@example.com',
    password: 'password'
  }})
}});
const {{ token }} = await loginResponse.json();

// Make authenticated request
const response = await fetch('http://localhost:8000/users', {{
  headers: {{'Authorization': `Bearer ${{token}}`}}
}});
const users = await response.json();
```

## Testing

Test the API endpoints using the provided test suite:

```bash
pytest tests/test_api.py
```

Or manually with curl:

```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{{"username": "user@example.com", "password": "password"}}'

# Get users (with token)
curl -H "Authorization: Bearer <token>" http://localhost:8000/users
```
"""
            
            api_doc_path = os.path.join(project_dir, "docs", "api.md")
            with open(api_doc_path, 'w') as f:
                f.write(api_doc_content)
    
    def _generate_tests(self, project_dir: str, project_type: str, framework: str):
        """Generate test files"""
        
        if framework in ["react", "vue", "angular", "next"]:
            # Jest configuration
            jest_config = {
                "testEnvironment": "jsdom",
                "setupFilesAfterEnv": ["<rootDir>/src/setupTests.ts"],
                "testMatch": [
                    "**/__tests__/**/*.(js|jsx|ts|tsx)",
                    "**/*.(test|spec).(js|jsx|ts|tsx)"
                ],
                "transform": {
                    "^.+\\.(js|jsx|ts|tsx)$": "babel-jest"
                },
                "moduleNameMapping": {
                    "^@/(.*)$": "<rootDir>/src/$1"
                },
                "collectCoverageFrom": [
                    "src/**/*.{js,jsx,ts,tsx}",
                    "!src/**/*.d.ts"
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
            
            jest_config_path = os.path.join(project_dir, "jest.config.js")
            with open(jest_config_path, 'w') as f:
                f.write(f"module.exports = {json.dumps(jest_config, indent=2)}")
            
            # Setup tests file
            setup_tests_content = """import '@testing-library/jest-dom';

// Mock matchMedia
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

// Mock IntersectionObserver
global.IntersectionObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));
"""
            
            setup_tests_path = os.path.join(project_dir, "src", "setupTests.ts")
            with open(setup_tests_path, 'w') as f:
                f.write(setup_tests_content)
            
            # Sample component test
            if framework == "react":
                test_content = """import React from 'react';
import { render, screen } from '@testing-library/react';
import { App } from './App';

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText('Hello World')).toBeInTheDocument();
  });
  
  it('has correct title', () => {
    render(<App />);
    expect(document.title).toBe('My App');
  });
});
"""
                
                test_path = os.path.join(project_dir, "src", "App.test.tsx")
                with open(test_path, 'w') as f:
                    f.write(test_content)
        
        elif framework in ["fastapi", "flask", "django"]:
            # Pytest configuration
            pytest_config = """[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --cov=src --cov-report=html --cov-report=term-missing"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
"""
            
            pytest_config_path = os.path.join(project_dir, "pyproject.toml")
            # Append to existing pyproject.toml or create new
            with open(pytest_config_path, 'a') as f:
                f.write(f"\n{pytest_config}")
            
            # Sample API test
            if framework == "fastapi":
                test_content = """import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_user():
    response = client.post(
        "/users",
        json={"name": "John Doe", "email": "john@example.com"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

class TestUserAPI:
    def test_user_creation_validation(self):
        # Test invalid email
        response = client.post(
            "/users",
            json={"name": "John Doe", "email": "invalid-email"}
        )
        assert response.status_code == 422
    
    def test_user_update(self):
        # Create user first
        create_response = client.post(
            "/users",
            json={"name": "John Doe", "email": "john@example.com"}
        )
        user_id = create_response.json()["id"]
        
        # Update user
        update_response = client.put(
            f"/users/{user_id}",
            json={"name": "John Updated", "email": "john.updated@example.com"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "John Updated"
    
    def test_user_deletion(self):
        # Create user first
        create_response = client.post(
            "/users",
            json={"name": "John Doe", "email": "john@example.com"}
        )
        user_id = create_response.json()["id"]
        
        # Delete user
        delete_response = client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 204
        
        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
"""
                
                test_path = os.path.join(project_dir, "tests", "test_api.py")
                with open(test_path, 'w') as f:
                    f.write(test_content)
            
            # Conftest.py for shared fixtures
            conftest_content = """import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
"""
            
            conftest_path = os.path.join(project_dir, "tests", "conftest.py")
            with open(conftest_path, 'w') as f:
                f.write(conftest_content)
    
    def _generate_security_config(self, project_dir: str, project_type: str, framework: str):
        """Generate security configuration"""
        
        # Security policy
        security_policy = """# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability, please report it to:
- Email: security@example.com
- Create a private GitHub issue

## Security Measures

This project implements the following security measures:

### Authentication & Authorization
- JWT tokens for API authentication
- Role-based access control
- Session management
- Password hashing with bcrypt

### Input Validation
- Request validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection

### Infrastructure Security
- HTTPS enforcement
- Security headers
- Rate limiting
- Input size limits

### Dependencies
- Regular security updates
- Automated vulnerability scanning
- Dependency pinning

## Security Checklist

- [ ] All inputs are validated and sanitized
- [ ] Authentication is properly implemented
- [ ] Authorization checks are in place
- [ ] Sensitive data is encrypted
- [ ] Security headers are configured
- [ ] Rate limiting is implemented
- [ ] Dependencies are up to date
- [ ] Security tests are included

## Compliance

This project follows:
- OWASP Top 10 guidelines
- Security best practices
- Industry standards
"""
        
        security_policy_path = os.path.join(project_dir, "SECURITY.md")
        with open(security_policy_path, 'w') as f:
            f.write(security_policy)
        
        # GitHub security workflow
        security_workflow = """name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run CodeQL Analysis
      uses: github/codeql-action/analyze@v2
      with:
        languages: javascript, python
"""
        
        security_workflow_path = os.path.join(project_dir, ".github", "workflows", "security.yml")
        with open(security_workflow_path, 'w') as f:
            f.write(security_workflow)
    
    def _generate_dev_scripts(self, project_dir: str, project_type: str, framework: str):
        """Generate development scripts"""
        
        # Development setup script
        if framework in ["react", "vue", "angular", "next"]:
            setup_script = """#!/bin/bash
set -e

echo "🚀 Setting up development environment..."

# Check Node.js version
node_version=$(node --version | cut -d'v' -f2)
required_version="18.0.0"

if [ "$(printf '%s\\n' "$required_version" "$node_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Node.js version $node_version is too old. Required: $required_version+"
    exit 1
fi

echo "✅ Node.js version: $node_version"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Setup environment
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please update .env with your configuration"
fi

# Run initial build
echo "🔨 Running initial build..."
npm run build

# Run tests
echo "🧪 Running tests..."
npm test

echo "✅ Development environment setup complete!"
echo "🎯 Run 'npm run dev' to start development server"
"""
        elif framework in ["fastapi", "flask", "django"]:
            setup_script = """#!/bin/bash
set -e

echo "🚀 Setting up development environment..."

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2)
required_version="3.9.0"

if [ "$(printf '%s\\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old. Required: $required_version+"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please update .env with your configuration"
fi

# Run database migrations
echo "🗄️ Running database migrations..."
alembic upgrade head

# Run tests
echo "🧪 Running tests..."
pytest

echo "✅ Development environment setup complete!"
echo "🎯 Run 'source venv/bin/activate && python main.py' to start development server"
"""
        else:
            setup_script = """#!/bin/bash
set -e

echo "🚀 Setting up development environment..."

# Add your setup commands here
echo "⚙️ Setting up project..."

# Setup environment
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please update .env with your configuration"
fi

echo "✅ Development environment setup complete!"
"""
        
        setup_script_path = os.path.join(project_dir, "scripts", "setup.sh")
        with open(setup_script_path, 'w') as f:
            f.write(setup_script)
        
        os.chmod(setup_script_path, 0o755)
        
        # Environment example
        env_example = """# Environment Configuration

# Application
APP_NAME=my-app
APP_ENV=development
APP_DEBUG=true
APP_PORT=3000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
DATABASE_POOL_SIZE=10

# Redis
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=your-secret-key-here
JWT_EXPIRATION=24h

# External APIs
API_KEY=your-api-key-here

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=info

# Security
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000
"""
        
        env_example_path = os.path.join(project_dir, ".env.example")
        with open(env_example_path, 'w') as f:
            f.write(env_example)
        
        # Gitignore
        gitignore_content = """.env
.env.local
.env.production
.env.staging

# Dependencies
node_modules/
venv/
__pycache__/
*.pyc
*.pyo
*.pyd

# Build outputs
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Testing
coverage/
.coverage
.pytest_cache/

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
"""
        
        gitignore_path = os.path.join(project_dir, ".gitignore")
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
    
    def _initialize_git(self, project_dir: str):
        """Initialize git repository"""
        try:
            os.chdir(project_dir)
            
            # Initialize git
            subprocess.run(["git", "init"], check=True)
            
            # Add all files
            subprocess.run(["git", "add", "."], check=True)
            
            # Initial commit
            subprocess.run([
                "git", "commit", "-m", "🎉 Initial commit: Project generated with AI development tools"
            ], check=True)
            
            logger.info("✅ Git repository initialized")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize git: {e}")
        except Exception as e:
            logger.error(f"Error initializing git: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate new application project')
    parser.add_argument('--name', required=True, help='Project name')
    parser.add_argument('--type', required=True, choices=['web', 'mobile', 'api', 'desktop', 'cli', 'saas', 'ai'], 
                       help='Project type')
    parser.add_argument('--framework', required=True, help='Framework to use')
    parser.add_argument('--backend', help='Backend framework (for web projects)')
    parser.add_argument('--database', help='Database to use (for API projects)')
    parser.add_argument('--features', nargs='+', help='Additional features to include')
    parser.add_argument('--output', help='Output directory')
    
    args = parser.parse_args()
    
    # Validate framework for project type
    generator = NewAppTemplateGenerator()
    
    if args.type not in generator.project_types:
        logger.error(f"Invalid project type: {args.type}")
        sys.exit(1)
    
    if args.framework not in generator.project_types[args.type]["frameworks"]:
        logger.error(f"Invalid framework '{args.framework}' for project type '{args.type}'")
        logger.info(f"Available frameworks: {generator.project_types[args.type]['frameworks']}")
        sys.exit(1)
    
    # Generate project
    options = {
        'backend': args.backend,
        'database': args.database,
        'features': args.features or [],
        'output': args.output
    }
    
    try:
        project_dir = generator.generate_project(args.name, args.type, args.framework, options)
        
        logger.info(f"""
🎉 Project '{args.name}' generated successfully!

📁 Location: {project_dir}
🔧 Type: {args.type}
🚀 Framework: {args.framework}

🎯 Next steps:
1. cd {project_dir}
2. ./scripts/setup.sh
3. Open in your IDE
4. Start developing with AI assistance!

🧠 AI Features:
- CEO Quality Control Agent monitors your code
- Sequential thinking for complex problems
- Real-time research with Perplexity
- Automated testing with Playwright
- Continuous improvement with memory

🚀 Start development:
- npm run dev (Node.js projects)
- python main.py (Python projects)

📚 Documentation:
- README.md - Project overview
- docs/ - Detailed documentation
- CLAUDE.md - AI configuration
""")
        
    except Exception as e:
        logger.error(f"Failed to generate project: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()