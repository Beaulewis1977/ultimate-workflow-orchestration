# Autonomous Development System - Testing & Validation Suite

## Overview

This comprehensive testing suite provides thorough validation and quality assurance for the autonomous development system. It includes unit tests, integration tests, end-to-end testing, performance benchmarks, security validation, and automated CI/CD pipelines.

## Test Structure

```
testing/
├── unit/                   # Unit tests for individual components
├── integration/           # Integration tests for component interactions
├── e2e/                   # End-to-end workflow testing with Playwright
├── performance/           # Performance and load testing
├── validation/            # Project detection and memory validation
├── qa/                    # Quality assurance and security testing
├── automation/            # CI/CD pipeline automation
├── data/                  # Test data generators and mock scenarios
├── reports/               # Generated test reports and coverage
├── Dockerfile             # Multi-stage Docker build for testing
├── docker-compose.yml     # Complete testing environment
├── requirements.txt       # Testing dependencies
├── pytest.ini            # Pytest configuration
├── conftest.py           # Global test fixtures and configuration
└── run_tests.py          # Main test runner script
```

## Quick Start

### Local Testing

1. **Install dependencies:**
   ```bash
   cd testing/
   pip install -r requirements.txt
   ```

2. **Run all tests:**
   ```bash
   python run_tests.py --suite all
   ```

3. **Run specific test suite:**
   ```bash
   python run_tests.py --suite unit
   python run_tests.py --suite integration
   python run_tests.py --suite e2e
   python run_tests.py --suite performance
   ```

### Docker Testing

1. **Build and run tests in Docker:**
   ```bash
   docker-compose run --rm test-runner
   ```

2. **Run specific environments:**
   ```bash
   # Development environment with debugging
   docker-compose run --rm test-dev
   
   # CI/CD environment with full reporting
   docker-compose run --rm test-ci
   
   # Performance testing
   docker-compose run --rm test-performance
   
   # Security testing
   docker-compose run --rm test-security
   ```

3. **Start monitoring stack:**
   ```bash
   docker-compose up -d test-prometheus test-grafana
   ```

## Test Suites

### Unit Tests (`unit/`)

Tests individual components in isolation:
- **Orchestrator tests** (`test_orchestrator.py`) - Core orchestration logic
- **Claude config detection** (`test_claude_config_detector.py`) - Configuration parsing
- **Tmux utilities** (`test_tmux_utils.py`) - Session management

**Run:** `python run_tests.py --suite unit`

### Integration Tests (`integration/`)

Tests component interactions and tool integration:
- **Tool integration** (`test_tool_integration.py`) - TaskMaster AI, GitHub, Fetch tool interactions
- **Workflow coordination** - Agent collaboration testing
- **Data persistence** - Storage and retrieval validation

**Run:** `python run_tests.py --suite integration`

### End-to-End Tests (`e2e/`)

Full workflow testing using Playwright:
- **Autonomous workflow** (`test_autonomous_workflow.py`) - Complete project lifecycle
- **Project lifecycle** (`test_project_lifecycle.py`) - Multi-phase development
- **User interface testing** - Dashboard and monitoring interfaces

**Run:** `python run_tests.py --suite e2e`

### Performance Tests (`performance/`)

Load testing and performance validation:
- **Load testing** (`test_load_testing.py`) - Concurrent operations and scaling
- **Stress testing** (`test_stress_testing.py`) - High-load scenarios
- **Memory profiling** - Resource usage monitoring
- **Benchmark comparisons** - Performance regression detection

**Run:** `python run_tests.py --suite performance`

### Validation Tests (`validation/`)

System validation and compliance:
- **Project detection** (`test_project_detection.py`) - CLAUDE.md parsing and validation
- **Memory management** (`test_memory_management.py`) - Leak detection and resource monitoring
- **Configuration validation** - Settings and environment verification

**Run:** `python run_tests.py --suite validation`

### Quality Assurance (`qa/`)

Code quality and security validation:
- **Security testing** (`test_security_validation.py`) - Vulnerability scanning and validation
- **Code quality** (`test_code_quality.py`) - Standards compliance and metrics
- **Static analysis** - Code structure and maintainability

**Run:** `python run_tests.py --suite qa`

## Advanced Usage

### Custom Test Markers

Filter tests using pytest markers:

```bash
# Run only critical tests
python run_tests.py --suite all --markers critical

# Run only smoke tests
python run_tests.py --suite all --markers smoke

# Run memory-specific tests
python run_tests.py --suite all --markers memory
```

### Parallel Execution

Run tests in parallel for faster execution:

```bash
# Use pytest-xdist for parallel execution
pytest -n auto unit/ integration/
```

### Coverage Reports

Generate detailed coverage reports:

```bash
# HTML coverage report
pytest unit/ --cov=../ --cov-report=html:reports/coverage

# XML coverage for CI/CD
pytest unit/ --cov=../ --cov-report=xml:reports/coverage.xml
```

### Performance Benchmarking

Run performance benchmarks with detailed metrics:

```bash
pytest performance/ --benchmark-json=reports/benchmark.json --benchmark-min-rounds=5
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd testing/
          python run_tests.py --suite all --fail-fast
```

### GitLab CI

```yaml
stages:
  - test

test:
  stage: test
  script:
    - cd testing/
    - python run_tests.py --suite all
  artifacts:
    reports:
      junit: testing/reports/*_report.xml
      coverage_report:
        coverage_format: cobertura
        path: testing/reports/coverage.xml
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'cd testing/ && python run_tests.py --suite all'
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'testing/reports',
                        reportFiles: 'test_report.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }
    }
}
```

## Configuration

### Environment Variables

- `TESTING=true` - Enable testing mode
- `BMAD_WORKSPACE=/path/to/workspace` - Set workspace path
- `LOG_LEVEL=DEBUG` - Set logging level
- `CI=true` - Enable CI-specific behaviors

### Pytest Configuration

Key settings in `pytest.ini`:
- Test discovery patterns
- Marker definitions
- Coverage settings
- Report generation
- Timeout configurations

## Monitoring and Reporting

### Test Reports

All test runs generate comprehensive reports:
- **HTML reports** - Detailed test results with logs
- **Coverage reports** - Code coverage analysis
- **Performance reports** - Benchmark results and trends
- **Security reports** - Vulnerability assessments

### Monitoring Dashboard

Access monitoring at `http://localhost:3000` (Grafana) when running:
```bash
docker-compose up -d test-grafana test-prometheus
```

## Troubleshooting

### Common Issues

1. **Docker permission errors:**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Playwright browser issues:**
   ```bash
   playwright install chromium
   ```

3. **Memory issues during testing:**
   ```bash
   # Increase Docker memory limits
   docker-compose run --rm -e PYTEST_TIMEOUT=3600 test-runner
   ```

### Debug Mode

Run tests with detailed debugging:

```bash
# Local debugging
python run_tests.py --suite unit --markers debug

# Docker debugging
docker-compose run --rm test-dev pytest unit/ --pdb --tb=long
```

### Performance Issues

If tests are running slowly:

1. Use parallel execution: `pytest -n auto`
2. Skip slow tests: `pytest -m "not slow"`
3. Use Docker for isolation: `docker-compose run test-performance`

## Contributing

When adding new tests:

1. Follow the existing structure and naming conventions
2. Add appropriate markers for test categorization
3. Include docstrings and clear assertions
4. Update this README if adding new test suites
5. Ensure tests pass in both local and Docker environments

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review test logs in `reports/` directory
3. Run tests with `--verbose` for detailed output
4. Use `--tb=long` for full error tracebacks