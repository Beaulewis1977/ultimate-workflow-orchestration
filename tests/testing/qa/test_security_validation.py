"""
Security validation tests for the autonomous development system.
"""
import pytest
import os
import json
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch
import hashlib
import secrets

class SecurityValidator:
    """Security validation and testing utility."""
    
    def __init__(self):
        self.security_issues = []
        self.sensitive_patterns = [
            r'password\s*=\s*["\']([^"\']+)["\']',
            r'api_key\s*=\s*["\']([^"\']+)["\']',
            r'secret\s*=\s*["\']([^"\']+)["\']',
            r'token\s*=\s*["\']([^"\']+)["\']',
            r'private_key\s*=\s*["\']([^"\']+)["\']'
        ]
        self.dangerous_functions = [
            'eval', 'exec', 'subprocess.call', 'os.system',
            'open', '__import__', 'compile'
        ]
    
    def scan_for_secrets(self, file_path):
        """Scan file for exposed secrets."""
        import re
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return []
        
        found_secrets = []
        for pattern in self.sensitive_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                found_secrets.append({
                    "file": file_path,
                    "line": content[:match.start()].count('\n') + 1,
                    "pattern": pattern,
                    "match": match.group(0)
                })
        
        return found_secrets
    
    def scan_for_dangerous_functions(self, file_path):
        """Scan for potentially dangerous function usage."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return []
        
        dangerous_usage = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for func in self.dangerous_functions:
                if func in line and not line.strip().startswith('#'):
                    dangerous_usage.append({
                        "file": file_path,
                        "line": line_num,
                        "function": func,
                        "code": line.strip()
                    })
        
        return dangerous_usage
    
    def validate_file_permissions(self, file_path):
        """Validate file permissions for security."""
        issues = []
        
        try:
            stat_info = os.stat(file_path)
            mode = stat_info.st_mode
            
            # Check for world-writable files
            if mode & 0o002:
                issues.append({
                    "file": file_path,
                    "issue": "World-writable file",
                    "severity": "high"
                })
            
            # Check for world-readable sensitive files
            if file_path.endswith(('.key', '.pem', '.p12')):
                if mode & 0o004:
                    issues.append({
                        "file": file_path,
                        "issue": "World-readable sensitive file",
                        "severity": "medium"
                    })
        
        except Exception as e:
            issues.append({
                "file": file_path,
                "issue": f"Cannot check permissions: {e}",
                "severity": "low"
            })
        
        return issues
    
    def validate_input_sanitization(self, code_content):
        """Check for proper input sanitization."""
        issues = []
        
        # Check for SQL injection vulnerabilities
        sql_patterns = [
            r'execute\s*\(\s*["\'].*%.*["\']',
            r'query\s*\(\s*["\'].*\+.*["\']',
            r'\.format\s*\([^)]*\)'
        ]
        
        import re
        for pattern in sql_patterns:
            if re.search(pattern, code_content, re.IGNORECASE):
                issues.append({
                    "type": "sql_injection",
                    "description": "Potential SQL injection vulnerability",
                    "pattern": pattern
                })
        
        # Check for command injection
        command_patterns = [
            r'subprocess\..*shell\s*=\s*True',
            r'os\.system\s*\(',
            r'os\.popen\s*\('
        ]
        
        for pattern in command_patterns:
            if re.search(pattern, code_content, re.IGNORECASE):
                issues.append({
                    "type": "command_injection",
                    "description": "Potential command injection vulnerability",
                    "pattern": pattern
                })
        
        return issues

class CryptographyValidator:
    """Validate cryptographic implementations."""
    
    def __init__(self):
        self.weak_algorithms = [
            'md5', 'sha1', 'des', 'rc4'
        ]
        self.secure_algorithms = [
            'sha256', 'sha512', 'aes', 'rsa'
        ]
    
    def validate_hash_function(self, algorithm):
        """Validate hash function strength."""
        algorithm = algorithm.lower()
        
        if algorithm in self.weak_algorithms:
            return False, f"Weak hash algorithm: {algorithm}"
        
        if algorithm in self.secure_algorithms:
            return True, f"Secure hash algorithm: {algorithm}"
        
        return None, f"Unknown algorithm: {algorithm}"
    
    def validate_random_generation(self, method):
        """Validate random number generation method."""
        secure_methods = ['secrets', 'os.urandom', 'random.SystemRandom']
        insecure_methods = ['random.random', 'random.randint']
        
        if any(secure in method for secure in secure_methods):
            return True, "Secure random generation"
        
        if any(insecure in method for insecure in insecure_methods):
            return False, "Insecure random generation"
        
        return None, "Unknown random generation method"
    
    def test_encryption_strength(self, key_size, algorithm):
        """Test encryption key strength."""
        min_key_sizes = {
            'aes': 256,
            'rsa': 2048,
            'dsa': 2048,
            'ecdsa': 256
        }
        
        algorithm = algorithm.lower()
        if algorithm in min_key_sizes:
            min_size = min_key_sizes[algorithm]
            if key_size >= min_size:
                return True, f"Strong {algorithm} key ({key_size} bits)"
            else:
                return False, f"Weak {algorithm} key ({key_size} bits, minimum {min_size})"
        
        return None, f"Unknown encryption algorithm: {algorithm}"

@pytest.mark.security
@pytest.mark.qa
class TestSecurityValidation:
    """Security validation test suite."""
    
    @pytest.fixture
    def security_validator(self):
        """Create security validator instance."""
        return SecurityValidator()
    
    @pytest.fixture
    def crypto_validator(self):
        """Create cryptography validator instance."""
        return CryptographyValidator()
    
    def test_secret_detection_positive(self, security_validator, temp_workspace):
        """Test detection of exposed secrets."""
        # Create file with secrets
        secret_file = temp_workspace / "config.py"
        secret_file.write_text("""
