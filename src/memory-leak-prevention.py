#!/usr/bin/env python3
"""
Memory Leak Prevention System

Comprehensive memory management and leak prevention for the autonomous development system.
Addresses EventTarget memory leaks, resource cleanup, and performance optimization.

Author: Autonomous AI Development System
Version: 1.0.0
"""

import gc
import os
import sys
import time
import psutil
import threading
import weakref
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Any, Callable
from dataclasses import dataclass
from contextlib import contextmanager
from collections import defaultdict
import logging
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/memory-leak-prevention.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class MemoryMetrics:
    """Memory usage metrics."""
    timestamp: datetime
    total_memory: float  # MB
    used_memory: float   # MB
    available_memory: float  # MB
    cpu_percent: float
    active_threads: int
    active_processes: int
    python_objects: int

@dataclass
class ResourceHandle:
    """Resource handle for tracking and cleanup."""
    resource_id: str
    resource_type: str
    created_at: datetime
    cleanup_func: Optional[Callable] = None
    metadata: Optional[Dict] = None

class AbortControllerManager:
    """Manages AbortController instances to prevent EventTarget memory leaks."""
    
    def __init__(self, max_controllers: int = 10):
        self.max_controllers = max_controllers
        self.controllers: Dict[str, Any] = {}
        self.listener_counts: Dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()
        
    def create_controller(self, controller_id: str = None) -> str:
        """Create a new AbortController with automatic cleanup."""
        if controller_id is None:
            controller_id = f"controller_{int(time.time() * 1000000)}"
        
        with self._lock:
            # Clean up old controllers if we're at the limit
            if len(self.controllers) >= self.max_controllers:
                self._cleanup_oldest_controllers()
            
            # Create new controller (simulated - actual implementation would use JS AbortController)
            controller = {
                'id': controller_id,
                'created_at': datetime.now(),
                'aborted': False,
                'listeners': set()
            }
            
            self.controllers[controller_id] = controller
            self.listener_counts[controller_id] = 0
            
            logger.debug(f"Created AbortController: {controller_id}")
            return controller_id
    
    def add_listener(self, controller_id: str, listener_id: str) -> bool:
        """Add a listener to an AbortController."""
        with self._lock:
            if controller_id not in self.controllers:
                logger.warning(f"Controller not found: {controller_id}")
                return False
            
            controller = self.controllers[controller_id]
            if controller['aborted']:
                logger.warning(f"Cannot add listener to aborted controller: {controller_id}")
                return False
            
            controller['listeners'].add(listener_id)
            self.listener_counts[controller_id] += 1
            
            # Warn if too many listeners
            if self.listener_counts[controller_id] > 10:
                logger.warning(f"High listener count for controller {controller_id}: {self.listener_counts[controller_id]}")
            
            return True
    
    def abort_controller(self, controller_id: str) -> bool:
        """Abort a controller and clean up its listeners."""
        with self._lock:
            if controller_id not in self.controllers:
                return False
            
            controller = self.controllers[controller_id]
            controller['aborted'] = True
            
            # Clean up all listeners
            listener_count = len(controller['listeners'])
            controller['listeners'].clear()
            self.listener_counts[controller_id] = 0
            
            logger.debug(f"Aborted controller {controller_id}, cleaned up {listener_count} listeners")
            return True
    
    def cleanup_controller(self, controller_id: str) -> bool:
        """Completely remove a controller."""
        with self._lock:
            if controller_id in self.controllers:
                self.abort_controller(controller_id)
                del self.controllers[controller_id]
                del self.listener_counts[controller_id]
                logger.debug(f"Cleaned up controller: {controller_id}")
                return True
            return False
    
    def _cleanup_oldest_controllers(self, count: int = 3):
        """Clean up the oldest controllers."""
        if not self.controllers:
            return
        
        # Sort by creation time
        sorted_controllers = sorted(
            self.controllers.items(),
            key=lambda x: x[1]['created_at']
        )
        
        for i in range(min(count, len(sorted_controllers))):
            controller_id = sorted_controllers[i][0]
            self.cleanup_controller(controller_id)
    
    def get_stats(self) -> Dict:
        """Get statistics about controller usage."""
        with self._lock:
            total_listeners = sum(self.listener_counts.values())
            aborted_count = sum(1 for c in self.controllers.values() if c['aborted'])
            
            return {
                'total_controllers': len(self.controllers),
                'total_listeners': total_listeners,
                'aborted_controllers': aborted_count,
                'max_listeners_per_controller': max(self.listener_counts.values()) if self.listener_counts else 0
            }


