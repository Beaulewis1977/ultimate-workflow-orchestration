"""
Memory management validation tests for the autonomous development system.
"""
import pytest
import gc
import sys
import psutil
import time
import threading
from unittest.mock import Mock, patch
import weakref
from typing import List, Dict, Any

class MemoryTracker:
    """Track memory usage and detect leaks."""
    
    def __init__(self):
        self.baseline_memory = 0
        self.current_memory = 0
        self.peak_memory = 0
        self.memory_samples = []
        self.object_counts = {}
        self.weak_refs = []
    
    def start_tracking(self):
        """Start memory tracking."""
        gc.collect()  # Clean up before starting
        process = psutil.Process()
        self.baseline_memory = process.memory_info().rss
        self.current_memory = self.baseline_memory
        self.peak_memory = self.baseline_memory
        self.memory_samples = [self.baseline_memory]
    
    def sample_memory(self):
        """Take a memory sample."""
        gc.collect()
        process = psutil.Process()
        memory = process.memory_info().rss
        self.current_memory = memory
        self.peak_memory = max(self.peak_memory, memory)
        self.memory_samples.append(memory)
        return memory
    
    def get_memory_growth(self):
        """Get memory growth since baseline."""
        return self.current_memory - self.baseline_memory
    
    def get_memory_growth_mb(self):
        """Get memory growth in MB."""
        return self.get_memory_growth() / 1024 / 1024
    
    def track_object(self, obj, name=None):
        """Track an object for lifecycle monitoring."""
        obj_type = type(obj).__name__
        if obj_type not in self.object_counts:
            self.object_counts[obj_type] = 0
        self.object_counts[obj_type] += 1
        
        # Create weak reference to detect when object is deleted
        def cleanup_callback(ref):
            self.object_counts[obj_type] -= 1
        
        weak_ref = weakref.ref(obj, cleanup_callback)
        self.weak_refs.append(weak_ref)
        return weak_ref
    
    def get_object_counts(self):
        """Get current object counts."""
        return self.object_counts.copy()
    
    def check_for_leaks(self, threshold_mb=10):
        """Check for memory leaks."""
        growth_mb = self.get_memory_growth_mb()
        
        # Check for significant memory growth
        if growth_mb > threshold_mb:
            return True, f"Memory growth of {growth_mb:.2f}MB exceeds threshold"
        
        # Check for objects that should have been cleaned up
        leaked_objects = []
        for obj_type, count in self.object_counts.items():
            if count > 0:
                leaked_objects.append(f"{obj_type}: {count}")
        
        if leaked_objects:
            return True, f"Potential object leaks: {', '.join(leaked_objects)}"
        
        return False, "No memory leaks detected"

class MockMemoryIntensiveSystem:
    """Mock system that can simulate memory usage patterns."""
    
    def __init__(self):
        self.data_cache = {}
        self.active_sessions = {}
        self.large_objects = []
    
    def create_large_object(self, size_mb=1):
        """Create a large object to simulate memory usage."""
        size_bytes = int(size_mb * 1024 * 1024)
        large_data = bytearray(size_bytes)
        obj_id = id(large_data)
        self.large_objects.append((obj_id, large_data))
        return obj_id
    
    def cache_data(self, key, data_size_kb=100):
        """Cache data to simulate memory accumulation."""
        data = bytearray(data_size_kb * 1024)
        self.data_cache[key] = data
        return key
    
    def create_session(self, session_id, data_size_kb=50):
        """Create a session with associated data."""
        session_data = {
            "id": session_id,
            "data": bytearray(data_size_kb * 1024),
            "created_at": time.time()
        }
        self.active_sessions[session_id] = session_data
        return session_id
    
    def cleanup_cache(self):
        """Clean up cache."""
        self.data_cache.clear()
    
    def cleanup_sessions(self):
        """Clean up sessions."""
        self.active_sessions.clear()
    
    def cleanup_large_objects(self):
        """Clean up large objects."""
        self.large_objects.clear()
    
    def full_cleanup(self):
        """Perform full cleanup."""
        self.cleanup_cache()
        self.cleanup_sessions()
        self.cleanup_large_objects()
        gc.collect()