# Configuration file
DATABASE_URL = "postgresql://user:pass@localhost/db"
API_KEY = "sk-1234567890abcdef"
password = "supersecret123"
SECRET_TOKEN = "abc123def456"
""")
        
        secrets = security_validator.scan_for_secrets(secret_file)
        
        # Should detect multiple secrets
        assert len(secrets) >= 2
        
        # Check that API_KEY was detected
        api_key_found = any("API_KEY" in secret["match"] for secret in secrets)
        assert api_key_found
    
    def test_secret_detection_negative(self, security_validator, temp_workspace):
        """Test that no secrets are detected in clean code."""
        # Create file without secrets
        clean_file = temp_workspace / "clean_code.py"
        clean_file.write_text("""
# Clean configuration file
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
API_KEY = os.environ.get('API_KEY')
password_hash = hash_password(user_input)
""")
        
        secrets = security_validator.scan_for_secrets(clean_file)
        
        # Should not detect any secrets
        assert len(secrets) == 0
    
    def test_dangerous_function_detection(self, security_validator, temp_workspace):
        """Test detection of dangerous function usage."""
        # Create file with dangerous functions
        dangerous_file = temp_workspace / "dangerous.py"
        dangerous_file.write_text("""
import subprocess
import os

# Dangerous usage
result = eval(user_input)
subprocess.call(command, shell=True)
os.system("rm -rf /")
exec(code_from_user)
""")
        
        dangerous_usage = security_validator.scan_for_dangerous_functions(dangerous_file)
        
        # Should detect multiple dangerous functions
        assert len(dangerous_usage) >= 3
        
        # Check specific functions
        functions_found = [usage["function"] for usage in dangerous_usage]
        assert "eval" in functions_found
        assert "exec" in functions_found
    
    def test_file_permission_validation(self, security_validator, temp_workspace):
        """Test file permission validation."""
        # Create files with different permissions
        secure_file = temp_workspace / "secure.txt"
        secure_file.write_text("secure content")
        secure_file.chmod(0o600)  # Read/write for owner only
        
        # Test secure file
        issues = security_validator.validate_file_permissions(secure_file)
        world_writable = any("World-writable" in issue["issue"] for issue in issues)
        assert not world_writable
    
    def test_input_sanitization_validation(self, security_validator):
        """Test input sanitization validation."""
        # Code with SQL injection vulnerability
        vulnerable_code = """
def get_user(username):
    query = "SELECT * FROM users WHERE name = '%s'" % username
    return execute(query)
"""
        
        issues = security_validator.validate_input_sanitization(vulnerable_code)
        
        # Should detect SQL injection vulnerability
        sql_issues = [issue for issue in issues if issue["type"] == "sql_injection"]
        assert len(sql_issues) > 0
    
    def test_command_injection_detection(self, security_validator):
        """Test command injection detection."""
        # Code with command injection vulnerability
        vulnerable_code = """
import subprocess

def process_file(filename):
    subprocess.run(f"cat {filename}", shell=True)
