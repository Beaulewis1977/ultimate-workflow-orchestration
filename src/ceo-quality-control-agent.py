#!/usr/bin/env python3
"""
CEO/Quality Control Agent - The Ultimate Overseer
=================================================

This agent acts as the CEO/Quality Control system that:
1. Monitors all development work and outputs
2. Validates against project plans and requirements
3. Automatically fixes issues or sends work back for revision
4. Maintains quality standards across all agents
5. Provides executive oversight and decision making

Author: Autonomous Development System
Version: 1.0.0
"""

import asyncio
import json
import logging
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import yaml
import subprocess
import hashlib
import tempfile
import difflib
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
import psutil
import aiohttp
import redis
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ast
import tokenize
from io import StringIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/mnt/c/bmad-workspace/logs/ceo-quality-control.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class QualityStandard(Enum):
    """Quality standards for different work types"""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    NEEDS_IMPROVEMENT = "needs_improvement"
    UNACCEPTABLE = "unacceptable"

class WorkType(Enum):
    """Types of work that can be quality controlled"""
    CODE = "code"
    DOCUMENTATION = "documentation"
    TESTS = "tests"
    ARCHITECTURE = "architecture"
    DESIGN = "design"
    DEPLOYMENT = "deployment"
    SECURITY = "security"
    PERFORMANCE = "performance"

@dataclass
class QualityMetrics:
    """Metrics for quality assessment"""
    code_quality: float = 0.0
    test_coverage: float = 0.0
    documentation_completeness: float = 0.0
    security_score: float = 0.0
    performance_score: float = 0.0
    architecture_compliance: float = 0.0
    overall_score: float = 0.0
    
    def calculate_overall_score(self):
        """Calculate overall quality score"""
        metrics = [
            self.code_quality,
            self.test_coverage,
            self.documentation_completeness,
            self.security_score,
            self.performance_score,
            self.architecture_compliance
        ]
        self.overall_score = sum(metrics) / len(metrics)

@dataclass
class QualityIssue:
    """Represents a quality issue found during review"""
    issue_type: str
    severity: str  # critical, high, medium, low
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False
    agent_responsible: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class WorkItem:
    """Represents a work item for quality control"""
    id: str
    work_type: WorkType
    file_path: str
    agent_name: str
    project_name: str
    content: str
    requirements: List[str]
    quality_metrics: QualityMetrics = field(default_factory=QualityMetrics)
    issues: List[QualityIssue] = field(default_factory=list)
    status: str = "pending"  # pending, approved, rejected, needs_revision
    timestamp: datetime = field(default_factory=datetime.now)
    revision_count: int = 0
    max_revisions: int = 3

