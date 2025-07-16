"""
Stress testing for the autonomous development system.
"""
import pytest
import asyncio
import time
import psutil
import threading
import random
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock, patch

class StressTestScenario:
    """Stress test scenario runner."""
    
    def __init__(self, name, duration_seconds=60):
        self.name = name
        self.duration_seconds = duration_seconds
        self.start_time = None
        self.end_time = None
        self.metrics = {
            "operations_completed": 0,
            "operations_failed": 0,
            "peak_memory_mb": 0,
            "peak_cpu_percent": 0,
            "average_response_time": 0,
            "errors": []
        }
        self.running = False
    
    def start(self):
        """Start the stress test scenario."""
        self.start_time = time.time()
        self.running = True
        
        # Start resource monitoring
        self.monitor_thread = threading.Thread(target=self._monitor_resources)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop(self):
        """Stop the stress test scenario."""
        self.running = False
        self.end_time = time.time()
    
    def _monitor_resources(self):
        """Monitor system resources."""
        process = psutil.Process()
        
        while self.running:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=0.1)
                self.metrics["peak_cpu_percent"] = max(self.metrics["peak_cpu_percent"], cpu_percent)
                
                # Memory usage
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024
                self.metrics["peak_memory_mb"] = max(self.metrics["peak_memory_mb"], memory_mb)
                
            except Exception as e:
                self.metrics["errors"].append(str(e))
            
            time.sleep(0.5)
    
    def record_operation(self, success=True, response_time=0):
        """Record an operation result."""
        if success:
            self.metrics["operations_completed"] += 1
        else:
            self.metrics["operations_failed"] += 1
        
        # Update average response time
        total_ops = self.metrics["operations_completed"] + self.metrics["operations_failed"]
        if total_ops > 0:
            current_avg = self.metrics["average_response_time"]
            self.metrics["average_response_time"] = ((current_avg * (total_ops - 1)) + response_time) / total_ops
    
    def get_results(self):
        """Get stress test results."""
        duration = (self.end_time or time.time()) - (self.start_time or time.time())
        total_ops = self.metrics["operations_completed"] + self.metrics["operations_failed"]
        
        return {
            "scenario_name": self.name,
            "duration_seconds": duration,
            "total_operations": total_ops,
            "operations_per_second": total_ops / duration if duration > 0 else 0,
            "success_rate": self.metrics["operations_completed"] / total_ops if total_ops > 0 else 0,
            "peak_memory_mb": self.metrics["peak_memory_mb"],
            "peak_cpu_percent": self.metrics["peak_cpu_percent"],
            "average_response_time": self.metrics["average_response_time"],
            "error_count": len(self.metrics["errors"])
        }

class MockStressTestSystem:
    """Mock system for stress testing."""
    
    def __init__(self):
        self.agents = {}
        self.tasks = {}
        self.connections = set()
        self.processing_load = 0
    
    async def create_agent(self, agent_id, config=None):
        """Create an agent with stress simulation."""
        start_time = time.time()
        
        # Simulate variable processing time based on load
        base_time = 0.05  # 50ms base
        load_factor = min(self.processing_load / 100, 2.0)
        processing_time = base_time * (1 + load_factor)
        
        await asyncio.sleep(processing_time)
        
        # Simulate occasional failures under stress
        failure_rate = min(self.processing_load / 1000, 0.1)  # Max 10% failure rate
        if random.random() < failure_rate:
            raise Exception(f"Agent creation failed under stress: {agent_id}")
        
        self.agents[agent_id] = {
            "config": config or {},
            "created_at": time.time(),
            "status": "active"
        }
        
        self.processing_load += 1
        return time.time() - start_time
    
    async def process_task(self, task_id, task_data):
        """Process a task with stress simulation."""
        start_time = time.time()
        
        # Variable processing time based on data size and system load
        data_size = len(str(task_data))
        base_time = 0.02 + (data_size / 10000)  # Scale with data size
        load_factor = min(self.processing_load / 200, 3.0)
        processing_time = base_time * (1 + load_factor)
        
        await asyncio.sleep(processing_time)
        
        # Higher failure rate under heavy load
        failure_rate = min(self.processing_load / 500, 0.15)  # Max 15% failure rate
        if random.random() < failure_rate:
            raise Exception(f"Task processing failed under stress: {task_id}")
        
        self.tasks[task_id] = {
            "data": task_data,
            "processed_at": time.time(),
            "status": "completed"
        }
        
        self.processing_load += 2
        return time.time() - start_time
    
    async def establish_connection(self, connection_id):
        """Establish a connection with stress simulation."""
        start_time = time.time()
        
        # Connection time increases with number of existing connections
        connection_overhead = len(self.connections) * 0.001
        processing_time = 0.01 + connection_overhead
        
        await asyncio.sleep(processing_time)
        
        # Connection failures under heavy load
        if len(self.connections) > 100:
            if random.random() < 0.2:  # 20% failure rate with >100 connections
                raise Exception(f"Connection limit exceeded: {connection_id}")
        
        self.connections.add(connection_id)
        return time.time() - start_time
    
    def cleanup_resources(self):
        """Cleanup resources to simulate garbage collection."""
        # Reduce processing load over time
        self.processing_load = max(0, self.processing_load - 5)