class ResourceTracker:
    """Tracks and manages system resources to prevent leaks."""
    
    def __init__(self):
        self.resources: Dict[str, ResourceHandle] = {}
        self.resource_types: Dict[str, Set[str]] = defaultdict(set)
        self._lock = threading.Lock()
        self.cleanup_thread = None
        self.running = False
        
    def register_resource(self, resource_id: str, resource_type: str, 
                         cleanup_func: Callable = None, metadata: Dict = None) -> bool:
        """Register a resource for tracking."""
        with self._lock:
            if resource_id in self.resources:
                logger.warning(f"Resource already registered: {resource_id}")
                return False
            
            handle = ResourceHandle(
                resource_id=resource_id,
                resource_type=resource_type,
                created_at=datetime.now(),
                cleanup_func=cleanup_func,
                metadata=metadata or {}
            )
            
            self.resources[resource_id] = handle
            self.resource_types[resource_type].add(resource_id)
            
            logger.debug(f"Registered resource: {resource_id} ({resource_type})")
            return True
    
    def unregister_resource(self, resource_id: str) -> bool:
        """Unregister and clean up a resource."""
        with self._lock:
            if resource_id not in self.resources:
                return False
            
            handle = self.resources[resource_id]
            
            # Execute cleanup function if provided
            if handle.cleanup_func:
                try:
                    handle.cleanup_func()
                except Exception as e:
                    logger.error(f"Error in cleanup function for {resource_id}: {e}")
            
            # Remove from tracking
            self.resource_types[handle.resource_type].discard(resource_id)
            del self.resources[resource_id]
            
            logger.debug(f"Unregistered resource: {resource_id}")
            return True
    
    def cleanup_expired_resources(self, max_age_minutes: int = 60):
        """Clean up resources older than specified age."""
        cutoff_time = datetime.now() - timedelta(minutes=max_age_minutes)
        expired_resources = []
        
        with self._lock:
            for resource_id, handle in self.resources.items():
                if handle.created_at < cutoff_time:
                    expired_resources.append(resource_id)
        
        for resource_id in expired_resources:
            self.unregister_resource(resource_id)
            logger.info(f"Cleaned up expired resource: {resource_id}")
    
    def get_resource_stats(self) -> Dict:
        """Get statistics about tracked resources."""
        with self._lock:
            stats = {
                'total_resources': len(self.resources),
                'by_type': {rtype: len(resources) for rtype, resources in self.resource_types.items()},
                'oldest_resource': None,
                'resource_ages': {}
            }
            
            if self.resources:
                now = datetime.now()
                oldest_handle = min(self.resources.values(), key=lambda x: x.created_at)
                stats['oldest_resource'] = {
                    'id': oldest_handle.resource_id,
                    'type': oldest_handle.resource_type,
                    'age_minutes': (now - oldest_handle.created_at).total_seconds() / 60
                }
                
                # Calculate age distribution
                for handle in self.resources.values():
                    age_minutes = (now - handle.created_at).total_seconds() / 60
                    age_bucket = f"{int(age_minutes//10)*10}-{int(age_minutes//10)*10+10}min"
                    stats['resource_ages'][age_bucket] = stats['resource_ages'].get(age_bucket, 0) + 1
            
            return stats
    
    def start_cleanup_thread(self, interval_minutes: int = 5):
        """Start background cleanup thread."""
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            return
        
        self.running = True
        self.cleanup_thread = threading.Thread(target=self._cleanup_worker, args=(interval_minutes,))
        self.cleanup_thread.daemon = True
        self.cleanup_thread.start()
        logger.info("Started resource cleanup thread")
    
    def stop_cleanup_thread(self):
        """Stop background cleanup thread."""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=10)
        logger.info("Stopped resource cleanup thread")
    
    def _cleanup_worker(self, interval_minutes: int):
        """Background cleanup worker."""
        while self.running:
            try:
                self.cleanup_expired_resources()
                time.sleep(interval_minutes * 60)
            except Exception as e:
                logger.error(f"Error in cleanup worker: {e}")
                time.sleep(60)  # Wait 1 minute before retrying