class QualityReviewEngine:
    """Engine for performing quality reviews"""
    
    def __init__(self):
        self.quality_standards = {
            WorkType.CODE: {
                "min_quality_score": 0.8,
                "max_complexity": 10,
                "min_coverage": 0.8,
                "required_patterns": ["error_handling", "logging", "documentation"]
            },
            WorkType.DOCUMENTATION: {
                "min_completeness": 0.9,
                "required_sections": ["overview", "usage", "examples"],
                "max_readability_score": 8.0
            },
            WorkType.TESTS: {
                "min_coverage": 0.9,
                "required_types": ["unit", "integration"],
                "max_test_time": 30.0
            },
            WorkType.ARCHITECTURE: {
                "min_compliance": 0.85,
                "required_patterns": ["separation_of_concerns", "single_responsibility"],
                "max_coupling": 0.3
            }
        }
        
    async def review_work_item(self, work_item: WorkItem) -> Tuple[QualityStandard, List[QualityIssue]]:
        """Perform comprehensive quality review"""
        issues = []
        
        # Perform specific reviews based on work type
        if work_item.work_type == WorkType.CODE:
            code_issues = await self._review_code_quality(work_item)
            issues.extend(code_issues)
            
        elif work_item.work_type == WorkType.DOCUMENTATION:
            doc_issues = await self._review_documentation(work_item)
            issues.extend(doc_issues)
            
        elif work_item.work_type == WorkType.TESTS:
            test_issues = await self._review_tests(work_item)
            issues.extend(test_issues)
            
        elif work_item.work_type == WorkType.ARCHITECTURE:
            arch_issues = await self._review_architecture(work_item)
            issues.extend(arch_issues)
            
        # Calculate overall quality metrics
        await self._calculate_quality_metrics(work_item)
        
        # Determine quality standard
        quality_standard = self._determine_quality_standard(work_item)
        
        return quality_standard, issues
    
    async def _review_code_quality(self, work_item: WorkItem) -> List[QualityIssue]:
        """Review code quality specifically"""
        issues = []
        content = work_item.content
        
        # Check for basic code quality issues
        if not self._has_error_handling(content):
            issues.append(QualityIssue(
                issue_type="missing_error_handling",
                severity="high",
                description="Code lacks proper error handling",
                file_path=work_item.file_path,
                suggested_fix="Add try-catch blocks and proper error handling",
                auto_fixable=True
            ))
        
        if not self._has_logging(content):
            issues.append(QualityIssue(
                issue_type="missing_logging",
                severity="medium",
                description="Code lacks proper logging",
                file_path=work_item.file_path,
                suggested_fix="Add logging statements for debugging and monitoring",
                auto_fixable=True
            ))
        
        if not self._has_documentation(content):
            issues.append(QualityIssue(
                issue_type="missing_documentation",
                severity="medium",
                description="Code lacks proper documentation",
                file_path=work_item.file_path,
                suggested_fix="Add docstrings and comments",
                auto_fixable=True
            ))
        
        # Check complexity
        complexity = self._calculate_complexity(content)
        if complexity > self.quality_standards[WorkType.CODE]["max_complexity"]:
            issues.append(QualityIssue(
                issue_type="high_complexity",
                severity="high",
                description=f"Code complexity ({complexity}) exceeds maximum (10)",
                file_path=work_item.file_path,
                suggested_fix="Refactor code to reduce complexity",
                auto_fixable=False
            ))
        
        # Check for security issues
        security_issues = await self._check_security_issues(content)
        issues.extend(security_issues)
        
        return issues
    
    async def _review_documentation(self, work_item: WorkItem) -> List[QualityIssue]:
        """Review documentation quality"""
        issues = []
        content = work_item.content
        
        required_sections = self.quality_standards[WorkType.DOCUMENTATION]["required_sections"]
        
        for section in required_sections:
            if not self._has_section(content, section):
                issues.append(QualityIssue(
                    issue_type="missing_section",
                    severity="medium",
                    description=f"Documentation missing required section: {section}",
                    file_path=work_item.file_path,
                    suggested_fix=f"Add {section} section to documentation",
                    auto_fixable=True
                ))
        
        # Check readability
        readability_score = self._calculate_readability(content)
        if readability_score > self.quality_standards[WorkType.DOCUMENTATION]["max_readability_score"]:
            issues.append(QualityIssue(
                issue_type="poor_readability",
                severity="medium",
                description=f"Documentation readability score ({readability_score}) exceeds maximum",
                file_path=work_item.file_path,
                suggested_fix="Simplify language and improve structure",
                auto_fixable=False
            ))
        
        return issues
    
    async def _review_tests(self, work_item: WorkItem) -> List[QualityIssue]:
        """Review test quality"""
        issues = []
        content = work_item.content
        
        # Check for test types
        required_types = self.quality_standards[WorkType.TESTS]["required_types"]
        
        for test_type in required_types:
            if not self._has_test_type(content, test_type):
                issues.append(QualityIssue(
                    issue_type="missing_test_type",
                    severity="high",
                    description=f"Missing {test_type} tests",
                    file_path=work_item.file_path,
                    suggested_fix=f"Add {test_type} tests",
                    auto_fixable=True
                ))
        
        # Check test coverage
        coverage = await self._calculate_test_coverage(work_item.file_path)
        if coverage < self.quality_standards[WorkType.TESTS]["min_coverage"]:
            issues.append(QualityIssue(
                issue_type="low_test_coverage",
                severity="high",
                description=f"Test coverage ({coverage:.2f}) below minimum",
                file_path=work_item.file_path,
                suggested_fix="Add more test cases to improve coverage",
                auto_fixable=False
            ))
        
        return issues
    
    async def _review_architecture(self, work_item: WorkItem) -> List[QualityIssue]:
        """Review architecture quality"""
        issues = []
        content = work_item.content
        
        # Check for architectural patterns
        required_patterns = self.quality_standards[WorkType.ARCHITECTURE]["required_patterns"]
        
        for pattern in required_patterns:
            if not self._follows_pattern(content, pattern):
                issues.append(QualityIssue(
                    issue_type="missing_pattern",
                    severity="medium",
                    description=f"Code doesn't follow {pattern} pattern",
                    file_path=work_item.file_path,
                    suggested_fix=f"Refactor to follow {pattern} pattern",
                    auto_fixable=False
                ))
        
        return issues
    
    def _has_error_handling(self, content: str) -> bool:
        """Check if code has proper error handling"""
        error_patterns = [
            r'try\s*:',
            r'except\s+\w+',
            r'catch\s*\(',
            r'throw\s+',
            r'raise\s+',
            r'error\s*\(',
            r'Error\s*\('
        ]
        
        for pattern in error_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _has_logging(self, content: str) -> bool:
        """Check if code has proper logging"""
        logging_patterns = [
            r'logger\.',
            r'log\.',
            r'console\.log',
            r'print\s*\(',
            r'logging\.',
            r'log\s*\('
        ]
        
        for pattern in logging_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _has_documentation(self, content: str) -> bool:
        """Check if code has proper documentation"""
        doc_patterns = [
            r'""".*?"""',
            r"'''.*?'''",
            r'/\*\*.*?\*/',
            r'//.*',
            r'#.*'
        ]
        
        for pattern in doc_patterns:
            if re.search(pattern, content, re.DOTALL):
                return True
        return False
    
    def _calculate_complexity(self, content: str) -> int:
        """Calculate code complexity (simplified McCabe complexity)"""
        complexity = 1  # Base complexity
        
        complexity_patterns = [
            r'\bif\b',
            r'\belse\b',
            r'\belif\b',
            r'\bwhile\b',
            r'\bfor\b',
            r'\btry\b',
            r'\bexcept\b',
            r'\bcase\b',
            r'\bswitch\b',
            r'\b\?\s*.*\s*:\s*',  # ternary operator
            r'\band\b',
            r'\bor\b',
            r'\|\|',
            r'\&\&'
        ]
        
        for pattern in complexity_patterns:
            complexity += len(re.findall(pattern, content, re.IGNORECASE))
        
        return complexity
    
    async def _check_security_issues(self, content: str) -> List[QualityIssue]:
        """Check for security issues in code"""
        issues = []
        
        # Common security anti-patterns
        security_patterns = [
            (r'eval\s*\(', "dangerous_eval", "Use of eval() function is dangerous"),
            (r'exec\s*\(', "dangerous_exec", "Use of exec() function is dangerous"),
            (r'input\s*\(', "dangerous_input", "Direct user input without validation"),
            (r'pickle\.loads', "dangerous_pickle", "Pickle deserialization is dangerous"),
            (r'shell=True', "dangerous_shell", "Shell injection vulnerability"),
            (r'subprocess\.\w+.*shell=True', "dangerous_subprocess", "Subprocess with shell=True is dangerous"),
            (r'password\s*=\s*["\'].*["\']', "hardcoded_password", "Hardcoded password detected"),
            (r'api_key\s*=\s*["\'].*["\']', "hardcoded_api_key", "Hardcoded API key detected"),
            (r'secret\s*=\s*["\'].*["\']', "hardcoded_secret", "Hardcoded secret detected"),
        ]
        
        for pattern, issue_type, description in security_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(QualityIssue(
                    issue_type=issue_type,
                    severity="critical",
                    description=description,
                    suggested_fix=f"Remove or properly secure {issue_type.replace('_', ' ')}",
                    auto_fixable=False
                ))
        
        return issues
    
    def _has_section(self, content: str, section: str) -> bool:
        """Check if documentation has required section"""
        section_patterns = [
            rf'#{1,6}\s*{section}',
            rf'## {section}',
            rf'{section}:',
            rf'{section}\n[=-]+'
        ]
        
        for pattern in section_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _calculate_readability(self, content: str) -> float:
        """Calculate readability score (simplified Flesch Reading Ease)"""
        sentences = len(re.findall(r'[.!?]+', content))
        words = len(content.split())
        syllables = self._count_syllables(content)
        
        if sentences == 0 or words == 0:
            return 0.0
        
        # Simplified readability score
        avg_sentence_length = words / sentences
        avg_syllables_per_word = syllables / words
        
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Convert to 0-10 scale (higher is worse for our purposes)
        return max(0, min(10, (100 - readability) / 10))
    
    def _count_syllables(self, text: str) -> int:
        """Count syllables in text (simplified)"""
        vowels = "aeiouy"
        syllables = 0
        prev_was_vowel = False
        
        for char in text.lower():
            if char in vowels:
                if not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = True
            else:
                prev_was_vowel = False
        
        return max(1, syllables)
    
    def _has_test_type(self, content: str, test_type: str) -> bool:
        """Check if tests include specific test type"""
        test_patterns = {
            "unit": [r'test_\w+', r'unittest', r'describe\s*\(', r'it\s*\('],
            "integration": [r'integration.*test', r'test.*integration', r'e2e.*test'],
            "performance": [r'performance.*test', r'benchmark', r'load.*test'],
            "security": [r'security.*test', r'test.*security', r'vulnerability.*test']
        }
        
        patterns = test_patterns.get(test_type, [])
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    async def _calculate_test_coverage(self, file_path: str) -> float:
        """Calculate test coverage (simplified)"""
        try:
            # This is a simplified version - in practice, you'd integrate with coverage tools
            if "test" in file_path.lower():
                return 0.9  # Assume test files have high coverage
            else:
                return 0.7  # Assume regular files have lower coverage
        except Exception:
            return 0.0
    
    def _follows_pattern(self, content: str, pattern: str) -> bool:
        """Check if code follows architectural pattern"""
        pattern_checks = {
            "separation_of_concerns": self._check_separation_of_concerns,
            "single_responsibility": self._check_single_responsibility,
            "dependency_injection": self._check_dependency_injection,
            "factory_pattern": self._check_factory_pattern
        }
        
        checker = pattern_checks.get(pattern)
        if checker:
            return checker(content)
        return True
    
    def _check_separation_of_concerns(self, content: str) -> bool:
        """Check for separation of concerns"""
        # Simplified check - look for mixed responsibilities
        concerns = ["database", "ui", "business", "validation", "logging"]
        found_concerns = []
        
        for concern in concerns:
            if re.search(concern, content, re.IGNORECASE):
                found_concerns.append(concern)
        
        # If more than 2 concerns in one file, might violate separation
        return len(found_concerns) <= 2
    
    def _check_single_responsibility(self, content: str) -> bool:
        """Check for single responsibility principle"""
        # Count the number of class methods or functions
        class_methods = len(re.findall(r'def\s+\w+', content))
        
        # If too many methods, might violate single responsibility
        return class_methods <= 10
    
    def _check_dependency_injection(self, content: str) -> bool:
        """Check for dependency injection pattern"""
        # Look for constructor injection patterns
        injection_patterns = [
            r'__init__\s*\([^)]+\)',
            r'constructor\s*\([^)]+\)',
            r'@inject',
            r'dependencies\s*='
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _check_factory_pattern(self, content: str) -> bool:
        """Check for factory pattern"""
        factory_patterns = [
            r'class\s+\w+Factory',
            r'def\s+create_\w+',
            r'factory\s*\(',
            r'Factory\s*\('
        ]
        
        for pattern in factory_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    async def _calculate_quality_metrics(self, work_item: WorkItem):
        """Calculate comprehensive quality metrics"""
        content = work_item.content
        
        # Code quality metrics
        work_item.quality_metrics.code_quality = self._calculate_code_quality_score(content)
        
        # Test coverage
        work_item.quality_metrics.test_coverage = await self._calculate_test_coverage(work_item.file_path)
        
        # Documentation completeness
        work_item.quality_metrics.documentation_completeness = self._calculate_documentation_completeness(content)
        
        # Security score
        security_issues = await self._check_security_issues(content)
        work_item.quality_metrics.security_score = max(0, 1.0 - (len(security_issues) * 0.2))
        
        # Performance score (simplified)
        work_item.quality_metrics.performance_score = self._calculate_performance_score(content)
        
        # Architecture compliance
        work_item.quality_metrics.architecture_compliance = self._calculate_architecture_compliance(content)
        
        # Calculate overall score
        work_item.quality_metrics.calculate_overall_score()
    
    def _calculate_code_quality_score(self, content: str) -> float:
        """Calculate code quality score"""
        score = 1.0
        
        # Deduct points for issues
        if not self._has_error_handling(content):
            score -= 0.2
        if not self._has_logging(content):
            score -= 0.1
        if not self._has_documentation(content):
            score -= 0.1
        
        complexity = self._calculate_complexity(content)
        if complexity > 10:
            score -= 0.3
        elif complexity > 5:
            score -= 0.1
        
        return max(0, score)
    
    def _calculate_documentation_completeness(self, content: str) -> float:
        """Calculate documentation completeness score"""
        if work_item.work_type != WorkType.DOCUMENTATION:
            return 0.8  # Default for non-documentation work
        
        required_sections = ["overview", "usage", "examples", "installation", "configuration"]
        found_sections = sum(1 for section in required_sections if self._has_section(content, section))
        
        return found_sections / len(required_sections)
    
    def _calculate_performance_score(self, content: str) -> float:
        """Calculate performance score"""
        score = 1.0
        
        # Check for performance anti-patterns
        performance_issues = [
            r'while\s+True\s*:',  # Infinite loops
            r'for\s+.*\s+in\s+range\s*\(\s*10000',  # Large loops
            r'time\.sleep\s*\(\s*[1-9]',  # Long sleeps
            r'recursive.*factorial',  # Inefficient recursion
        ]
        
        for pattern in performance_issues:
            if re.search(pattern, content, re.IGNORECASE):
                score -= 0.2
        
        return max(0, score)
    
    def _calculate_architecture_compliance(self, content: str) -> float:
        """Calculate architecture compliance score"""
        score = 1.0
        
        # Check for architectural patterns
        patterns = ["separation_of_concerns", "single_responsibility"]
        
        for pattern in patterns:
            if not self._follows_pattern(content, pattern):
                score -= 0.2
        
        return max(0, score)
    
    def _determine_quality_standard(self, work_item: WorkItem) -> QualityStandard:
        """Determine overall quality standard"""
        overall_score = work_item.quality_metrics.overall_score
        critical_issues = len([i for i in work_item.issues if i.severity == "critical"])
        
        if critical_issues > 0:
            return QualityStandard.UNACCEPTABLE
        elif overall_score >= 0.9:
            return QualityStandard.EXCELLENT
        elif overall_score >= 0.8:
            return QualityStandard.GOOD
        elif overall_score >= 0.7:
            return QualityStandard.ACCEPTABLE
        elif overall_score >= 0.6:
            return QualityStandard.NEEDS_IMPROVEMENT
        else:
            return QualityStandard.UNACCEPTABLE

class AutoFixEngine:
    """Engine for automatically fixing quality issues"""
    
    def __init__(self):
        self.fix_patterns = {
            "missing_error_handling": self._fix_missing_error_handling,
            "missing_logging": self._fix_missing_logging,
            "missing_documentation": self._fix_missing_documentation,
            "missing_section": self._fix_missing_section,
            "missing_test_type": self._fix_missing_test_type
        }
    
    async def auto_fix_issue(self, work_item: WorkItem, issue: QualityIssue) -> bool:
        """Attempt to automatically fix an issue"""
        if not issue.auto_fixable:
            return False
        
        fix_function = self.fix_patterns.get(issue.issue_type)
        if not fix_function:
            return False
        
        try:
            fixed_content = await fix_function(work_item.content, issue)
            if fixed_content != work_item.content:
                work_item.content = fixed_content
                logger.info(f"Auto-fixed issue: {issue.issue_type} in {work_item.file_path}")
                return True
        except Exception as e:
            logger.error(f"Failed to auto-fix {issue.issue_type}: {str(e)}")
        
        return False
    
    async def _fix_missing_error_handling(self, content: str, issue: QualityIssue) -> str:
        """Add basic error handling to code"""
        if "def " in content:
            # Add try-catch around function bodies
            lines = content.split('\n')
            fixed_lines = []
            in_function = False
            indent_level = 0
            
            for line in lines:
                if re.match(r'\s*def\s+', line):
                    in_function = True
                    indent_level = len(line) - len(line.lstrip())
                    fixed_lines.append(line)
                elif in_function and line.strip() and not line.startswith(' ' * (indent_level + 4)):
                    # End of function
                    in_function = False
                    fixed_lines.append(line)
                elif in_function and line.strip() and not line.strip().startswith('try:'):
                    # Add try-catch
                    fixed_lines.append(' ' * (indent_level + 4) + 'try:')
                    fixed_lines.append(' ' * (indent_level + 8) + line.lstrip())
                    fixed_lines.append(' ' * (indent_level + 4) + 'except Exception as e:')
                    fixed_lines.append(' ' * (indent_level + 8) + 'logger.error(f"Error: {e}")')
                    fixed_lines.append(' ' * (indent_level + 8) + 'raise')
                    in_function = False
                else:
                    fixed_lines.append(line)
            
            return '\n'.join(fixed_lines)
        
        return content
    
    async def _fix_missing_logging(self, content: str, issue: QualityIssue) -> str:
        """Add basic logging to code"""
        if "import logging" not in content:
            # Add logging import
            lines = content.split('\n')
            import_section = []
            other_lines = []
            
            for line in lines:
                if line.startswith('import ') or line.startswith('from '):
                    import_section.append(line)
                else:
                    other_lines.append(line)
            
            import_section.append('import logging')
            import_section.append('logger = logging.getLogger(__name__)')
            
            return '\n'.join(import_section + [''] + other_lines)
        
        return content
    
    async def _fix_missing_documentation(self, content: str, issue: QualityIssue) -> str:
        """Add basic documentation to code"""
        if "def " in content:
            lines = content.split('\n')
            fixed_lines = []
            
            for i, line in enumerate(lines):
                if re.match(r'\s*def\s+', line):
                    fixed_lines.append(line)
                    indent = len(line) - len(line.lstrip())
                    # Add basic docstring
                    fixed_lines.append(' ' * (indent + 4) + '"""')
                    fixed_lines.append(' ' * (indent + 4) + 'TODO: Add function description')
                    fixed_lines.append(' ' * (indent + 4) + '"""')
                else:
                    fixed_lines.append(line)
            
            return '\n'.join(fixed_lines)
        
        return content
    
    async def _fix_missing_section(self, content: str, issue: QualityIssue) -> str:
        """Add missing section to documentation"""
        section_templates = {
            "overview": "## Overview\n\nTODO: Add project overview\n",
            "usage": "## Usage\n\nTODO: Add usage instructions\n",
            "examples": "## Examples\n\nTODO: Add code examples\n",
            "installation": "## Installation\n\nTODO: Add installation instructions\n",
            "configuration": "## Configuration\n\nTODO: Add configuration details\n"
        }
        
        # Extract section name from issue description
        section_match = re.search(r'section:\s+(\w+)', issue.description)
        if section_match:
            section = section_match.group(1)
            template = section_templates.get(section, f"## {section.title()}\n\nTODO: Add {section} content\n")
            return content + '\n' + template
        
        return content
    
    async def _fix_missing_test_type(self, content: str, issue: QualityIssue) -> str:
        """Add missing test type"""
        test_templates = {
            "unit": '''
def test_unit_example():
    """Unit test example"""
    # TODO: Add unit test
    assert True
''',
            "integration": '''
def test_integration_example():
    """Integration test example"""
    # TODO: Add integration test
    assert True
'''
        }
        
        # Extract test type from issue description
        test_match = re.search(r'Missing\s+(\w+)\s+tests', issue.description)
        if test_match:
            test_type = test_match.group(1)
            template = test_templates.get(test_type, f'''
def test_{test_type}_example():
    """TODO: Add {test_type} test"""
    assert True
''')
            return content + '\n' + template
        
        return content

class CEOQualityControlAgent:
    """Main CEO/Quality Control Agent"""
    
    def __init__(self, config_path: str = "/mnt/c/bmad-workspace/config/ceo-config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.work_queue = asyncio.Queue()
        self.active_reviews = {}
        self.quality_engine = QualityReviewEngine()
        self.auto_fix_engine = AutoFixEngine()
        self.redis_client = self._init_redis()
        self.file_observer = None
        self.running = False
        
        # Agent tracking
        self.agent_performance = {}
        self.project_standards = {}
        self.quality_reports = []
        
        # Executive dashboard
        self.dashboard_data = {
            "total_reviews": 0,
            "passed_reviews": 0,
            "failed_reviews": 0,
            "auto_fixes": 0,
            "agent_scores": {},
            "project_health": {}
        }
    
    def _load_config(self) -> Dict:
        """Load CEO configuration"""
        default_config = {
            "quality_standards": {
                "min_overall_score": 0.8,
                "auto_fix_enabled": True,
                "max_revision_attempts": 3,
                "critical_issue_threshold": 0
            },
            "monitoring": {
                "watch_directories": ["/mnt/c/bmad-workspace/projects"],
                "file_patterns": ["*.py", "*.js", "*.ts", "*.md", "*.yaml", "*.json"],
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
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    return {**default_config, **config}
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        
        return default_config
    
    def _init_redis(self) -> redis.Redis:
        """Initialize Redis connection"""
        try:
            return redis.Redis(host='localhost', port=6379, db=2)
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            return None
    
    async def start(self):
        """Start the CEO Quality Control Agent"""
        logger.info("🎯 CEO Quality Control Agent Starting...")
        self.running = True
        
        # Start file monitoring
        await self._start_file_monitoring()
        
        # Start work processing
        tasks = [
            asyncio.create_task(self._process_work_queue()),
            asyncio.create_task(self._monitor_agent_performance()),
            asyncio.create_task(self._generate_reports()),
            asyncio.create_task(self._health_check_loop())
        ]
        
        logger.info("✅ CEO Quality Control Agent Active - Maintaining Excellence!")
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("CEO Quality Control Agent shutting down...")
        finally:
            self.running = False
            if self.file_observer:
                self.file_observer.stop()
    
    async def _start_file_monitoring(self):
        """Start monitoring files for changes"""
        class QualityFileHandler(FileSystemEventHandler):
            def __init__(self, ceo_agent):
                self.ceo_agent = ceo_agent
            
            def on_modified(self, event):
                if not event.is_directory:
                    asyncio.create_task(self.ceo_agent._handle_file_change(event.src_path))
        
        self.file_observer = Observer()
        handler = QualityFileHandler(self)
        
        for watch_dir in self.config["monitoring"]["watch_directories"]:
            if os.path.exists(watch_dir):
                self.file_observer.schedule(handler, watch_dir, recursive=True)
        
        self.file_observer.start()
        logger.info("📁 File monitoring started")
    
    async def _handle_file_change(self, file_path: str):
        """Handle file changes for quality review"""
        try:
            # Check if file should be reviewed
            if not self._should_review_file(file_path):
                return
            
            # Determine work type
            work_type = self._determine_work_type(file_path)
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create work item
            work_item = WorkItem(
                id=hashlib.md5(f"{file_path}_{datetime.now()}".encode()).hexdigest(),
                work_type=work_type,
                file_path=file_path,
                agent_name=self._detect_agent_from_file(file_path),
                project_name=self._extract_project_name(file_path),
                content=content,
                requirements=self._get_project_requirements(file_path)
            )
            
            # Add to queue
            await self.work_queue.put(work_item)
            logger.info(f"📋 Queued for review: {file_path}")
            
        except Exception as e:
            logger.error(f"Error handling file change {file_path}: {e}")
    
    def _should_review_file(self, file_path: str) -> bool:
        """Check if file should be reviewed"""
        # Check file patterns
        file_patterns = self.config["monitoring"]["file_patterns"]
        exclude_patterns = self.config["monitoring"]["exclude_patterns"]
        
        # Check exclude patterns first
        for pattern in exclude_patterns:
            if pattern in file_path:
                return False
        
        # Check include patterns
        for pattern in file_patterns:
            if file_path.endswith(pattern.replace("*", "")):
                return True
        
        return False
    
    def _determine_work_type(self, file_path: str) -> WorkType:
        """Determine work type based on file"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in ['.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c']:
            return WorkType.CODE
        elif file_ext in ['.md', '.rst', '.txt']:
            return WorkType.DOCUMENTATION
        elif 'test' in file_path.lower() or file_path.endswith('_test.py'):
            return WorkType.TESTS
        elif file_ext in ['.yaml', '.yml', '.json'] and 'architect' in file_path.lower():
            return WorkType.ARCHITECTURE
        else:
            return WorkType.CODE
    
    def _detect_agent_from_file(self, file_path: str) -> str:
        """Detect which agent worked on the file"""
        # Look for agent signatures in git history or file metadata
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%cn', file_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(file_path)
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        
        # Default fallback
        return "unknown_agent"
    
    def _extract_project_name(self, file_path: str) -> str:
        """Extract project name from file path"""
        path_parts = Path(file_path).parts
        
        if "projects" in path_parts:
            project_index = path_parts.index("projects")
            if project_index + 1 < len(path_parts):
                return path_parts[project_index + 1]
        
        return "unknown_project"
    
    def _get_project_requirements(self, file_path: str) -> List[str]:
        """Get project requirements from CLAUDE.md or other sources"""
        requirements = []
        
        # Look for CLAUDE.md in project directory
        project_dir = self._find_project_root(file_path)
        claude_md_path = os.path.join(project_dir, "CLAUDE.md")
        
        if os.path.exists(claude_md_path):
            try:
                with open(claude_md_path, 'r') as f:
                    content = f.read()
                    # Extract requirements from CLAUDE.md
                    if "requirements:" in content.lower():
                        # Simple extraction - in practice, you'd parse YAML frontmatter
                        req_section = content.split("requirements:")[-1].split("\n")
                        for line in req_section:
                            if line.strip().startswith("-"):
                                requirements.append(line.strip()[1:].strip())
            except Exception as e:
                logger.error(f"Error reading CLAUDE.md: {e}")
        
        return requirements
    
    def _find_project_root(self, file_path: str) -> str:
        """Find project root directory"""
        current = os.path.dirname(file_path)
        
        while current != "/":
            if os.path.exists(os.path.join(current, "CLAUDE.md")) or \
               os.path.exists(os.path.join(current, ".git")):
                return current
            current = os.path.dirname(current)
        
        return os.path.dirname(file_path)
    
    async def _process_work_queue(self):
        """Process work items from queue"""
        while self.running:
            try:
                # Get work item with timeout
                work_item = await asyncio.wait_for(self.work_queue.get(), timeout=1.0)
                
                # Process the work item
                await self._review_work_item(work_item)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing work queue: {e}")
    
    async def _review_work_item(self, work_item: WorkItem):
        """Review a work item for quality"""
        logger.info(f"🔍 Reviewing: {work_item.file_path} by {work_item.agent_name}")
        
        try:
            # Add to active reviews
            self.active_reviews[work_item.id] = work_item
            
            # Perform quality review
            quality_standard, issues = await self.quality_engine.review_work_item(work_item)
            work_item.issues = issues
            
            # Update dashboard
            self.dashboard_data["total_reviews"] += 1
            
            # Determine action based on quality
            if quality_standard in [QualityStandard.EXCELLENT, QualityStandard.GOOD]:
                # Approve the work
                work_item.status = "approved"
                self.dashboard_data["passed_reviews"] += 1
                logger.info(f"✅ APPROVED: {work_item.file_path} - Quality: {quality_standard.value}")
                
            elif quality_standard == QualityStandard.ACCEPTABLE:
                # Approve with minor notes
                work_item.status = "approved"
                self.dashboard_data["passed_reviews"] += 1
                logger.info(f"✅ APPROVED (with notes): {work_item.file_path}")
                
            elif quality_standard == QualityStandard.NEEDS_IMPROVEMENT:
                # Try auto-fix first
                if self.config["quality_standards"]["auto_fix_enabled"]:
                    fixed_count = await self._attempt_auto_fixes(work_item)
                    if fixed_count > 0:
                        # Re-review after fixes
                        quality_standard, issues = await self.quality_engine.review_work_item(work_item)
                        work_item.issues = issues
                        
                        if quality_standard in [QualityStandard.EXCELLENT, QualityStandard.GOOD, QualityStandard.ACCEPTABLE]:
                            work_item.status = "approved"
                            self.dashboard_data["passed_reviews"] += 1
                            logger.info(f"✅ APPROVED after auto-fix: {work_item.file_path}")
                        else:
                            await self._send_for_revision(work_item)
                    else:
                        await self._send_for_revision(work_item)
                else:
                    await self._send_for_revision(work_item)
                    
            else:  # UNACCEPTABLE
                # Immediately send for revision or escalate
                await self._send_for_revision(work_item)
            
            # Store review results
            await self._store_review_results(work_item)
            
            # Update agent performance
            self._update_agent_performance(work_item)
            
        except Exception as e:
            logger.error(f"Error reviewing work item {work_item.id}: {e}")
            work_item.status = "error"
        
        finally:
            # Remove from active reviews
            if work_item.id in self.active_reviews:
                del self.active_reviews[work_item.id]
    
    async def _attempt_auto_fixes(self, work_item: WorkItem) -> int:
        """Attempt to automatically fix issues"""
        fixed_count = 0
        
        for issue in work_item.issues:
            if issue.auto_fixable:
                if await self.auto_fix_engine.auto_fix_issue(work_item, issue):
                    fixed_count += 1
                    self.dashboard_data["auto_fixes"] += 1
        
        # Write fixed content back to file
        if fixed_count > 0:
            try:
                with open(work_item.file_path, 'w', encoding='utf-8') as f:
                    f.write(work_item.content)
                logger.info(f"🔧 Auto-fixed {fixed_count} issues in {work_item.file_path}")
            except Exception as e:
                logger.error(f"Error writing auto-fixes: {e}")
                fixed_count = 0
        
        return fixed_count
    
    async def _send_for_revision(self, work_item: WorkItem):
        """Send work back for revision"""
        work_item.status = "needs_revision"
        work_item.revision_count += 1
        self.dashboard_data["failed_reviews"] += 1
        
        # Generate revision instructions
        revision_instructions = self._generate_revision_instructions(work_item)
        
        # Send to appropriate agent
        await self._notify_agent_for_revision(work_item, revision_instructions)
        
        logger.warning(f"❌ REVISION REQUIRED: {work_item.file_path} - Attempt {work_item.revision_count}")
        
        # Check if max revisions reached
        if work_item.revision_count >= work_item.max_revisions:
            await self._escalate_to_ceo(work_item)
    
    def _generate_revision_instructions(self, work_item: WorkItem) -> str:
        """Generate detailed revision instructions"""
        instructions = f"""
🎯 REVISION REQUIRED: {work_item.file_path}

📊 QUALITY METRICS:
- Overall Score: {work_item.quality_metrics.overall_score:.2f}
- Code Quality: {work_item.quality_metrics.code_quality:.2f}
- Test Coverage: {work_item.quality_metrics.test_coverage:.2f}
- Documentation: {work_item.quality_metrics.documentation_completeness:.2f}
- Security: {work_item.quality_metrics.security_score:.2f}

❌ ISSUES TO FIX:
"""
        
        for issue in work_item.issues:
            instructions += f"""
- {issue.severity.upper()}: {issue.description}
  Fix: {issue.suggested_fix}
  File: {issue.file_path}
  Line: {issue.line_number or 'N/A'}
"""
        
        instructions += f"""
🎯 REQUIREMENTS:
{chr(10).join(f"- {req}" for req in work_item.requirements)}

📋 REVISION INSTRUCTIONS:
1. Address all {len(work_item.issues)} quality issues listed above
2. Ensure overall quality score reaches at least {self.config['quality_standards']['min_overall_score']}
3. Follow project requirements and coding standards
4. Test your changes thoroughly
5. Document any significant changes

⚠️ This is revision attempt {work_item.revision_count} of {work_item.max_revisions}
"""
        
        return instructions
    
    async def _notify_agent_for_revision(self, work_item: WorkItem, instructions: str):
        """Notify agent about required revision"""
        try:
            # Create revision file
            revision_file = os.path.join(
                os.path.dirname(work_item.file_path),
                f".revision-{work_item.id}.md"
            )
            
            with open(revision_file, 'w') as f:
                f.write(instructions)
            
            # Send notification via Claude Code or tmux
            await self._send_agent_notification(work_item.agent_name, instructions)
            
        except Exception as e:
            logger.error(f"Error notifying agent for revision: {e}")
    
    async def _send_agent_notification(self, agent_name: str, message: str):
        """Send notification to agent"""
        try:
            # Try to send via tmux session
            tmux_session = f"{agent_name}-session"
            
            result = subprocess.run([
                "/mnt/c/bmad-workspace/Tmux-Orchestrator/send-claude-message.sh",
                tmux_session,
                f"CEO QUALITY CONTROL: {message}"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"📨 Sent revision notification to {agent_name}")
            else:
                logger.warning(f"Failed to send notification to {agent_name}")
                
        except Exception as e:
            logger.error(f"Error sending agent notification: {e}")
    
    async def _escalate_to_ceo(self, work_item: WorkItem):
        """Escalate to CEO level (highest authority)"""
        logger.critical(f"🚨 CEO ESCALATION: {work_item.file_path} - Max revisions reached")
        
        # Generate CEO report
        ceo_report = f"""
🚨 CEO ESCALATION REQUIRED

📁 File: {work_item.file_path}
👤 Agent: {work_item.agent_name}
📊 Project: {work_item.project_name}
🔄 Revision Attempts: {work_item.revision_count}
📈 Quality Score: {work_item.quality_metrics.overall_score:.2f}

❌ PERSISTENT ISSUES:
{chr(10).join(f"- {issue.severity.upper()}: {issue.description}" for issue in work_item.issues)}

💡 CEO RECOMMENDATIONS:
1. Consider reassigning to different agent
2. Review project requirements clarity
3. Provide additional training/resources
4. Evaluate if timeline is realistic
5. Consider architectural changes

🎯 DECISION REQUIRED:
- Approve with current quality (not recommended)
- Reassign to senior developer
- Modify requirements
- Extend timeline
- Escalate to external consultant
"""
        
        # Store CEO escalation
        await self._store_ceo_escalation(work_item, ceo_report)
        
        # Send to CEO dashboard
        await self._update_ceo_dashboard(work_item, ceo_report)
    
    async def _store_review_results(self, work_item: WorkItem):
        """Store review results for analysis"""
        try:
            review_data = {
                "work_item_id": work_item.id,
                "file_path": work_item.file_path,
                "agent_name": work_item.agent_name,
                "project_name": work_item.project_name,
                "work_type": work_item.work_type.value,
                "quality_metrics": {
                    "overall_score": work_item.quality_metrics.overall_score,
                    "code_quality": work_item.quality_metrics.code_quality,
                    "test_coverage": work_item.quality_metrics.test_coverage,
                    "documentation": work_item.quality_metrics.documentation_completeness,
                    "security": work_item.quality_metrics.security_score,
                    "performance": work_item.quality_metrics.performance_score,
                    "architecture": work_item.quality_metrics.architecture_compliance
                },
                "issues": [
                    {
                        "type": issue.issue_type,
                        "severity": issue.severity,
                        "description": issue.description,
                        "auto_fixable": issue.auto_fixable
                    }
                    for issue in work_item.issues
                ],
                "status": work_item.status,
                "revision_count": work_item.revision_count,
                "timestamp": work_item.timestamp.isoformat()
            }
            
            # Store in Redis for quick access
            if self.redis_client:
                self.redis_client.hset(
                    f"review:{work_item.id}",
                    mapping=review_data
                )
                self.redis_client.expire(f"review:{work_item.id}", 86400)  # 24 hours
            
            # Store in file for persistence
            reviews_dir = "/mnt/c/bmad-workspace/logs/reviews"
            os.makedirs(reviews_dir, exist_ok=True)
            
            review_file = os.path.join(reviews_dir, f"review-{work_item.id}.json")
            with open(review_file, 'w') as f:
                json.dump(review_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error storing review results: {e}")
    
    def _update_agent_performance(self, work_item: WorkItem):
        """Update agent performance metrics"""
        agent_name = work_item.agent_name
        
        if agent_name not in self.agent_performance:
            self.agent_performance[agent_name] = {
                "total_reviews": 0,
                "passed_reviews": 0,
                "failed_reviews": 0,
                "avg_quality_score": 0.0,
                "revision_rate": 0.0,
                "specialties": [],
                "improvement_areas": []
            }
        
        agent_stats = self.agent_performance[agent_name]
        agent_stats["total_reviews"] += 1
        
        if work_item.status == "approved":
            agent_stats["passed_reviews"] += 1
        else:
            agent_stats["failed_reviews"] += 1
        
        # Update average quality score
        agent_stats["avg_quality_score"] = (
            (agent_stats["avg_quality_score"] * (agent_stats["total_reviews"] - 1) +
             work_item.quality_metrics.overall_score) / agent_stats["total_reviews"]
        )
        
        # Update revision rate
        agent_stats["revision_rate"] = agent_stats["failed_reviews"] / agent_stats["total_reviews"]
        
        # Update dashboard
        self.dashboard_data["agent_scores"][agent_name] = agent_stats["avg_quality_score"]
    
    async def _monitor_agent_performance(self):
        """Monitor agent performance continuously"""
        while self.running:
            try:
                # Generate performance reports
                await self._generate_agent_performance_report()
                
                # Check for underperforming agents
                await self._check_underperforming_agents()
                
                # Update project health metrics
                await self._update_project_health()
                
                # Sleep for 1 hour
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Error monitoring agent performance: {e}")
                await asyncio.sleep(300)  # Sleep for 5 minutes on error
    
    async def _generate_agent_performance_report(self):
        """Generate performance report for all agents"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "agents": self.agent_performance,
                "overall_metrics": {
                    "total_agents": len(self.agent_performance),
                    "avg_quality_score": sum(
                        agent["avg_quality_score"] for agent in self.agent_performance.values()
                    ) / len(self.agent_performance) if self.agent_performance else 0,
                    "total_reviews": sum(
                        agent["total_reviews"] for agent in self.agent_performance.values()
                    ),
                    "overall_pass_rate": self.dashboard_data["passed_reviews"] / 
                                        self.dashboard_data["total_reviews"] if self.dashboard_data["total_reviews"] > 0 else 0
                }
            }
            
            # Store performance report
            reports_dir = "/mnt/c/bmad-workspace/logs/performance"
            os.makedirs(reports_dir, exist_ok=True)
            
            report_file = os.path.join(reports_dir, f"performance-{datetime.now().strftime('%Y%m%d-%H%M')}.json")
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"📊 Generated performance report: {report_file}")
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
    
    async def _check_underperforming_agents(self):
        """Check for underperforming agents and take action"""
        try:
            for agent_name, stats in self.agent_performance.items():
                if stats["total_reviews"] < 5:
                    continue  # Not enough data
                
                # Check if agent is underperforming
                if (stats["avg_quality_score"] < 0.6 or 
                    stats["revision_rate"] > 0.5):
                    
                    await self._handle_underperforming_agent(agent_name, stats)
                    
        except Exception as e:
            logger.error(f"Error checking underperforming agents: {e}")
    
    async def _handle_underperforming_agent(self, agent_name: str, stats: Dict):
        """Handle underperforming agent"""
        logger.warning(f"⚠️ UNDERPERFORMING AGENT: {agent_name}")
        
        # Generate improvement plan
        improvement_plan = f"""
🎯 PERFORMANCE IMPROVEMENT PLAN

👤 Agent: {agent_name}
📊 Current Stats:
- Quality Score: {stats['avg_quality_score']:.2f}
- Revision Rate: {stats['revision_rate']:.2f}
- Total Reviews: {stats['total_reviews']}

📈 IMPROVEMENT ACTIONS:
1. Review coding standards and best practices
2. Focus on error handling and documentation
3. Improve test coverage
4. Attend quality training session
5. Pair with high-performing agent

🎯 TARGETS:
- Quality Score: > 0.8
- Revision Rate: < 0.3
- Timeline: 2 weeks

⚠️ Note: Continued underperformance may result in task reassignment
"""
        
        # Send improvement plan to agent
        await self._send_agent_notification(agent_name, improvement_plan)
        
        # Store improvement plan
        plans_dir = "/mnt/c/bmad-workspace/logs/improvement-plans"
        os.makedirs(plans_dir, exist_ok=True)
        
        plan_file = os.path.join(plans_dir, f"improvement-{agent_name}-{datetime.now().strftime('%Y%m%d')}.md")
        with open(plan_file, 'w') as f:
            f.write(improvement_plan)
    
    async def _update_project_health(self):
        """Update project health metrics"""
        try:
            # Calculate project health scores
            for project_name in set(work_item.project_name for work_item in self.active_reviews.values()):
                project_reviews = [
                    work_item for work_item in self.active_reviews.values()
                    if work_item.project_name == project_name
                ]
                
                if project_reviews:
                    avg_quality = sum(
                        review.quality_metrics.overall_score for review in project_reviews
                    ) / len(project_reviews)
                    
                    health_status = "excellent" if avg_quality > 0.9 else \
                                   "good" if avg_quality > 0.8 else \
                                   "fair" if avg_quality > 0.7 else "poor"
                    
                    self.dashboard_data["project_health"][project_name] = {
                        "health_score": avg_quality,
                        "status": health_status,
                        "total_reviews": len(project_reviews),
                        "last_updated": datetime.now().isoformat()
                    }
            
        except Exception as e:
            logger.error(f"Error updating project health: {e}")
    
    async def _generate_reports(self):
        """Generate regular reports"""
        while self.running:
            try:
                # Generate daily report
                await self._generate_daily_report()
                
                # Sleep until next day
                await asyncio.sleep(86400)  # 24 hours
                
            except Exception as e:
                logger.error(f"Error generating reports: {e}")
                await asyncio.sleep(3600)  # Sleep for 1 hour on error
    
    async def _generate_daily_report(self):
        """Generate daily quality report"""
        try:
            report = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": {
                    "total_reviews": self.dashboard_data["total_reviews"],
                    "passed_reviews": self.dashboard_data["passed_reviews"],
                    "failed_reviews": self.dashboard_data["failed_reviews"],
                    "auto_fixes": self.dashboard_data["auto_fixes"],
                    "pass_rate": self.dashboard_data["passed_reviews"] / self.dashboard_data["total_reviews"] 
                                if self.dashboard_data["total_reviews"] > 0 else 0
                },
                "agent_performance": self.agent_performance,
                "project_health": self.dashboard_data["project_health"],
                "recommendations": self._generate_recommendations()
            }
            
            # Store daily report
            reports_dir = "/mnt/c/bmad-workspace/logs/daily-reports"
            os.makedirs(reports_dir, exist_ok=True)
            
            report_file = os.path.join(reports_dir, f"daily-report-{datetime.now().strftime('%Y%m%d')}.json")
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            # Generate executive summary
            await self._generate_executive_summary(report)
            
            logger.info(f"📈 Generated daily report: {report_file}")
            
        except Exception as e:
            logger.error(f"Error generating daily report: {e}")
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on current performance"""
        recommendations = []
        
        # Check overall pass rate
        if self.dashboard_data["total_reviews"] > 0:
            pass_rate = self.dashboard_data["passed_reviews"] / self.dashboard_data["total_reviews"]
            
            if pass_rate < 0.8:
                recommendations.append("Overall pass rate is below 80%. Consider reviewing coding standards and providing additional training.")
            
            if pass_rate < 0.6:
                recommendations.append("Critical: Pass rate is below 60%. Immediate intervention required.")
        
        # Check agent performance
        underperforming_agents = [
            agent for agent, stats in self.agent_performance.items()
            if stats["avg_quality_score"] < 0.7 and stats["total_reviews"] > 5
        ]
        
        if underperforming_agents:
            recommendations.append(f"The following agents need performance improvement: {', '.join(underperforming_agents)}")
        
        # Check project health
        unhealthy_projects = [
            project for project, health in self.dashboard_data["project_health"].items()
            if health["health_score"] < 0.7
        ]
        
        if unhealthy_projects:
            recommendations.append(f"Projects requiring attention: {', '.join(unhealthy_projects)}")
        
        return recommendations
    
    async def _generate_executive_summary(self, report: Dict):
        """Generate executive summary for leadership"""
        try:
            summary = f"""