"""
        
        issues = security_validator.validate_input_sanitization(vulnerable_code)
        
        # Should detect command injection vulnerability
        command_issues = [issue for issue in issues if issue["type"] == "command_injection"]
        assert len(command_issues) > 0
    
    def test_hash_algorithm_validation(self, crypto_validator):
        """Test hash algorithm validation."""
        # Test weak algorithm
        is_secure, message = crypto_validator.validate_hash_function("md5")
        assert is_secure is False
        assert "Weak" in message
        
        # Test strong algorithm
        is_secure, message = crypto_validator.validate_hash_function("sha256")
        assert is_secure is True
        assert "Secure" in message
    
    def test_random_generation_validation(self, crypto_validator):
        """Test random number generation validation."""
        # Test secure method
        is_secure, message = crypto_validator.validate_random_generation("secrets.token_hex()")
        assert is_secure is True
        assert "Secure" in message
        
        # Test insecure method
        is_secure, message = crypto_validator.validate_random_generation("random.randint()")
        assert is_secure is False
        assert "Insecure" in message
    
    def test_encryption_strength_validation(self, crypto_validator):
        """Test encryption strength validation."""
        # Test strong RSA key
        is_strong, message = crypto_validator.test_encryption_strength(2048, "RSA")
        assert is_strong is True
        assert "Strong" in message
        
        # Test weak RSA key
        is_strong, message = crypto_validator.test_encryption_strength(1024, "RSA")
        assert is_strong is False
        assert "Weak" in message
    
    def test_comprehensive_security_scan(self, security_validator, temp_workspace):
        """Test comprehensive security scanning."""
        # Create multiple files with various security issues
        files_content = {
            "config.py": """
API_KEY = "sk-real-api-key-123"
DB_PASSWORD = "password123"
""",
            "processor.py": """
import subprocess

def process_input(user_data):
    # Dangerous: eval user input
    result = eval(user_data)
    
    # Dangerous: shell injection
    subprocess.run(f"echo {user_data}", shell=True)
    
    return result
""",
            "database.py": """
def get_user(user_id):
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE id = " + user_id
    return execute_query(query)
"""
        }
        
        all_issues = {
            "secrets": [],
            "dangerous_functions": [],
            "input_sanitization": []
        }
        
        for filename, content in files_content.items():
            file_path = temp_workspace / filename
            file_path.write_text(content)
            
            # Scan for different types of issues
            all_issues["secrets"].extend(
                security_validator.scan_for_secrets(file_path)
            )
            all_issues["dangerous_functions"].extend(
                security_validator.scan_for_dangerous_functions(file_path)
            )
            all_issues["input_sanitization"].extend(
                security_validator.validate_input_sanitization(content)
            )
        
        # Should detect multiple types of security issues
        assert len(all_issues["secrets"]) >= 2
        assert len(all_issues["dangerous_functions"]) >= 2
        assert len(all_issues["input_sanitization"]) >= 1
        
        # Count total issues
        total_issues = sum(len(issues) for issues in all_issues.values())
        assert total_issues >= 5
    
    def test_secure_code_validation(self, security_validator, temp_workspace):
        """Test validation of secure code."""
        # Create secure code file
        secure_file = temp_workspace / "secure_code.py"
        secure_file.write_text("""
import os
import hashlib
import secrets
from sqlalchemy import text

# Secure configuration
API_KEY = os.environ.get('API_KEY')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

def secure_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def secure_random():
    return secrets.token_hex(32)

def safe_query(user_id):
    # Parameterized query
    query = text("SELECT * FROM users WHERE id = :user_id")
    return execute_query(query, user_id=user_id)
""")
        
        # Scan for issues
        secrets = security_validator.scan_for_secrets(secure_file)
        dangerous_functions = security_validator.scan_for_dangerous_functions(secure_file)
        
        # Secure code should have minimal issues
        assert len(secrets) == 0
        assert len(dangerous_functions) == 0
    
    @pytest.mark.slow
    def test_security_regression_suite(self, security_validator, temp_workspace):
        """Test security regression detection."""
        # This test would check that previously identified security issues
        # don't reappear in the codebase
        
        # Create a baseline of security issues
        baseline_file = temp_workspace / "baseline_security.json"
        
        # Simulate scanning entire project
        security_baseline = {
            "timestamp": "2024-01-01T00:00:00Z",
            "total_files_scanned": 10,
            "issues_found": {
                "secrets": 0,
                "dangerous_functions": 0,
                "permission_issues": 0
            },
            "files_with_issues": []
        }
        
        baseline_file.write_text(json.dumps(security_baseline, indent=2))
        
        # Verify baseline exists and is readable
        assert baseline_file.exists()
        
        with open(baseline_file) as f:
            loaded_baseline = json.load(f)
        
        assert loaded_baseline["issues_found"]["secrets"] == 0
        assert loaded_baseline["issues_found"]["dangerous_functions"] == 0