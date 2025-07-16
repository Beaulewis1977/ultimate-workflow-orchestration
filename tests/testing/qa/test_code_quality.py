"""
Code quality assurance tests for the autonomous development system.
"""
import pytest
import ast
import re
import tempfile
from pathlib import Path
from typing import List, Dict, Any
import json

class CodeQualityAnalyzer:
    """Analyze code quality metrics and standards."""
    
    def __init__(self):
        self.metrics = {
            "complexity": 0,
            "maintainability": 0,
            "readability": 0,
            "documentation": 0,
            "test_coverage": 0
        }
        self.issues = []
    
    def analyze_complexity(self, code_content):
        """Analyze cyclomatic complexity."""
        try:
            tree = ast.parse(code_content)
            complexity_analyzer = ComplexityVisitor()
            complexity_analyzer.visit(tree)
            return complexity_analyzer.complexity
        except SyntaxError:
            return -1  # Invalid code
    
    def analyze_function_length(self, code_content):
        """Analyze function length."""
        try:
            tree = ast.parse(code_content)
            length_analyzer = FunctionLengthVisitor()
            length_analyzer.visit(tree)
            return length_analyzer.function_lengths
        except SyntaxError:
            return {}
    
    def analyze_naming_conventions(self, code_content):
        """Analyze naming conventions."""
        issues = []
        
        # Check for PEP 8 naming conventions
        patterns = {
            "snake_case_function": r"def\s+([a-z_][a-z0-9_]*)\s*\(",
            "CamelCase_class": r"class\s+([A-Z][a-zA-Z0-9]*)\s*[\(:]",
            "CONSTANT": r"^([A-Z_][A-Z0-9_]*)\s*="
        }
        
        lines = code_content.split('\n')
        for line_num, line in enumerate(lines, 1):
            # Check function names
            func_matches = re.finditer(patterns["snake_case_function"], line)
            for match in func_matches:
                func_name = match.group(1)
                if not re.match(r"^[a-z_][a-z0-9_]*$", func_name):
                    issues.append({
                        "line": line_num,
                        "type": "naming",
                        "message": f"Function '{func_name}' should use snake_case"
                    })
            
            # Check class names
            class_matches = re.finditer(patterns["CamelCase_class"], line)
            for match in class_matches:
                class_name = match.group(1)
                if not re.match(r"^[A-Z][a-zA-Z0-9]*$", class_name):
                    issues.append({
                        "line": line_num,
                        "type": "naming",
                        "message": f"Class '{class_name}' should use CamelCase"
                    })
        
        return issues
    
    def analyze_documentation(self, code_content):
        """Analyze documentation quality."""
        try:
            tree = ast.parse(code_content)
            doc_analyzer = DocumentationVisitor()
            doc_analyzer.visit(tree)
            return doc_analyzer.documentation_stats
        except SyntaxError:
            return {"documented_functions": 0, "total_functions": 0, "coverage": 0}
    
    def analyze_imports(self, code_content):
        """Analyze import organization and quality."""
        issues = []
        lines = code_content.split('\n')
        
        import_section_ended = False
        found_imports_after_code = False
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue
            
            # Check for imports
            if stripped.startswith(('import ', 'from ')):
                if import_section_ended:
                    found_imports_after_code = True
                    issues.append({
                        "line": line_num,
                        "type": "import_order",
                        "message": "Imports should be at the top of the file"
                    })
                
                # Check for relative imports
                if 'from .' in stripped:
                    issues.append({
                        "line": line_num,
                        "type": "relative_import",
                        "message": "Avoid relative imports when possible"
                    })
            else:
                import_section_ended = True
        
        return issues
    
    def analyze_code_duplication(self, code_content):
        """Analyze code duplication."""
        lines = code_content.split('\n')
        line_counts = {}
        duplicates = []
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                if stripped in line_counts:
                    line_counts[stripped].append(line_num)
                else:
                    line_counts[stripped] = [line_num]
        
        for line_content, line_numbers in line_counts.items():
            if len(line_numbers) > 2 and len(line_content) > 20:  # Ignore short lines
                duplicates.append({
                    "content": line_content,
                    "occurrences": len(line_numbers),
                    "lines": line_numbers
                })
        
        return duplicates

