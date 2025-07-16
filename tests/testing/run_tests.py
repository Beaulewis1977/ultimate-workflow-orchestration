#!/usr/bin/env python3
"""
Main test runner for the autonomous development system testing suite.
"""
import os
import sys
import argparse
import subprocess
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestRunner:
    """Main test runner for the autonomous development system."""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.testing_path = self.workspace_path / "testing"
        self.reports_path = self.testing_path / "reports"
        self.reports_path.mkdir(exist_ok=True)
        
        self.test_suites = {
            "unit": "unit/",
            "integration": "integration/",
            "e2e": "e2e/",
            "performance": "performance/",
            "validation": "validation/",
            "qa": "qa/",
            "security": "qa/test_security_validation.py",
            "memory": "validation/test_memory_management.py"
        }
    
    def run_test_suite(self, suite_name: str, **kwargs) -> Dict[str, Any]:
        """Run a specific test suite."""
        if suite_name not in self.test_suites:
            raise ValueError(f"Unknown test suite: {suite_name}")
        
        suite_path = self.test_suites[suite_name]
        start_time = time.time()
        
        logger.info(f"Running {suite_name} tests from {suite_path}")
        
        # Build pytest command
        cmd = self._build_pytest_command(suite_path, suite_name, **kwargs)
        
        # Run tests
        try:
            result = subprocess.run(
                cmd,
                cwd=self.testing_path,
                capture_output=True,
                text=True,
                timeout=kwargs.get('timeout', 1800)  # 30 minute default timeout
            )
            
            duration = time.time() - start_time
            
            return {
                "suite": suite_name,
                "status": "passed" if result.returncode == 0 else "failed",
                "duration": duration,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(cmd)
            }
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                "suite": suite_name,
                "status": "timeout",
                "duration": duration,
                "exit_code": -1,
                "error": "Test suite timed out"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "suite": suite_name,
                "status": "error",
                "duration": duration,
                "exit_code": -1,
                "error": str(e)
            }
    
    def _build_pytest_command(self, suite_path: str, suite_name: str, **kwargs) -> List[str]:
        """Build pytest command with appropriate options."""
        cmd = ["python", "-m", "pytest", suite_path]
        
        # Common options
        cmd.extend([
            "--verbose",
            "--tb=short",
            f"--html={self.reports_path}/{suite_name}_report.html",
            "--self-contained-html"
        ])
        
        # Coverage for unit and integration tests
        if suite_name in ["unit", "integration"]:
            cmd.extend([
                "--cov=../",
                f"--cov-report=html:{self.reports_path}/{suite_name}_coverage",
                f"--cov-report=xml:{self.reports_path}/{suite_name}_coverage.xml"
            ])
        
        # Performance benchmarks
        if suite_name == "performance":
            cmd.extend([
                "--benchmark-json=" + str(self.reports_path / "benchmark.json"),
                "--benchmark-min-rounds=3"
            ])
        
        # Security specific options
        if suite_name == "security":
            cmd.extend([
                "--disable-warnings",
                "-x"  # Stop on first failure for security tests
            ])
        
        # Memory testing options
        if suite_name == "memory":
            cmd.extend([
                "--tb=long",
                "--capture=no"  # Show memory info in real-time
            ])
        
        # Add custom markers
        if kwargs.get('markers'):
            for marker in kwargs['markers']:
                cmd.extend(["-m", marker])
        
        # Add custom options
        if kwargs.get('pytest_args'):
            cmd.extend(kwargs['pytest_args'])
        
        return cmd
    
    def run_all_tests(self, exclude_suites: List[str] = None, **kwargs) -> Dict[str, Any]:
        """Run all test suites."""
        exclude_suites = exclude_suites or []
        results = {}
        overall_start_time = time.time()
        
        logger.info("Starting comprehensive test run")
        
        # Run each test suite
        for suite_name in self.test_suites:
            if suite_name in exclude_suites:
                logger.info(f"Skipping {suite_name} tests (excluded)")
                continue
            
            result = self.run_test_suite(suite_name, **kwargs)
            results[suite_name] = result
            
            # Log result
            status = result["status"]
            duration = result["duration"]
            logger.info(f"{suite_name} tests {status} in {duration:.2f}s")
            
            # Stop on first failure if fail_fast is enabled
            if kwargs.get('fail_fast') and status != "passed":
                logger.warning(f"Stopping test run due to {suite_name} failure (fail_fast enabled)")
                break
        
        overall_duration = time.time() - overall_start_time
        
        # Calculate overall statistics
        total_suites = len(results)
        passed_suites = len([r for r in results.values() if r["status"] == "passed"])
        failed_suites = len([r for r in results.values() if r["status"] == "failed"])
        error_suites = len([r for r in results.values() if r["status"] == "error"])
        timeout_suites = len([r for r in results.values() if r["status"] == "timeout"])
        
        overall_result = {
            "overall_status": "passed" if passed_suites == total_suites else "failed",
            "total_duration": overall_duration,
            "statistics": {
                "total_suites": total_suites,
                "passed": passed_suites,
                "failed": failed_suites,
                "errors": error_suites,
                "timeouts": timeout_suites
            },
            "suite_results": results
        }
        
        # Save overall results
        results_file = self.reports_path / "overall_results.json"
        with open(results_file, 'w') as f:
            json.dump(overall_result, f, indent=2)
        
        logger.info(f"Test run completed: {passed_suites}/{total_suites} suites passed in {overall_duration:.2f}s")
        
        return overall_result
    
    def run_docker_tests(self, service: str = "test-runner", **kwargs) -> Dict[str, Any]:
        """Run tests in Docker environment."""
        logger.info(f"Running tests in Docker service: {service}")
        
        start_time = time.time()
        
        try:
            # Build and run Docker service
            cmd = ["docker-compose", "run", "--rm", service]
            
            if kwargs.get('pytest_args'):
                cmd.extend(kwargs['pytest_args'])
            
            result = subprocess.run(
                cmd,
                cwd=self.testing_path,
                capture_output=True,
                text=True,
                timeout=kwargs.get('timeout', 3600)  # 1 hour timeout for Docker
            )
            
            duration = time.time() - start_time
            
            return {
                "service": service,
                "status": "passed" if result.returncode == 0 else "failed",
                "duration": duration,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except Exception as e:
            duration = time.time() - start_time
            return {
                "service": service,
                "status": "error",
                "duration": duration,
                "error": str(e)
            }
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive test report."""
        report_lines = [
            "# Autonomous Development System - Test Report",
            f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Overall Summary",
            f"- **Status**: {results['overall_status'].upper()}",
            f"- **Duration**: {results['total_duration']:.2f} seconds",
            f"- **Total Suites**: {results['statistics']['total_suites']}",
            f"- **Passed**: {results['statistics']['passed']}",
            f"- **Failed**: {results['statistics']['failed']}",
            f"- **Errors**: {results['statistics']['errors']}",
            f"- **Timeouts**: {results['statistics']['timeouts']}",
            "",
            "## Suite Results"
        ]
        
        for suite_name, result in results["suite_results"].items():
            status_emoji = {
                "passed": "✅",
                "failed": "❌", 
                "error": "⚠️",
                "timeout": "⏰"
            }.get(result["status"], "❓")
            
            report_lines.extend([
                f"### {suite_name.title()} Tests {status_emoji}",
                f"- **Status**: {result['status'].upper()}",
                f"- **Duration**: {result['duration']:.2f}s",
                f"- **Exit Code**: {result['exit_code']}",
                ""
            ])
            
            if result["status"] != "passed":
                report_lines.extend([
                    "**Error Details:**",
                    "```",
                    result.get("stderr", result.get("error", "No error details available"))[:500] + "...",
                    "```",
                    ""
                ])
        
        report_content = "\n".join(report_lines)
        
        # Save report
        report_file = self.reports_path / "test_report.md"
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        return str(report_file)

def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Autonomous Development System Test Runner")
    
    parser.add_argument(
        "--suite", 
        choices=list(TestRunner({}).test_suites.keys()) + ["all"],
        default="all",
        help="Test suite to run"
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        help="Run tests in Docker environment"
    )
    parser.add_argument(
        "--docker-service",
        default="test-runner",
        help="Docker service to use for testing"
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Test suites to exclude"
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first test suite failure"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1800,
        help="Timeout for test execution (seconds)"
    )
    parser.add_argument(
        "--workspace",
        help="Path to workspace directory"
    )
    parser.add_argument(
        "--markers",
        nargs="*",
        help="Pytest markers to filter tests"
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Generate report from existing results"
    )
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = TestRunner(args.workspace)
    
    if args.report_only:
        # Load existing results and generate report
        results_file = runner.reports_path / "overall_results.json"
        if results_file.exists():
            with open(results_file) as f:
                results = json.load(f)
            report_file = runner.generate_report(results)
            print(f"Report generated: {report_file}")
        else:
            print("No existing results found")
        return
    
    # Run tests
    if args.docker:
        # Run in Docker
        pytest_args = []
        if args.markers:
            for marker in args.markers:
                pytest_args.extend(["-m", marker])
        
        result = runner.run_docker_tests(
            service=args.docker_service,
            timeout=args.timeout,
            pytest_args=pytest_args
        )
        
        print(f"Docker tests {result['status']} in {result['duration']:.2f}s")
        if result['status'] != 'passed':
            print("STDERR:", result.get('stderr', ''))
            sys.exit(1)
    
    else:
        # Run locally
        if args.suite == "all":
            results = runner.run_all_tests(
                exclude_suites=args.exclude,
                fail_fast=args.fail_fast,
                timeout=args.timeout,
                markers=args.markers
            )
            
            # Generate report
            report_file = runner.generate_report(results)
            print(f"Test report generated: {report_file}")
            
            # Exit with error code if tests failed
            if results["overall_status"] != "passed":
                sys.exit(1)
        
        else:
            result = runner.run_test_suite(
                args.suite,
                timeout=args.timeout,
                markers=args.markers
            )
            
            print(f"{args.suite} tests {result['status']} in {result['duration']:.2f}s")
            if result['status'] != 'passed':
                print("STDERR:", result.get('stderr', ''))
                sys.exit(1)

if __name__ == "__main__":
    main()