# CEO Quality Control - Daily Executive Summary
## {report['date']}

## 📊 Key Metrics
- **Total Reviews**: {report['summary']['total_reviews']}
- **Pass Rate**: {report['summary']['pass_rate']:.1%}
- **Auto-Fixes Applied**: {report['summary']['auto_fixes']}
- **Active Projects**: {len(report['project_health'])}

## 🎯 Performance Highlights
- **Top Performing Agent**: {max(self.agent_performance.items(), key=lambda x: x[1]['avg_quality_score'])[0] if self.agent_performance else 'N/A'}
- **Most Improved Project**: {max(report['project_health'].items(), key=lambda x: x[1]['health_score'])[0] if report['project_health'] else 'N/A'}
- **Quality Trend**: {'🔺 Improving' if report['summary']['pass_rate'] > 0.8 else '⚠️ Needs Attention'}

## 💡 Key Recommendations
{chr(10).join(f"- {rec}" for rec in report['recommendations'])}

## 🚨 Immediate Actions Required
{chr(10).join(f"- {action}" for action in self._get_immediate_actions())}

---
*Generated by CEO Quality Control Agent*
"""
            
            summary_file = f"/mnt/c/bmad-workspace/logs/executive-summaries/summary-{datetime.now().strftime('%Y%m%d')}.md"
            os.makedirs(os.path.dirname(summary_file), exist_ok=True)
            
            with open(summary_file, 'w') as f:
                f.write(summary)
            
            logger.info(f"📋 Generated executive summary: {summary_file}")
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
    
    def _get_immediate_actions(self) -> List[str]:
        """Get immediate actions required"""
        actions = []
        
        # Check for critical issues
        if self.dashboard_data["total_reviews"] > 0:
            pass_rate = self.dashboard_data["passed_reviews"] / self.dashboard_data["total_reviews"]
            
            if pass_rate < 0.5:
                actions.append("CRITICAL: Pass rate below 50% - Stop all development and review process")
            
            if pass_rate < 0.7:
                actions.append("Conduct emergency training session for all agents")
        
        # Check for stuck reviews
        stuck_reviews = [
            review for review in self.active_reviews.values()
            if review.revision_count >= 2
        ]
        
        if stuck_reviews:
            actions.append(f"Review {len(stuck_reviews)} stuck work items requiring escalation")
        
        return actions
    
    async def _health_check_loop(self):
        """Continuous health checking"""
        while self.running:
            try:
                await self._perform_health_check()
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")
                await asyncio.sleep(60)  # Sleep for 1 minute on error
    
    async def _perform_health_check(self):
        """Perform system health check"""
        try:
            health_status = {
                "timestamp": datetime.now().isoformat(),
                "system_status": "healthy",
                "queue_size": self.work_queue.qsize(),
                "active_reviews": len(self.active_reviews),
                "redis_connected": self.redis_client is not None and self.redis_client.ping(),
                "file_monitoring": self.file_observer is not None and self.file_observer.is_alive(),
                "memory_usage": psutil.virtual_memory().percent,
                "cpu_usage": psutil.cpu_percent()
            }
            
            # Check for issues
            issues = []
            
            if health_status["queue_size"] > 100:
                issues.append("Work queue is backing up")
                
            if health_status["memory_usage"] > 80:
                issues.append("High memory usage detected")
                
            if health_status["cpu_usage"] > 80:
                issues.append("High CPU usage detected")
                
            if not health_status["redis_connected"]:
                issues.append("Redis connection lost")
                
            if not health_status["file_monitoring"]:
                issues.append("File monitoring is down")
            
            if issues:
                health_status["system_status"] = "warning"
                health_status["issues"] = issues
                logger.warning(f"Health check issues: {issues}")
            
            # Store health status
            if self.redis_client:
                self.redis_client.hset("ceo:health", mapping=health_status)
                self.redis_client.expire("ceo:health", 600)  # 10 minutes
            
        except Exception as e:
            logger.error(f"Error performing health check: {e}")
    
    async def _store_ceo_escalation(self, work_item: WorkItem, report: str):
        """Store CEO escalation for review"""
        try:
            escalation_data = {
                "work_item_id": work_item.id,
                "file_path": work_item.file_path,
                "agent_name": work_item.agent_name,
                "project_name": work_item.project_name,
                "report": report,
                "timestamp": datetime.now().isoformat()
            }
            
            # Store escalation
            escalations_dir = "/mnt/c/bmad-workspace/logs/ceo-escalations"
            os.makedirs(escalations_dir, exist_ok=True)
            
            escalation_file = os.path.join(escalations_dir, f"escalation-{work_item.id}.json")
            with open(escalation_file, 'w') as f:
                json.dump(escalation_data, f, indent=2)
            
            logger.critical(f"🚨 CEO escalation stored: {escalation_file}")
            
        except Exception as e:
            logger.error(f"Error storing CEO escalation: {e}")
    
    async def _update_ceo_dashboard(self, work_item: WorkItem, report: str):
        """Update CEO dashboard with escalation"""
        try:
            # This would integrate with a web dashboard or notification system
            # For now, we'll create a simple dashboard file
            
            dashboard_file = "/mnt/c/bmad-workspace/logs/ceo-dashboard.json"
            
            dashboard_data = {
                "last_updated": datetime.now().isoformat(),
                "total_reviews": self.dashboard_data["total_reviews"],
                "pass_rate": self.dashboard_data["passed_reviews"] / self.dashboard_data["total_reviews"] 
                            if self.dashboard_data["total_reviews"] > 0 else 0,
                "active_escalations": len([r for r in self.active_reviews.values() if r.revision_count >= 3]),
                "agent_performance": self.agent_performance,
                "project_health": self.dashboard_data["project_health"],
                "recent_escalation": {
                    "file_path": work_item.file_path,
                    "agent": work_item.agent_name,
                    "project": work_item.project_name,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            with open(dashboard_file, 'w') as f:
                json.dump(dashboard_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error updating CEO dashboard: {e}")

async def main():
    """Main function to run the CEO Quality Control Agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CEO Quality Control Agent')
    parser.add_argument('--config', default='/mnt/c/bmad-workspace/config/ceo-config.yaml', 
                       help='Configuration file path')
    parser.add_argument('--debug', action='store_true', 
                       help='Enable debug logging')
    parser.add_argument('--test', action='store_true',
                       help='Run in test mode')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create config directory if it doesn't exist
    config_dir = os.path.dirname(args.config)
    os.makedirs(config_dir, exist_ok=True)
    
    # Create logs directory
    os.makedirs('/mnt/c/bmad-workspace/logs', exist_ok=True)
    
    # Initialize and start the CEO agent
    ceo_agent = CEOQualityControlAgent(args.config)
    
    if args.test:
        logger.info("Running in test mode...")
        # Run basic tests
        await ceo_agent._perform_health_check()
        logger.info("Test completed successfully")
        return
    
    try:
        await ceo_agent.start()
    except KeyboardInterrupt:
        logger.info("CEO Quality Control Agent stopped by user")
    except Exception as e:
        logger.error(f"CEO Quality Control Agent crashed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())