class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor to calculate cyclomatic complexity."""
    
    def __init__(self):
        self.complexity = 1  # Base complexity
    
    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

class FunctionLengthVisitor(ast.NodeVisitor):
    """AST visitor to analyze function lengths."""
    
    def __init__(self):
        self.function_lengths = {}
    
    def visit_FunctionDef(self, node):
        # Calculate function length
        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
            length = node.end_lineno - node.lineno + 1
        else:
            # Fallback for older Python versions
            length = len(ast.dump(node).split('\n'))
        
        self.function_lengths[node.name] = length
        self.generic_visit(node)

class DocumentationVisitor(ast.NodeVisitor):
    """AST visitor to analyze documentation coverage."""
    
    def __init__(self):
        self.documentation_stats = {
            "documented_functions": 0,
            "total_functions": 0,
            "documented_classes": 0,
            "total_classes": 0
        }
    
    def visit_FunctionDef(self, node):
        self.documentation_stats["total_functions"] += 1
        
        # Check for docstring
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Str)):
            self.documentation_stats["documented_functions"] += 1
        
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.documentation_stats["total_classes"] += 1
        
        # Check for docstring
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Str)):
            self.documentation_stats["documented_classes"] += 1
        
        self.generic_visit(node)

@pytest.mark.qa
class TestCodeQuality:
    """Code quality assurance test suite."""
    
    @pytest.fixture
    def quality_analyzer(self):
        """Create code quality analyzer."""
        return CodeQualityAnalyzer()
    
    def test_complexity_analysis_low(self, quality_analyzer):
        """Test complexity analysis for low complexity code."""
        simple_code = """
def simple_function(x):
    \"\"\"Simple function with low complexity.\"\"\"
    return x * 2

def another_simple(a, b):
    \"\"\"Another simple function.\"\"\"
    result = a + b
    return result
"""
        
        complexity = quality_analyzer.analyze_complexity(simple_code)
        assert complexity <= 3  # Should be low complexity
    
    def test_complexity_analysis_high(self, quality_analyzer):
        """Test complexity analysis for high complexity code."""
        complex_code = """
def complex_function(x, y, z):
    \"\"\"Complex function with many branches.\"\"\"
    if x > 0:
        if y > 0:
            if z > 0:
                for i in range(x):
                    while y > 0:
                        try:
                            if i % 2 == 0:
                                result = x + y + z
                            else:
                                result = x - y - z
                        except ValueError:
                            result = 0
                        y -= 1
                return result
            else:
                return x + y
        else:
            return x
    else:
        return 0
"""
        
        complexity = quality_analyzer.analyze_complexity(complex_code)
        assert complexity > 10  # Should be high complexity
    
    def test_function_length_analysis(self, quality_analyzer):
        """Test function length analysis."""
        code_with_long_function = """
def short_function():
    return "short"

def long_function():
    # This function is intentionally long
    line1 = "line 1"
    line2 = "line 2"
    line3 = "line 3"
    line4 = "line 4"
    line5 = "line 5"
    line6 = "line 6"
    line7 = "line 7"
    line8 = "line 8"
    line9 = "line 9"
    line10 = "line 10"
    return line1 + line2 + line3 + line4 + line5
"""
        
        function_lengths = quality_analyzer.analyze_function_length(code_with_long_function)
        
        assert "short_function" in function_lengths
        assert "long_function" in function_lengths
        assert function_lengths["long_function"] > function_lengths["short_function"]
    
    def test_naming_convention_violations(self, quality_analyzer):
        """Test detection of naming convention violations."""
        bad_naming_code = """
def BadFunctionName():  # Should be snake_case
    pass

class bad_class_name:  # Should be CamelCase
    pass

def good_function_name():
    pass

class GoodClassName:
    pass
"""
        
        naming_issues = quality_analyzer.analyze_naming_conventions(bad_naming_code)
        
        # Should detect naming violations
        assert len(naming_issues) >= 2
        
        # Check specific violations
        bad_function = any("BadFunctionName" in issue["message"] for issue in naming_issues)
        bad_class = any("bad_class_name" in issue["message"] for issue in naming_issues)
        
        assert bad_function
        assert bad_class
    
    def test_documentation_analysis(self, quality_analyzer):
        """Test documentation coverage analysis."""
        documented_code = """
def documented_function():
    \"\"\"This function has documentation.\"\"\"
    return True

def undocumented_function():
    return False

class DocumentedClass:
    \"\"\"This class has documentation.\"\"\"
    pass

class UndocumentedClass:
    pass
"""
        
        doc_stats = quality_analyzer.analyze_documentation(documented_code)
        
        assert doc_stats["total_functions"] == 2
        assert doc_stats["documented_functions"] == 1
        assert doc_stats["total_classes"] == 2
        assert doc_stats["documented_classes"] == 1
    
    def test_import_organization(self, quality_analyzer):
        """Test import organization analysis."""
        bad_import_code = """
import os
import sys

def some_function():
    pass

import json  # Import after code - bad
from .relative import something  # Relative import
"""
        
        import_issues = quality_analyzer.analyze_imports(bad_import_code)
        
        # Should detect import issues
        assert len(import_issues) >= 2
        
        # Check specific issues
        late_import = any("top of the file" in issue["message"] for issue in import_issues)
        relative_import = any("relative import" in issue["message"] for issue in import_issues)
        
        assert late_import
        assert relative_import
    
    def test_code_duplication_detection(self, quality_analyzer):
        """Test code duplication detection."""
        duplicate_code = """