class MemoryMonitor:
    """Monitors system memory usage and detects potential leaks."""
    
    def __init__(self, warning_threshold: float = 80.0, critical_threshold: float = 90.0):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.metrics_history: List[MemoryMetrics] = []
        self.max_history = 1000
        self._lock = threading.Lock()
        self.monitoring = False
        self.monitor_thread = None
        
    def get_current_metrics(self) -> MemoryMetrics:
        """Get current memory metrics."""
        process = psutil.Process()
        memory_info = psutil.virtual_memory()
        
        return MemoryMetrics(
            timestamp=datetime.now(),
            total_memory=memory_info.total / (1024 * 1024),  # MB
            used_memory=memory_info.used / (1024 * 1024),    # MB
            available_memory=memory_info.available / (1024 * 1024),  # MB
            cpu_percent=psutil.cpu_percent(interval=0.1),
            active_threads=threading.active_count(),
            active_processes=len(psutil.pids()),
            python_objects=len(gc.get_objects())
        )
    
    def record_metrics(self) -> MemoryMetrics:
        """Record current metrics and return them."""
        metrics = self.get_current_metrics()
        
        with self._lock:
            self.metrics_history.append(metrics)
            
            # Trim history if too long
            if len(self.metrics_history) > self.max_history:
                self.metrics_history = self.metrics_history[-self.max_history:]
        
        # Check for warnings
        memory_usage_percent = (metrics.used_memory / metrics.total_memory) * 100
        
        if memory_usage_percent > self.critical_threshold:
            logger.critical(f"CRITICAL: Memory usage at {memory_usage_percent:.1f}%")
            self.trigger_emergency_cleanup()
        elif memory_usage_percent > self.warning_threshold:
            logger.warning(f"WARNING: Memory usage at {memory_usage_percent:.1f}%")
        
        return metrics
    
    def detect_memory_leak(self, window_minutes: int = 10) -> Optional[Dict]:
        """Detect potential memory leaks by analyzing trends."""
        with self._lock:
            if len(self.metrics_history) < 2:
                return None
            
            # Get metrics from the specified window
            cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
            recent_metrics = [m for m in self.metrics_history if m.timestamp > cutoff_time]
            
            if len(recent_metrics) < 5:  # Need at least 5 data points
                return None
            
            # Calculate trends
            memory_trend = self._calculate_trend([m.used_memory for m in recent_metrics])
            object_trend = self._calculate_trend([m.python_objects for m in recent_metrics])
            thread_trend = self._calculate_trend([m.active_threads for m in recent_metrics])
            
            # Detect leak patterns
            leak_indicators = []
            
            if memory_trend > 0.5:  # Memory increasing
                leak_indicators.append(f"Memory usage increasing (trend: {memory_trend:.2f})")
            
            if object_trend > 100:  # Python objects increasing significantly
                leak_indicators.append(f"Python objects increasing (trend: {object_trend:.0f} objects/minute)")
            
            if thread_trend > 0.1:  # Thread count increasing
                leak_indicators.append(f"Thread count increasing (trend: {thread_trend:.2f})")
            
            if leak_indicators:
                return {
                    'timestamp': datetime.now(),
                    'indicators': leak_indicators,
                    'current_memory_mb': recent_metrics[-1].used_memory,
                    'memory_trend_mb_per_minute': memory_trend,
                    'object_count': recent_metrics[-1].python_objects,
                    'thread_count': recent_metrics[-1].active_threads
                }
            
            return None
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend (slope) of values over time."""
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        x_values = list(range(n))
        
        # Simple linear regression
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def trigger_emergency_cleanup(self):
        """Trigger emergency cleanup procedures."""
        logger.critical("Triggering emergency cleanup procedures")
        
        # Force garbage collection
        collected = gc.collect()
        logger.info(f"Garbage collection freed {collected} objects")
        
        # Clear weak references
        gc.collect()
        
        # Log current object types
        self.log_object_types()
    
    def log_object_types(self):
        """Log current Python object types for debugging."""
        obj_types = defaultdict(int)
        for obj in gc.get_objects():
            obj_types[type(obj).__name__] += 1
        
        # Log top 10 object types
        sorted_types = sorted(obj_types.items(), key=lambda x: x[1], reverse=True)[:10]
        logger.info("Top Python object types:")
        for obj_type, count in sorted_types:
            logger.info(f"  {obj_type}: {count}")
    
    def start_monitoring(self, interval_seconds: int = 30):
        """Start continuous memory monitoring."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_worker, args=(interval_seconds,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        logger.info("Started memory monitoring")
    
    def stop_monitoring(self):
        """Stop memory monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        logger.info("Stopped memory monitoring")
    
    def _monitor_worker(self, interval_seconds: int):
        """Background monitoring worker."""
        while self.monitoring:
            try:
                self.record_metrics()
                
                # Check for leaks every 5 minutes
                if len(self.metrics_history) % 10 == 0:  # Every 10 recordings
                    leak_detection = self.detect_memory_leak()
                    if leak_detection:
                        logger.warning(f"Potential memory leak detected: {leak_detection}")
                
                time.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"Error in memory monitor: {e}")
                time.sleep(60)


class MemoryLeakPreventionSystem:
    """Main memory leak prevention system."""
    
    def __init__(self):
        self.abort_manager = AbortControllerManager()
        self.resource_tracker = ResourceTracker()
        self.memory_monitor = MemoryMonitor()
        self.running = False
        
    def start(self):
        """Start the memory leak prevention system."""
        if self.running:
            return
        
        logger.info("Starting Memory Leak Prevention System")
        
        # Start subsystems
        self.resource_tracker.start_cleanup_thread()
        self.memory_monitor.start_monitoring()
        
        self.running = True
        logger.info("Memory Leak Prevention System started successfully")
    
    def stop(self):
        """Stop the memory leak prevention system."""
        if not self.running:
            return
        
        logger.info("Stopping Memory Leak Prevention System")
        
        # Stop subsystems
        self.resource_tracker.stop_cleanup_thread()
        self.memory_monitor.stop_monitoring()
        
        # Clean up all resources
        self.cleanup_all_resources()
        
        self.running = False
        logger.info("Memory Leak Prevention System stopped")
    
    def cleanup_all_resources(self):
        """Clean up all tracked resources."""
        logger.info("Cleaning up all resources")
        
        # Clean up all AbortControllers
        with self.abort_manager._lock:
            controller_ids = list(self.abort_manager.controllers.keys())
            for controller_id in controller_ids:
                self.abort_manager.cleanup_controller(controller_id)
        
        # Clean up all tracked resources
        with self.resource_tracker._lock:
            resource_ids = list(self.resource_tracker.resources.keys())
            for resource_id in resource_ids:
                self.resource_tracker.unregister_resource(resource_id)
        
        # Force garbage collection
        collected = gc.collect()
        logger.info(f"Final garbage collection freed {collected} objects")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status."""
        return {
            'timestamp': datetime.now().isoformat(),
            'running': self.running,
            'abort_controllers': self.abort_manager.get_stats(),
            'resource_tracker': self.resource_tracker.get_resource_stats(),
            'memory_metrics': self.memory_monitor.get_current_metrics().__dict__,
            'potential_leaks': self.memory_monitor.detect_memory_leak()
        }
    
    @contextmanager
    def managed_resource(self, resource_type: str, cleanup_func: Callable = None):
        """Context manager for automatic resource management."""
        resource_id = f"{resource_type}_{int(time.time() * 1000000)}"
        
        try:
            self.resource_tracker.register_resource(resource_id, resource_type, cleanup_func)
            yield resource_id
        finally:
            self.resource_tracker.unregister_resource(resource_id)
    
    def create_managed_abort_controller(self) -> str:
        """Create a managed AbortController with automatic cleanup."""
        controller_id = self.abort_manager.create_controller()
        
        # Register with resource tracker for additional cleanup
        cleanup_func = lambda: self.abort_manager.cleanup_controller(controller_id)
        self.resource_tracker.register_resource(
            f"abort_controller_{controller_id}",
            "abort_controller",
            cleanup_func
        )
        
        return controller_id


# Global instance
memory_system = MemoryLeakPreventionSystem()


def main():
    """Main entry point for testing and monitoring."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Leak Prevention System")
    parser.add_argument('--start', action='store_true', help='Start the system')
    parser.add_argument('--stop', action='store_true', help='Stop the system')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--monitor', type=int, default=0, help='Monitor for N seconds')
    
    args = parser.parse_args()
    
    if args.start:
        memory_system.start()
        print("Memory Leak Prevention System started")
    
    elif args.stop:
        memory_system.stop()
        print("Memory Leak Prevention System stopped")
    
    elif args.status:
        status = memory_system.get_system_status()
        print(json.dumps(status, indent=2, default=str))
    
    elif args.monitor:
        memory_system.start()
        print(f"Monitoring for {args.monitor} seconds...")
        time.sleep(args.monitor)
        status = memory_system.get_system_status()
        print("\nFinal Status:")
        print(json.dumps(status, indent=2, default=str))
        memory_system.stop()
    
    else:
        print("Use --start, --stop, --status, or --monitor <seconds>")


if __name__ == "__main__":
    main()