"""
Unit tests for tmux utilities.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import subprocess

class MockTmuxUtils:
    """Mock tmux utilities for testing."""
    
    def __init__(self):
        self.sessions = {}
        self.windows = {}
    
    def create_session(self, session_name, detached=True):
        """Create a new tmux session."""
        if session_name in self.sessions:
            return False, f"Session {session_name} already exists"
        
        self.sessions[session_name] = {
            "name": session_name,
            "windows": [],
            "active": True
        }
        return True, f"Session {session_name} created"
    
    def kill_session(self, session_name):
        """Kill a tmux session."""
        if session_name not in self.sessions:
            return False, f"Session {session_name} not found"
        
        del self.sessions[session_name]
        return True, f"Session {session_name} killed"
    
    def list_sessions(self):
        """List all tmux sessions."""
        return list(self.sessions.keys())
    
    def session_exists(self, session_name):
        """Check if a session exists."""
        return session_name in self.sessions
    
    def create_window(self, session_name, window_name, command=None):
        """Create a new window in a session."""
        if session_name not in self.sessions:
            return False, f"Session {session_name} not found"
        
        window_id = f"{session_name}:{window_name}"
        self.windows[window_id] = {
            "session": session_name,
            "name": window_name,
            "command": command,
            "active": True
        }
        
        self.sessions[session_name]["windows"].append(window_name)
        return True, f"Window {window_name} created in session {session_name}"
    
    def send_keys(self, session_name, window_name, keys):
        """Send keys to a tmux window."""
        window_id = f"{session_name}:{window_name}"
        if window_id not in self.windows:
            return False, f"Window {window_name} not found in session {session_name}"
        
        return True, f"Keys sent to {window_id}: {keys}"
    
    def capture_pane(self, session_name, window_name):
        """Capture the content of a tmux pane."""
        window_id = f"{session_name}:{window_name}"
        if window_id not in self.windows:
            return False, f"Window {window_name} not found in session {session_name}"
        
        # Mock captured content
        return True, f"Mock output from {window_id}"

@pytest.mark.unit
class TestTmuxUtils:
    """Test suite for tmux utilities."""
    
    def test_session_creation(self):
        """Test tmux session creation."""
        tmux = MockTmuxUtils()
        
        success, message = tmux.create_session("test_session")
        assert success is True
        assert "test_session" in tmux.sessions
        assert "created" in message
    
    def test_duplicate_session_creation(self):
        """Test creating duplicate session."""
        tmux = MockTmuxUtils()
        tmux.create_session("test_session")
        
        success, message = tmux.create_session("test_session")
        assert success is False
        assert "already exists" in message
    
    def test_session_killing(self):
        """Test tmux session killing."""
        tmux = MockTmuxUtils()
        tmux.create_session("test_session")
        
        success, message = tmux.kill_session("test_session")
        assert success is True
        assert "test_session" not in tmux.sessions
        assert "killed" in message
    
    def test_kill_nonexistent_session(self):
        """Test killing non-existent session."""
        tmux = MockTmuxUtils()
        
        success, message = tmux.kill_session("nonexistent")
        assert success is False
        assert "not found" in message
    
    def test_list_sessions(self):
        """Test listing tmux sessions."""
        tmux = MockTmuxUtils()
        tmux.create_session("session1")
        tmux.create_session("session2")
        
        sessions = tmux.list_sessions()
        assert len(sessions) == 2
        assert "session1" in sessions
        assert "session2" in sessions
    
    def test_session_exists(self):
        """Test checking if session exists."""
        tmux = MockTmuxUtils()
        tmux.create_session("test_session")
        
        assert tmux.session_exists("test_session") is True
        assert tmux.session_exists("nonexistent") is False
    
    def test_window_creation(self):
        """Test tmux window creation."""
        tmux = MockTmuxUtils()
        tmux.create_session("test_session")
        
        success, message = tmux.create_window("test_session", "test_window", "ls -la")
        assert success is True
        assert "test_window" in tmux.sessions["test_session"]["windows"]
        assert "created" in message
    
    def test_window_creation_invalid_session(self):
        """Test window creation in invalid session."""
        tmux = MockTmuxUtils()
        
        success, message = tmux.create_window("nonexistent", "test_window")
        assert success is False
        assert "not found" in message
    
    def test_send_keys(self):
        """Test sending keys to tmux window."""
        tmux = MockTmuxUtils()
        tmux.create_session("test_session")
        tmux.create_window("test_session", "test_window")
        
        success, message = tmux.send_keys("test_session", "test_window", "echo hello")
        assert success is True
        assert "Keys sent" in message
    
    def test_send_keys_invalid_window(self):
        """Test sending keys to invalid window."""
        tmux = MockTmuxUtils()
        tmux.create_session("test_session")
        
        success, message = tmux.send_keys("test_session", "nonexistent", "echo hello")
        assert success is False
        assert "not found" in message
    
    def test_capture_pane(self):
        """Test capturing tmux pane content."""
        tmux = MockTmuxUtils()
        tmux.create_session("test_session")
        tmux.create_window("test_session", "test_window")
        
        success, content = tmux.capture_pane("test_session", "test_window")
        assert success is True
        assert "Mock output" in content
    
    def test_capture_pane_invalid_window(self):
        """Test capturing from invalid window."""
        tmux = MockTmuxUtils()
        tmux.create_session("test_session")
        
        success, message = tmux.capture_pane("test_session", "nonexistent")
        assert success is False
        assert "not found" in message