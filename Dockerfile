# Use Python 3.14 slim image as base
FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1

# Set work directory
WORKDIR /app

# Install system dependencies including Rust
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . ~/.cargo/env

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy project
COPY . /app/

# Create directory for static files
RUN mkdir -p /app/static

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
