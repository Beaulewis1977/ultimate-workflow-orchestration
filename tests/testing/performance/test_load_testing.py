"""
Performance and load testing for the autonomous development system.
"""
import pytest
import asyncio
import time
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import Mock, patch
import json
from pathlib import Path

class PerformanceMonitor:
    """Monitor system performance during tests."""
    
    def __init__(self):
        self.metrics = {
            "cpu_usage": [],
            "memory_usage": [],
            "response_times": [],
            "error_count": 0,
            "success_count": 0
        }
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start performance monitoring."""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self):
        """Monitor system metrics in a loop."""
        while self.monitoring:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.metrics["cpu_usage"].append(cpu_percent)
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.metrics["memory_usage"].append(memory.percent)
            
            time.sleep(1)
    
    def record_response_time(self, response_time):
        """Record a response time."""
        self.metrics["response_times"].append(response_time)
    
    def record_success(self):
        """Record a successful operation."""
        self.metrics["success_count"] += 1
    
    def record_error(self):
        """Record an error."""
        self.metrics["error_count"] += 1
    
    def get_statistics(self):
        """Get performance statistics."""
        response_times = self.metrics["response_times"]
        return {
            "avg_cpu_usage": sum(self.metrics["cpu_usage"]) / len(self.metrics["cpu_usage"]) if self.metrics["cpu_usage"] else 0,
            "max_cpu_usage": max(self.metrics["cpu_usage"]) if self.metrics["cpu_usage"] else 0,
            "avg_memory_usage": sum(self.metrics["memory_usage"]) / len(self.metrics["memory_usage"]) if self.metrics["memory_usage"] else 0,
            "max_memory_usage": max(self.metrics["memory_usage"]) if self.metrics["memory_usage"] else 0,
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "total_requests": len(response_times),
            "success_rate": self.metrics["success_count"] / (self.metrics["success_count"] + self.metrics["error_count"]) if (self.metrics["success_count"] + self.metrics["error_count"]) > 0 else 0,
            "error_rate": self.metrics["error_count"] / (self.metrics["success_count"] + self.metrics["error_count"]) if (self.metrics["success_count"] + self.metrics["error_count"]) > 0 else 0
        }

class MockAutonomousSystem:
    """Mock autonomous system for load testing."""
    
    def __init__(self, latency_ms=100):
        self.latency_ms = latency_ms
        self.active_agents = {}
        self.task_queue = []
        self.processing = False
    
    async def create_agent(self, agent_name, agent_type="generic"):
        """Create a new agent."""
        start_time = time.time()
        
        # Simulate processing time
        await asyncio.sleep(self.latency_ms / 1000)
        
        # Random failure simulation (5% failure rate)
        import random
        if random.random() < 0.05:
            raise Exception(f"Failed to create agent {agent_name}")
        
        self.active_agents[agent_name] = {
            "type": agent_type,
            "created_at": time.time(),
            "tasks_processed": 0
        }
        
        return time.time() - start_time
    
    async def process_task(self, task_data):
        """Process a task."""
        start_time = time.time()
        
        # Simulate task processing
        processing_time = self.latency_ms + (len(str(task_data)) * 2)
        await asyncio.sleep(processing_time / 1000)
        
        # Random failure simulation (3% failure rate)
        import random
        if random.random() < 0.03:
            raise Exception("Task processing failed")
        
        return time.time() - start_time
    
    async def get_system_status(self):
        """Get system status."""
        start_time = time.time()
        
        await asyncio.sleep(50 / 1000)  # 50ms response time
        
        return {
            "active_agents": len(self.active_agents),
            "queue_size": len(self.task_queue),
            "processing": self.processing,
            "uptime": "1h 30m"
        }, time.time() - start_time

@pytest.mark.performance
class TestLoadTesting:
    """Load testing for the autonomous development system."""
    
    @pytest.fixture
    def performance_monitor(self):
        """Create performance monitor."""
        monitor = PerformanceMonitor()
        monitor.start_monitoring()
        yield monitor
        monitor.stop_monitoring()
    
    @pytest.fixture
    def mock_system(self):
        """Create mock autonomous system."""
        return MockAutonomousSystem(latency_ms=100)
    
    @pytest.mark.asyncio
    async def test_concurrent_agent_creation(self, mock_system, performance_monitor):
        """Test creating multiple agents concurrently."""
        num_agents = 50
        
        async def create_agent_task(agent_id):
            try:
                response_time = await mock_system.create_agent(f"agent_{agent_id}")
                performance_monitor.record_response_time(response_time)
                performance_monitor.record_success()
            except Exception:
                performance_monitor.record_error()
        
        # Create agents concurrently
        tasks = [create_agent_task(i) for i in range(num_agents)]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Analyze performance
        stats = performance_monitor.get_statistics()
        
        # Performance assertions
        assert stats["avg_response_time"] < 1.0  # Average response time < 1 second
        assert stats["max_response_time"] < 2.0  # Max response time < 2 seconds
        assert stats["success_rate"] > 0.90  # Success rate > 90%
        assert stats["avg_cpu_usage"] < 80  # CPU usage < 80%
        assert stats["avg_memory_usage"] < 85  # Memory usage < 85%
    
    @pytest.mark.asyncio
    async def test_high_frequency_task_processing(self, mock_system, performance_monitor):
        """Test processing tasks at high frequency."""
        num_tasks = 100
        
        async def process_task_batch(batch_size=10):
            tasks = []
            for i in range(batch_size):
                task_data = {"id": i, "operation": "test", "data": "x" * 100}
                tasks.append(mock_system.process_task(task_data))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    performance_monitor.record_error()
                else:
                    performance_monitor.record_response_time(result)
                    performance_monitor.record_success()
        
        # Process tasks in batches
        batch_tasks = []
        for i in range(0, num_tasks, 10):
            batch_tasks.append(process_task_batch())
        
        await asyncio.gather(*batch_tasks)
        
        # Analyze performance
        stats = performance_monitor.get_statistics()
        
        # Performance assertions
        assert stats["total_requests"] >= num_tasks * 0.95  # At least 95% of tasks processed
        assert stats["avg_response_time"] < 0.5  # Average response time < 500ms
        assert stats["success_rate"] > 0.95  # Success rate > 95%
    
    @pytest.mark.asyncio
    async def test_system_status_load(self, mock_system, performance_monitor):
        """Test system status requests under load."""
        num_requests = 200
        
        async def status_request():
            try:
                status, response_time = await mock_system.get_system_status()
                performance_monitor.record_response_time(response_time)
                performance_monitor.record_success()
                return status
            except Exception:
                performance_monitor.record_error()
                return None
        
        # Make concurrent status requests
        tasks = [status_request() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
        
        # Count successful responses
        successful_responses = sum(1 for r in results if r is not None)
        
        # Analyze performance
        stats = performance_monitor.get_statistics()
        
        # Performance assertions
        assert successful_responses >= num_requests * 0.98  # 98% success rate
        assert stats["avg_response_time"] < 0.1  # Average response time < 100ms
        assert stats["max_response_time"] < 0.5  # Max response time < 500ms
    
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_memory_leak_detection(self, mock_system, performance_monitor):
        """Test for memory leaks during extended operation."""
        initial_memory = psutil.Process().memory_info().rss
        
        # Run operations for extended period
        for cycle in range(20):
            # Create and destroy agents
            agent_tasks = [mock_system.create_agent(f"temp_agent_{i}") for i in range(10)]
            await asyncio.gather(*agent_tasks, return_exceptions=True)
            
            # Process tasks
            task_tasks = [mock_system.process_task({"cycle": cycle, "task": i}) for i in range(20)]
            await asyncio.gather(*task_tasks, return_exceptions=True)
            
            # Clear agents
            mock_system.active_agents.clear()
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Check memory growth
            current_memory = psutil.Process().memory_info().rss
            memory_growth = (current_memory - initial_memory) / 1024 / 1024  # MB
            
            # Memory growth should be reasonable
            if cycle > 5:  # Allow initial stabilization
                assert memory_growth < 50, f"Memory growth too high: {memory_growth}MB after {cycle} cycles"
    
    @pytest.mark.benchmark
    def test_response_time_benchmark(self, benchmark, mock_system):
        """Benchmark response times."""
        
        async def benchmark_operation():
            return await mock_system.get_system_status()
        
        def sync_benchmark():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(benchmark_operation())
            finally:
                loop.close()
        
        # Run benchmark
        result = benchmark(sync_benchmark)
        
        # The benchmark will automatically collect timing statistics
        # We can add assertions here if needed
        assert result is not None