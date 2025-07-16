#!/usr/bin/env python3
"""
CLAUDE.md Auto-Deployment System

This system automatically detects when Claude Code enters a directory and deploys
the appropriate CLAUDE.md file based on project type detection.

Author: Autonomous AI Development System
Version: 1.0.0
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/claude-md-auto-deploy.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ProjectDetector:
    """Intelligent project type detection system."""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.files = self._scan_files()
        
    def _scan_files(self) -> List[str]:
        """Scan directory for files and return list of filenames."""
        try:
            files = []
            for root, dirs, file_list in os.walk(self.project_path):
                # Skip hidden directories and common build/cache directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {
                    'node_modules', '__pycache__', 'build', 'dist', 'target', 'venv', '.git'
                }]
                for file in file_list:
                    if not file.startswith('.'):
                        rel_path = os.path.relpath(os.path.join(root, file), self.project_path)
                        files.append(rel_path)
            return files
        except Exception as e:
            logger.error(f"Error scanning files: {e}")
            return []
    
    def detect_project_type(self) -> Tuple[str, Dict]:
        """
        Detect project type and return type with confidence scores.
        
        Returns:
            Tuple[str, Dict]: (project_type, metadata)
        """
        metadata = {
            'files_count': len(self.files),
            'technology_stack': self._detect_technology_stack(),
            'complexity': self._assess_complexity(),
            'has_existing_code': self._has_existing_code(),
            'saas_indicators': self._detect_saas_indicators(),
            'confidence_scores': {}
        }
        
        # Calculate confidence scores for each project type
        new_app_score = self._calculate_new_app_score()
        existing_app_score = self._calculate_existing_app_score()
        saas_app_score = self._calculate_saas_app_score()
        
        metadata['confidence_scores'] = {
            'new_app': new_app_score,
            'existing_app': existing_app_score,
            'saas_app': saas_app_score
        }
        
        # Determine project type based on highest confidence score
        if saas_app_score > 0.7:
            return 'saas-app', metadata
        elif existing_app_score > 0.6:
            return 'existing-app', metadata
        elif new_app_score > 0.5:
            return 'new-app', metadata
        else:
            # Default to new-app for empty or minimal directories
            return 'new-app', metadata
    
    def _detect_technology_stack(self) -> List[str]:
        """Detect technology stack from files."""
        stack = []
        
        # Frontend frameworks
        if any('package.json' in f for f in self.files):
            stack.append('node.js')
        if any('react' in f.lower() for f in self.files):
            stack.append('react')
        if any('vue' in f.lower() for f in self.files):
            stack.append('vue')
        if any('angular' in f.lower() for f in self.files):
            stack.append('angular')
        if any('next' in f.lower() for f in self.files):
            stack.append('next.js')
        
        # Backend frameworks
        if any('requirements.txt' in f or 'setup.py' in f for f in self.files):
            stack.append('python')
        if any('Gemfile' in f for f in self.files):
            stack.append('ruby')
        if any('pom.xml' in f or 'build.gradle' in f for f in self.files):
            stack.append('java')
        if any('go.mod' in f for f in self.files):
            stack.append('go')
        if any('.php' in f for f in self.files):
            stack.append('php')
        
        # Databases
        if any('docker-compose' in f for f in self.files):
            stack.append('docker')
        if any('postgres' in f.lower() or 'psql' in f.lower() for f in self.files):
            stack.append('postgresql')
        if any('mongo' in f.lower() for f in self.files):
            stack.append('mongodb')
        if any('redis' in f.lower() for f in self.files):
            stack.append('redis')
        
        return stack
    
    def _assess_complexity(self) -> str:
        """Assess project complexity based on file count and structure."""
        file_count = len(self.files)
        has_multiple_services = self._has_multiple_services()
        has_database = self._has_database_config()
        has_tests = self._has_tests()
        
        complexity_score = 0
        if file_count > 100:
            complexity_score += 2
        elif file_count > 50:
            complexity_score += 1
        
        if has_multiple_services:
            complexity_score += 2
        if has_database:
            complexity_score += 1
        if has_tests:
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'complex'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'simple'
    
    def _has_existing_code(self) -> bool:
        """Check if directory has existing code files."""
        code_extensions = {'.js', '.ts', '.py', '.java', '.go', '.rb', '.php', '.cpp', '.c', '.cs'}
        return any(
            any(f.endswith(ext) for ext in code_extensions)
            for f in self.files
        )
    
    def _detect_saas_indicators(self) -> List[str]:
        """Detect SaaS-specific indicators."""
        indicators = []
        
        # SaaS-specific files and patterns
        saas_patterns = [
            'subscription', 'billing', 'payment', 'tenant', 'multi-tenant',
            'stripe', 'paddle', 'auth', 'oauth', 'jwt', 'admin', 'dashboard',
            'analytics', 'metrics', 'plans', 'pricing', 'api', 'webhook'
        ]
        
        for pattern in saas_patterns:
            if any(pattern in f.lower() for f in self.files):
                indicators.append(pattern)
        
        # Check for SaaS frameworks
        if any('saas' in f.lower() for f in self.files):
            indicators.append('saas_framework')
        
        return indicators
    
    def _calculate_new_app_score(self) -> float:
        """Calculate confidence score for new app project type."""
        score = 0.0
        
        # Empty or minimal directory
        if len(self.files) == 0:
            score += 0.8
        elif len(self.files) < 5:
            score += 0.6
        
        # No existing code
        if not self._has_existing_code():
            score += 0.4
        
        # Has basic config files only
        config_files = {'package.json', 'requirements.txt', 'README.md', '.gitignore'}
        if any(f in config_files for f in self.files):
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_existing_app_score(self) -> float:
        """Calculate confidence score for existing app project type."""
        score = 0.0
        
        # Has existing code
        if self._has_existing_code():
            score += 0.5
        
        # Substantial file count
        if len(self.files) > 10:
            score += 0.3
        
        # Has project structure
        if self._has_project_structure():
            score += 0.2
        
        # Has version control
        if any('.git' in f for f in self.files):
            score += 0.1
        
        # But not too many SaaS indicators
        if len(self._detect_saas_indicators()) < 3:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_saas_app_score(self) -> float:
        """Calculate confidence score for SaaS app project type."""
        score = 0.0
        
        # SaaS indicators
        saas_indicators = self._detect_saas_indicators()
        score += min(len(saas_indicators) * 0.15, 0.6)
        
        # Has authentication
        if any('auth' in f.lower() for f in self.files):
            score += 0.2
        
        # Has API structure
        if any('api' in f.lower() for f in self.files):
            score += 0.1
        
        # Has database
        if self._has_database_config():
            score += 0.1
        
        # Has admin/dashboard
        if any(term in ' '.join(self.files).lower() for term in ['admin', 'dashboard']):
            score += 0.1
        
        return min(score, 1.0)
    
    def _has_multiple_services(self) -> bool:
        """Check if project has multiple services/microservices."""
        service_indicators = ['docker-compose', 'kubernetes', 'k8s', 'microservice']
        return any(indicator in ' '.join(self.files).lower() for indicator in service_indicators)
    
    def _has_database_config(self) -> bool:
        """Check if project has database configuration."""
        db_indicators = ['database', 'db', 'sql', 'mongo', 'redis', 'postgres', 'mysql']
        return any(indicator in ' '.join(self.files).lower() for indicator in db_indicators)
    
    def _has_tests(self) -> bool:
        """Check if project has test files."""
        return any('test' in f.lower() or 'spec' in f.lower() for f in self.files)
    
    def _has_project_structure(self) -> bool:
        """Check if project has organized structure."""
        structure_indicators = ['src', 'lib', 'app', 'components', 'services', 'models']
        return any(indicator in ' '.join(self.files).lower() for indicator in structure_indicators)


class ClaudeMDDeployer:
    """CLAUDE.md file deployment system."""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.templates_path = self.base_path.parent / 'templates' / 'claude-md-templates'
        self.ensure_templates_exist()
    
    def ensure_templates_exist(self):
        """Ensure template directory and files exist."""
        if not self.templates_path.exists():
            logger.error(f"Templates directory not found: {self.templates_path}")
            raise FileNotFoundError(f"Templates directory not found: {self.templates_path}")
    
    def deploy_claude_md(self, project_path: str, project_type: str, metadata: Dict) -> bool:
        """
        Deploy appropriate CLAUDE.md file to project directory.
        
        Args:
            project_path: Path to project directory
            project_type: Detected project type
            metadata: Project metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            target_path = Path(project_path) / 'CLAUDE.md'
            
            # Skip if CLAUDE.md already exists and is recent
            if target_path.exists():
                mod_time = datetime.fromtimestamp(target_path.stat().st_mtime)
                age_hours = (datetime.now() - mod_time).total_seconds() / 3600
                if age_hours < 24:  # Don't override recent files
                    logger.info(f"CLAUDE.md already exists and is recent: {target_path}")
                    return True
            
            # Select appropriate template
            template_mapping = {
                'new-app': 'CLAUDE-NEW-APP.md',
                'existing-app': 'CLAUDE-EXISTING-APP.md',
                'saas-app': 'CLAUDE-SAAS-APP.md'
            }
            
            template_file = template_mapping.get(project_type, 'CLAUDE-NEW-APP.md')
            template_path = self.templates_path / template_file
            
            if not template_path.exists():
                logger.error(f"Template not found: {template_path}")
                return False
            
            # Copy template to project directory
            shutil.copy2(template_path, target_path)
            
            # Add project-specific metadata
            self._add_project_metadata(target_path, metadata)
            
            logger.info(f"Successfully deployed {template_file} to {target_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error deploying CLAUDE.md: {e}")
            return False
    
    def _add_project_metadata(self, claude_md_path: Path, metadata: Dict):
        """Add project-specific metadata to CLAUDE.md file."""
        try:
            # Read existing content
            with open(claude_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add metadata section
            metadata_section = f"""
<!-- AUTO-GENERATED PROJECT METADATA -->
<!-- Detection Time: {datetime.now().isoformat()} -->
<!-- Technology Stack: {', '.join(metadata.get('technology_stack', []))} -->
<!-- Complexity: {metadata.get('complexity', 'unknown')} -->
<!-- Files Count: {metadata.get('files_count', 0)} -->
<!-- SaaS Indicators: {', '.join(metadata.get('saas_indicators', []))} -->

"""
            
            # Insert metadata after the first line
            lines = content.split('\n')
            lines.insert(1, metadata_section)
            
            # Write back to file
            with open(claude_md_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
                
        except Exception as e:
            logger.error(f"Error adding metadata: {e}")


class AutoDeploymentSystem:
    """Main auto-deployment system."""
    
    def __init__(self):
        self.detector = None
        self.deployer = ClaudeMDDeployer()
    
    def auto_deploy(self, project_path: str = None) -> Dict:
        """
        Auto-deploy CLAUDE.md based on project detection.
        
        Args:
            project_path: Path to project directory (defaults to current directory)
            
        Returns:
            Dict: Deployment results and metadata
        """
        if project_path is None:
            project_path = os.getcwd()
        
        try:
            logger.info(f"Starting auto-deployment for: {project_path}")
            
            # Detect project type
            self.detector = ProjectDetector(project_path)
            project_type, metadata = self.detector.detect_project_type()
            
            logger.info(f"Detected project type: {project_type}")
            logger.info(f"Confidence scores: {metadata['confidence_scores']}")
            
            # Deploy appropriate CLAUDE.md
            success = self.deployer.deploy_claude_md(project_path, project_type, metadata)
            
            result = {
                'success': success,
                'project_type': project_type,
                'metadata': metadata,
                'deployment_time': datetime.now().isoformat(),
                'claude_md_path': str(Path(project_path) / 'CLAUDE.md')
            }
            
            if success:
                logger.info("Auto-deployment completed successfully")
                self._log_deployment_summary(result)
            else:
                logger.error("Auto-deployment failed")
            
            return result
            
        except Exception as e:
            logger.error(f"Auto-deployment error: {e}")
            return {
                'success': False,
                'error': str(e),
                'deployment_time': datetime.now().isoformat()
            }
    
    def _log_deployment_summary(self, result: Dict):
        """Log deployment summary."""
        print("\n" + "="*60)
        print("🤖 CLAUDE.MD AUTO-DEPLOYMENT COMPLETE")
        print("="*60)
        print(f"📁 Project Path: {os.path.dirname(result['claude_md_path'])}")
        print(f"🎯 Project Type: {result['project_type']}")
        print(f"📊 Complexity: {result['metadata']['complexity']}")
        print(f"🛠️  Technology Stack: {', '.join(result['metadata']['technology_stack'])}")
        print(f"📝 CLAUDE.md: {result['claude_md_path']}")
        print(f"⚡ Confidence Scores:")
        for ptype, score in result['metadata']['confidence_scores'].items():
            print(f"   {ptype}: {score:.2f}")
        print("\n✅ The autonomous development system is now active!")
        print("💡 Provide your initial prompt to start development automation.")
        print("="*60)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="CLAUDE.md Auto-Deployment System")
    parser.add_argument('--project', type=str, help='Project directory path')
    parser.add_argument('--auto-detect', action='store_true', help='Auto-detect and deploy')
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize auto-deployment system
    system = AutoDeploymentSystem()
    
    # Auto-deploy
    result = system.auto_deploy(args.project)
    
    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()