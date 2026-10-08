# ==============================================================================
# Dockerfile – College Club Management System (v0.4 Containerized Release)
# Course: 24CYS401 – Secure Software Engineering
# Security Controls:
#   - Non-root user execution (appuser:appgroup, UID 10001:10001)
#   - Minimal Debian slim base image (python:3.12-slim-bookworm)
#   - No-cache dependency installation to prevent cache bloat
#   - Secure file and directory permissions (0750 on instance data directory)
#   - Built-in urllib-based healthcheck (no curl/wget attack surface)
#   - Production WSGI execution via Gunicorn
# ==============================================================================

FROM python:3.12-slim-bookworm AS runtime

# Set environment variables for Python runtime security and performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=5000 \
    PATH="/home/appuser/.local/bin:$PATH"

# Create unprivileged system group and user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin -M -d /app appuser

# Set working directory
WORKDIR /app

# Create persistent instance directory for SQLite and set ownership
RUN mkdir -p /app/instance && \
    chown -R appuser:appgroup /app && \
    chmod 750 /app/instance

# Copy requirements file first for optimal layer caching
COPY requirements.txt /app/requirements.txt

# Install dependencies as root then cleanup any temporary files
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code with non-root ownership
COPY --chown=appuser:appgroup app /app/app
COPY --chown=appuser:appgroup templates /app/templates
COPY --chown=appuser:appgroup static /app/static
COPY --chown=appuser:appgroup run.py /app/run.py

# Switch to unprivileged non-root user
USER appuser

# Expose container application port
EXPOSE 5000

# Container healthcheck using standard library urllib (no shell or curl dependency)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/login', timeout=4)" || exit 1

# Production WSGI server command execution
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "run:app"]
