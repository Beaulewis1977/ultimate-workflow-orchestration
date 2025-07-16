"""
Unit tests for the Claude configuration detector.
"""
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import os

class MockClaudeConfigDetector:
    """Mock Claude configuration detector for testing."""
    
    def __init__(self):
        self.config_paths = [
            "~/.claude/config.json",
            "~/.config/claude/config.json",
            "./claude.json"
        ]
        self.detected_config = None
    
    def detect_config(self):
        """Detect Claude configuration."""
        for path in self.config_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                try:
                    with open(expanded_path, 'r') as f:
                        config = json.load(f)
                    self.detected_config = config
                    return config
                except (json.JSONDecodeError, IOError):
                    continue
        return None
    
    def validate_config(self, config):
        """Validate Claude configuration."""
        required_fields = ["model", "api_key", "max_tokens"]
        if not isinstance(config, dict):
            return False, "Configuration must be a dictionary"
        
        for field in required_fields:
            if field not in config:
                return False, f"Missing required field: {field}"
        
        return True, "Configuration valid"
    
    def get_model_info(self, config):
        """Get model information from configuration."""
        if not config:
            return None
        
        return {
            "model": config.get("model"),
            "max_tokens": config.get("max_tokens", 4096),
            "temperature": config.get("temperature", 0.7),
            "provider": config.get("provider", "anthropic")
        }

@pytest.mark.unit
class TestClaudeConfigDetector:
    """Test suite for Claude configuration detection."""
    
    def test_config_detection_success(self, temp_workspace):
        """Test successful configuration detection."""
        detector = MockClaudeConfigDetector()
        
        # Create a test config file
        config_data = {
            "model": "claude-3-5-sonnet-20241022",
            "api_key": "test_key",
            "max_tokens": 4096
        }
        
        config_file = temp_workspace / "claude.json"
        config_file.write_text(json.dumps(config_data))
        
        # Mock the config paths to include our test file
        detector.config_paths = [str(config_file)]
        
        config = detector.detect_config()
        assert config is not None
        assert config["model"] == "claude-3-5-sonnet-20241022"
        assert config["api_key"] == "test_key"
    
    def test_config_detection_failure(self):
        """Test configuration detection when no config exists."""
        detector = MockClaudeConfigDetector()
        detector.config_paths = ["/nonexistent/path.json"]
        
        config = detector.detect_config()
        assert config is None
    
    def test_config_validation_success(self):
        """Test successful configuration validation."""
        detector = MockClaudeConfigDetector()
        
        valid_config = {
            "model": "claude-3-5-sonnet-20241022",
            "api_key": "test_key",
            "max_tokens": 4096
        }
        
        is_valid, message = detector.validate_config(valid_config)
        assert is_valid is True
        assert message == "Configuration valid"
    
    def test_config_validation_missing_fields(self):
        """Test configuration validation with missing fields."""
        detector = MockClaudeConfigDetector()
        
        invalid_config = {
            "model": "claude-3-5-sonnet-20241022"
            # Missing api_key and max_tokens
        }
        
        is_valid, message = detector.validate_config(invalid_config)
        assert is_valid is False
        assert "Missing required field" in message
    
    def test_config_validation_invalid_type(self):
        """Test configuration validation with invalid type."""
        detector = MockClaudeConfigDetector()
        
        is_valid, message = detector.validate_config("not a dict")
        assert is_valid is False
        assert "Configuration must be a dictionary" in message
    
    def test_model_info_extraction(self):
        """Test model information extraction."""
        detector = MockClaudeConfigDetector()
        
        config = {
            "model": "claude-3-5-sonnet-20241022",
            "api_key": "test_key",
            "max_tokens": 8192,
            "temperature": 0.5,
            "provider": "anthropic"
        }
        
        model_info = detector.get_model_info(config)
        assert model_info["model"] == "claude-3-5-sonnet-20241022"
        assert model_info["max_tokens"] == 8192
        assert model_info["temperature"] == 0.5
        assert model_info["provider"] == "anthropic"
    
    def test_model_info_with_defaults(self):
        """Test model information extraction with default values."""
        detector = MockClaudeConfigDetector()
        
        config = {
            "model": "claude-3-5-sonnet-20241022",
            "api_key": "test_key"
        }
        
        model_info = detector.get_model_info(config)
        assert model_info["model"] == "claude-3-5-sonnet-20241022"
        assert model_info["max_tokens"] == 4096  # Default
        assert model_info["temperature"] == 0.7  # Default
        assert model_info["provider"] == "anthropic"  # Default
    
    def test_model_info_none_config(self):
        """Test model information extraction with None config."""
        detector = MockClaudeConfigDetector()
        
        model_info = detector.get_model_info(None)
        assert model_info is None