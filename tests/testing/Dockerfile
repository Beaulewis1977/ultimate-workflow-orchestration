# Multi-stage Docker build for autonomous development system testing
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    nodejs \
    npm \
    docker.io \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set up Chrome for Playwright
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/bin/chromium

# Create working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium

# Copy test files
COPY . .

# Create test user (non-root for security)
RUN useradd -m -u 1000 testuser && \
    chown -R testuser:testuser /app
USER testuser

# Development stage with additional tools
FROM base as development

USER root

# Install development tools
RUN pip install --no-cache-dir \
    ipdb \
    pytest-xvfb \
    pytest-timeout \
    pytest-rerunfailures

# Install additional security tools
RUN pip install --no-cache-dir \
    bandit \
    safety \
    semgrep

USER testuser

# Production testing stage
FROM base as production

# Copy only necessary files
COPY --chown=testuser:testuser conftest.py pytest.ini ./
COPY --chown=testuser:testuser unit/ unit/
COPY --chown=testuser:testuser integration/ integration/
COPY --chown=testuser:testuser e2e/ e2e/
COPY --chown=testuser:testuser performance/ performance/
COPY --chown=testuser:testuser validation/ validation/
COPY --chown=testuser:testuser qa/ qa/
COPY --chown=testuser:testuser automation/ automation/
COPY --chown=testuser:testuser data/ data/

# Set default command
CMD ["pytest", "--verbose", "--tb=short"]

# CI/CD stage optimized for continuous integration
FROM base as ci

# Install CI-specific tools
RUN pip install --no-cache-dir \
    pytest-html \
    pytest-json-report \
    pytest-cov \
    codecov

# Copy test configuration
COPY --chown=testuser:testuser pytest.ini conftest.py ./
COPY --chown=testuser:testuser . .

# Create reports directory
RUN mkdir -p reports && chown testuser:testuser reports

# Default CI command with reporting
CMD ["pytest", \
     "--verbose", \
     "--tb=short", \
     "--html=reports/test_report.html", \
     "--self-contained-html", \
     "--json-report", \
     "--json-report-file=reports/test_report.json", \
     "--cov=../", \
     "--cov-report=html:reports/coverage", \
     "--cov-report=xml:reports/coverage.xml"]