@pytest.mark.validation
@pytest.mark.memory
class TestMemoryManagement:
    """Test suite for memory management validation."""
    
    @pytest.fixture
    def memory_tracker(self):
        """Create memory tracker."""
        tracker = MemoryTracker()
        tracker.start_tracking()
        yield tracker
        # Cleanup after test
        gc.collect()
    
    @pytest.fixture
    def mock_system(self):
        """Create mock memory-intensive system."""
        system = MockMemoryIntensiveSystem()
        yield system
        system.full_cleanup()
    
    def test_baseline_memory_measurement(self, memory_tracker):
        """Test baseline memory measurement."""
        # Memory tracker should have a baseline
        assert memory_tracker.baseline_memory > 0
        assert memory_tracker.current_memory == memory_tracker.baseline_memory
        assert memory_tracker.get_memory_growth() == 0
    
    def test_memory_growth_detection(self, memory_tracker, mock_system):
        """Test detection of memory growth."""
        initial_memory = memory_tracker.sample_memory()
        
        # Create some large objects
        for i in range(5):
            mock_system.create_large_object(size_mb=2)
        
        # Sample memory after allocation
        final_memory = memory_tracker.sample_memory()
        
        # Should detect memory growth
        growth_mb = memory_tracker.get_memory_growth_mb()
        assert growth_mb > 5  # Should have grown by at least 5MB
        assert final_memory > initial_memory
    
    def test_object_lifecycle_tracking(self, memory_tracker):
        """Test object lifecycle tracking."""
        # Create objects and track them
        objects = []
        for i in range(10):
            obj = {"data": "x" * 1000, "id": i}
            memory_tracker.track_object(obj, f"test_object_{i}")
            objects.append(obj)
        
        # Check object counts
        counts = memory_tracker.get_object_counts()
        assert counts.get("dict", 0) == 10
        
        # Delete objects
        del objects
        gc.collect()
        
        # Object counts should decrease
        final_counts = memory_tracker.get_object_counts()
        assert final_counts.get("dict", 0) == 0
    
    def test_memory_leak_detection_positive(self, memory_tracker, mock_system):
        """Test memory leak detection when leaks are present."""
        # Create objects without cleanup
        for i in range(20):
            mock_system.create_large_object(size_mb=1)
            mock_system.cache_data(f"leak_key_{i}", data_size_kb=500)
        
        memory_tracker.sample_memory()
        
        # Check for leaks with low threshold
        has_leak, message = memory_tracker.check_for_leaks(threshold_mb=5)
        assert has_leak is True
        assert "exceeds threshold" in message
    
    def test_memory_leak_detection_negative(self, memory_tracker, mock_system):
        """Test memory leak detection when no leaks are present."""
        # Create and immediately clean up objects
        for i in range(10):
            mock_system.create_large_object(size_mb=0.5)
        
        mock_system.full_cleanup()
        memory_tracker.sample_memory()
        
        # Check for leaks
        has_leak, message = memory_tracker.check_for_leaks(threshold_mb=10)
        assert has_leak is False
        assert "No memory leaks detected" in message
    
    def test_cache_memory_management(self, memory_tracker, mock_system):
        """Test cache memory management."""
        initial_memory = memory_tracker.sample_memory()
        
        # Fill cache
        for i in range(100):
            mock_system.cache_data(f"cache_key_{i}", data_size_kb=100)
        
        memory_after_cache = memory_tracker.sample_memory()
        cache_growth = (memory_after_cache - initial_memory) / 1024 / 1024
        
        # Should have significant memory growth
        assert cache_growth > 5  # At least 5MB growth
        
        # Clean cache
        mock_system.cleanup_cache()
        gc.collect()
        
        memory_after_cleanup = memory_tracker.sample_memory()
        cleanup_reduction = (memory_after_cache - memory_after_cleanup) / 1024 / 1024
        
        # Should have significant memory reduction after cleanup
        assert cleanup_reduction > 3  # At least 3MB reduction
    
    def test_session_memory_management(self, memory_tracker, mock_system):
        """Test session memory management."""
        initial_memory = memory_tracker.sample_memory()
        
        # Create many sessions
        session_ids = []
        for i in range(50):
            session_id = f"session_{i}"
            mock_system.create_session(session_id, data_size_kb=200)
            session_ids.append(session_id)
        
        memory_after_sessions = memory_tracker.sample_memory()
        session_growth = (memory_after_sessions - initial_memory) / 1024 / 1024
        
        # Should have memory growth from sessions
        assert session_growth > 8  # At least 8MB growth
        assert len(mock_system.active_sessions) == 50
        
        # Clean sessions
        mock_system.cleanup_sessions()
        gc.collect()
        
        memory_after_cleanup = memory_tracker.sample_memory()
        
        # Sessions should be cleaned up
        assert len(mock_system.active_sessions) == 0
    
    def test_garbage_collection_effectiveness(self, memory_tracker):
        """Test garbage collection effectiveness."""
        initial_memory = memory_tracker.sample_memory()
        
        # Create circular references (potential leak)
        objects = []
        for i in range(100):
            obj1 = {"id": i, "ref": None, "data": "x" * 1000}
            obj2 = {"id": i + 100, "ref": obj1, "data": "y" * 1000}
            obj1["ref"] = obj2
            objects.append((obj1, obj2))
        
        memory_after_creation = memory_tracker.sample_memory()
        
        # Delete references
        del objects
        
        # Force garbage collection
        collected = gc.collect()
        memory_after_gc = memory_tracker.sample_memory()
        
        # GC should have collected some objects
        assert collected > 0
        
        # Memory should have decreased after GC
        gc_reduction = (memory_after_creation - memory_after_gc) / 1024 / 1024
        assert gc_reduction > 0.1  # At least some reduction
    
    def test_memory_fragmentation_handling(self, memory_tracker, mock_system):
        """Test handling of memory fragmentation."""
        # Create and delete objects in a pattern that might cause fragmentation
        for cycle in range(10):
            # Allocate
            objects = []
            for i in range(20):
                obj_id = mock_system.create_large_object(size_mb=0.5)
                objects.append(obj_id)
            
            memory_tracker.sample_memory()
            
            # Deallocate every other object
            mock_system.large_objects = [
                obj for i, obj in enumerate(mock_system.large_objects) 
                if i % 2 == 0
            ]
            
            gc.collect()
        
        # Final cleanup
        mock_system.cleanup_large_objects()
        gc.collect()
        
        final_memory = memory_tracker.sample_memory()
        total_growth = memory_tracker.get_memory_growth_mb()
        
        # Memory growth should be reasonable despite fragmentation
        assert total_growth < 50  # Less than 50MB growth
    
    @pytest.mark.slow
    def test_long_running_memory_stability(self, memory_tracker, mock_system):
        """Test memory stability over extended operation."""
        memory_samples = []
        
        # Simulate long-running operation
        for iteration in range(50):
            # Create some temporary objects
            for i in range(10):
                mock_system.cache_data(f"temp_{iteration}_{i}", data_size_kb=50)
                mock_system.create_session(f"temp_session_{iteration}_{i}")
            
            # Sample memory
            current_memory = memory_tracker.sample_memory()
            memory_samples.append(current_memory)
            
            # Periodic cleanup
            if iteration % 10 == 9:
                mock_system.cleanup_cache()
                mock_system.cleanup_sessions()
                gc.collect()
        
        # Analyze memory trend
        initial_sample = memory_samples[10]  # Skip initial warmup
        final_sample = memory_samples[-1]
        
        # Memory should be relatively stable
        long_term_growth = (final_sample - initial_sample) / 1024 / 1024
        assert long_term_growth < 20  # Less than 20MB growth over time
        
        # Check for consistent cleanup
        has_leak, message = memory_tracker.check_for_leaks(threshold_mb=25)
        if has_leak:
            pytest.fail(f"Long-running memory leak detected: {message}")
    
    def test_concurrent_memory_access(self, memory_tracker, mock_system):
        """Test memory management under concurrent access."""
        import threading
        import queue
        
        results = queue.Queue()
        
        def worker_thread(worker_id):
            try:
                # Each worker creates and cleans up objects
                for i in range(20):
                    key = f"worker_{worker_id}_item_{i}"
                    mock_system.cache_data(key, data_size_kb=100)
                    
                    if i % 5 == 4:  # Periodic cleanup
                        # Clean up some items
                        keys_to_remove = [k for k in mock_system.data_cache.keys() 
                                        if k.startswith(f"worker_{worker_id}")][:3]
                        for k in keys_to_remove:
                            mock_system.data_cache.pop(k, None)
                
                results.put(("success", worker_id))
            except Exception as e:
                results.put(("error", str(e)))
        
        # Start multiple worker threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Check results
        error_count = 0
        while not results.empty():
            result_type, result_data = results.get()
            if result_type == "error":
                error_count += 1
        
        assert error_count == 0, "Concurrent memory access should not cause errors"
        
        # Check final memory state
        final_memory = memory_tracker.sample_memory()
        has_leak, message = memory_tracker.check_for_leaks(threshold_mb=15)
        
        if has_leak:
            pytest.warning(f"Potential memory issue under concurrency: {message}")