def function_one():
    result = some_complex_calculation_that_is_duplicated()
    return result

def function_two():
    result = some_complex_calculation_that_is_duplicated()
    return result

def function_three():
    result = some_complex_calculation_that_is_duplicated()
    return result
"""
        
        duplicates = quality_analyzer.analyze_code_duplication(duplicate_code)
        
        # Should detect duplicated lines
        assert len(duplicates) >= 1
        
        # Check that the duplicated line appears multiple times
        duplicate_found = any(
            dup["occurrences"] >= 3 and "some_complex_calculation" in dup["content"]
            for dup in duplicates
        )
        assert duplicate_found
    
    def test_comprehensive_quality_analysis(self, quality_analyzer, temp_workspace):
        """Test comprehensive code quality analysis."""
        # Create code file with various quality issues
        quality_test_file = temp_workspace / "quality_test.py"
        quality_test_file.write_text("""
import os
import sys

def BadFunctionName():  # Naming violation
    # High complexity function
    x = input("Enter number: ")
    if x > 0:
        if x < 100:
            if x % 2 == 0:
                for i in range(x):
                    while i > 0:
                        try:
                            result = complex_operation()
                            return result
                        except Exception:
                            i -= 1
            else:
                return x
        else:
            return 100
    else:
        return 0

import json  # Late import

def undocumented_function():  # No docstring
    result = complex_operation()  # Duplicated line
    return result

def another_function():
    result = complex_operation()  # Duplicated line
    return result

class bad_class_name:  # Naming violation
    pass
""")
        
        with open(quality_test_file) as f:
            code_content = f.read()
        
        # Run all quality analyses
        complexity = quality_analyzer.analyze_complexity(code_content)
        function_lengths = quality_analyzer.analyze_function_length(code_content)
        naming_issues = quality_analyzer.analyze_naming_conventions(code_content)
        doc_stats = quality_analyzer.analyze_documentation(code_content)
        import_issues = quality_analyzer.analyze_imports(code_content)
        duplicates = quality_analyzer.analyze_code_duplication(code_content)
        
        # Verify issues were detected
        assert complexity > 5  # High complexity
        assert len(naming_issues) >= 2  # Naming violations
        assert doc_stats["documented_functions"] == 0  # No documentation
        assert len(import_issues) >= 1  # Import issues
        assert len(duplicates) >= 1  # Code duplication
        
        # Calculate overall quality score
        quality_score = 100
        quality_score -= min(complexity * 2, 30)  # Complexity penalty
        quality_score -= len(naming_issues) * 5  # Naming penalty
        quality_score -= len(import_issues) * 3  # Import penalty
        quality_score -= len(duplicates) * 10  # Duplication penalty
        
        # Poor quality code should have low score
        assert quality_score < 70
    
    def test_high_quality_code_analysis(self, quality_analyzer):
        """Test analysis of high-quality code."""
        high_quality_code = """
\"\"\"
High-quality module with proper structure and documentation.
\"\"\"
import json
import os
import sys


class HighQualityClass:
    \"\"\"A well-documented class with clear purpose.\"\"\"
    
    def __init__(self, name: str):
        \"\"\"Initialize with a name.\"\"\"
        self.name = name
    
    def get_name(self) -> str:
        \"\"\"Return the name.\"\"\"
        return self.name


def well_documented_function(data: dict) -> dict:
    \"\"\"
    Process data with clear documentation.
    
    Args:
        data: Input data dictionary
        
    Returns:
        Processed data dictionary
    \"\"\"
    if not data:
        return {}
    
    processed = {}
    for key, value in data.items():
        processed[key] = str(value).upper()
    
    return processed


def simple_utility_function(x: int, y: int) -> int:
    \"\"\"Add two numbers together.\"\"\"
    return x + y
"""
        
        # Run quality analyses
        complexity = quality_analyzer.analyze_complexity(high_quality_code)
        naming_issues = quality_analyzer.analyze_naming_conventions(high_quality_code)
        doc_stats = quality_analyzer.analyze_documentation(high_quality_code)
        import_issues = quality_analyzer.analyze_imports(high_quality_code)
        duplicates = quality_analyzer.analyze_code_duplication(high_quality_code)
        
        # High-quality code should have good metrics
        assert complexity <= 5  # Low complexity
        assert len(naming_issues) == 0  # No naming violations
        assert doc_stats["documented_functions"] == doc_stats["total_functions"]  # All documented
        assert len(import_issues) == 0  # No import issues
        assert len(duplicates) == 0  # No duplication
        
        # Calculate quality score
        quality_score = 100
        quality_score -= complexity  # Minimal complexity penalty
        
        # High-quality code should have high score
        assert quality_score >= 95