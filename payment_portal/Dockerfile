# syntax=docker/dockerfile:1
# -----------------------------------
# Stage 1: Base image
# -----------------------------------
FROM python:3.12-slim-bookworm

# Prevents Python from writing .pyc files and ensures output is flushed
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------------
# System dependencies
# -----------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gnupg \
    ca-certificates \
    unixodbc-dev \
    apt-transport-https \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------
# Install Microsoft ODBC Driver for Azure SQL
# -----------------------------------
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
      > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------------
# Set working directory
# -----------------------------------
WORKDIR /app

# -----------------------------------
# Install Python dependencies
# -----------------------------------
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# -----------------------------------
# Copy Django project files
# -----------------------------------
COPY . /app

# -----------------------------------
# Entrypoint setup
# -----------------------------------
COPY ./deploy/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# -----------------------------------
# Environment and Ports
# -----------------------------------
ENV PORT=8000
EXPOSE 8000

# -----------------------------------
# Run the Django app
# -----------------------------------
ENTRYPOINT ["/app/entrypoint.sh"]