@pytest.mark.stress
class TestStressTesting:
    """Stress testing suite for the autonomous development system."""
    
    @pytest.fixture
    def stress_system(self):
        """Create stress test system."""
        return MockStressTestSystem()
    
    @pytest.mark.asyncio
    async def test_agent_creation_stress(self, stress_system):
        """Stress test agent creation under heavy load."""
        scenario = StressTestScenario("Agent Creation Stress", duration_seconds=30)
        scenario.start()
        
        async def create_agent_worker(worker_id):
            agent_count = 0
            while scenario.running:
                try:
                    agent_id = f"stress_agent_{worker_id}_{agent_count}"
                    response_time = await stress_system.create_agent(agent_id)
                    scenario.record_operation(success=True, response_time=response_time)
                    agent_count += 1
                    
                    # Small delay to prevent overwhelming
                    await asyncio.sleep(0.01)
                    
                except Exception as e:
                    scenario.record_operation(success=False)
                    await asyncio.sleep(0.1)  # Back off on failure
        
        # Run multiple workers concurrently
        workers = [create_agent_worker(i) for i in range(10)]
        
        # Let it run for the specified duration
        await asyncio.sleep(scenario.duration_seconds)
        scenario.stop()
        
        # Cancel workers
        for worker in workers:
            if not worker.done():
                worker.cancel()
        
        # Analyze results
        results = scenario.get_results()
        
        # Stress test assertions
        assert results["total_operations"] > 100, "Not enough operations completed under stress"
        assert results["success_rate"] > 0.8, f"Success rate too low: {results['success_rate']}"
        assert results["peak_memory_mb"] < 1000, f"Memory usage too high: {results['peak_memory_mb']}MB"
        assert results["average_response_time"] < 1.0, f"Response time too high: {results['average_response_time']}s"
    
    @pytest.mark.asyncio
    async def test_concurrent_task_processing_stress(self, stress_system):
        """Stress test concurrent task processing."""
        scenario = StressTestScenario("Task Processing Stress", duration_seconds=45)
        scenario.start()
        
        async def task_processing_worker(worker_id):
            task_count = 0
            while scenario.running:
                try:
                    task_id = f"stress_task_{worker_id}_{task_count}"
                    task_data = {
                        "operation": "stress_test",
                        "payload": "x" * random.randint(100, 1000),
                        "worker_id": worker_id,
                        "task_count": task_count
                    }
                    
                    response_time = await stress_system.process_task(task_id, task_data)
                    scenario.record_operation(success=True, response_time=response_time)
                    task_count += 1
                    
                    # Variable delay to simulate realistic workload
                    await asyncio.sleep(random.uniform(0.005, 0.02))
                    
                except Exception as e:
                    scenario.record_operation(success=False)
                    await asyncio.sleep(0.05)  # Back off on failure
        
        # Run many concurrent workers
        workers = [task_processing_worker(i) for i in range(20)]
        
        # Let it run for the specified duration
        await asyncio.sleep(scenario.duration_seconds)
        scenario.stop()
        
        # Cancel workers
        for worker in workers:
            if not worker.done():
                worker.cancel()
        
        # Analyze results
        results = scenario.get_results()
        
        # Stress test assertions
        assert results["total_operations"] > 500, "Not enough operations completed under stress"
        assert results["success_rate"] > 0.75, f"Success rate too low: {results['success_rate']}"
        assert results["operations_per_second"] > 10, f"Throughput too low: {results['operations_per_second']} ops/sec"
    
    @pytest.mark.asyncio
    async def test_connection_saturation_stress(self, stress_system):
        """Stress test connection handling under saturation."""
        scenario = StressTestScenario("Connection Saturation", duration_seconds=20)
        scenario.start()
        
        async def connection_worker(worker_id):
            connection_count = 0
            while scenario.running:
                try:
                    connection_id = f"stress_conn_{worker_id}_{connection_count}"
                    response_time = await stress_system.establish_connection(connection_id)
                    scenario.record_operation(success=True, response_time=response_time)
                    connection_count += 1
                    
                    # Rapid connection attempts
                    await asyncio.sleep(0.001)
                    
                except Exception as e:
                    scenario.record_operation(success=False)
                    await asyncio.sleep(0.01)  # Brief back off
        
        # Many concurrent connection attempts
        workers = [connection_worker(i) for i in range(15)]
        
        # Let it run for the specified duration
        await asyncio.sleep(scenario.duration_seconds)
        scenario.stop()
        
        # Cancel workers
        for worker in workers:
            if not worker.done():
                worker.cancel()
        
        # Analyze results
        results = scenario.get_results()
        
        # Connection stress assertions
        assert results["total_operations"] > 200, "Not enough connection attempts"
        assert results["success_rate"] > 0.7, f"Connection success rate too low: {results['success_rate']}"
        assert len(stress_system.connections) > 50, "Not enough successful connections established"
    
    @pytest.mark.asyncio
    async def test_mixed_workload_stress(self, stress_system):
        """Stress test with mixed workload (agents, tasks, connections)."""
        scenario = StressTestScenario("Mixed Workload Stress", duration_seconds=60)
        scenario.start()
        
        async def mixed_worker(worker_id):
            operation_count = 0
            while scenario.running:
                try:
                    # Randomly choose operation type
                    operation_type = random.choice(["agent", "task", "connection"])
                    
                    if operation_type == "agent":
                        agent_id = f"mixed_agent_{worker_id}_{operation_count}"
                        response_time = await stress_system.create_agent(agent_id)
                    elif operation_type == "task":
                        task_id = f"mixed_task_{worker_id}_{operation_count}"
                        task_data = {"mixed": True, "size": random.randint(50, 500)}
                        response_time = await stress_system.process_task(task_id, task_data)
                    else:  # connection
                        conn_id = f"mixed_conn_{worker_id}_{operation_count}"
                        response_time = await stress_system.establish_connection(conn_id)
                    
                    scenario.record_operation(success=True, response_time=response_time)
                    operation_count += 1
                    
                    # Variable delay
                    await asyncio.sleep(random.uniform(0.01, 0.05))
                    
                except Exception as e:
                    scenario.record_operation(success=False)
                    await asyncio.sleep(0.02)
        
        # Cleanup worker to simulate garbage collection
        async def cleanup_worker():
            while scenario.running:
                stress_system.cleanup_resources()
                await asyncio.sleep(1)
        
        # Run mixed workload with cleanup
        workers = [mixed_worker(i) for i in range(12)]
        workers.append(cleanup_worker())
        
        # Let it run for the specified duration
        await asyncio.sleep(scenario.duration_seconds)
        scenario.stop()
        
        # Cancel workers
        for worker in workers:
            if not worker.done():
                worker.cancel()
        
        # Analyze results
        results = scenario.get_results()
        
        # Mixed workload assertions
        assert results["total_operations"] > 300, "Not enough mixed operations completed"
        assert results["success_rate"] > 0.8, f"Mixed workload success rate too low: {results['success_rate']}"
        assert results["peak_memory_mb"] < 2000, f"Memory usage too high under mixed load: {results['peak_memory_mb']}MB"
        assert results["average_response_time"] < 2.0, f"Average response time too high: {results['average_response_time']}s"