# Base image for Python 3.10
FROM python:3.10-slim

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . /app/backend

# Set the Python path so module imports work correctly
ENV PYTHONPATH=/app

# Expose port for FastMCP Server
EXPOSE 8080
ENV PORT 8080

# The default command will run the Orchestrator loop
# To run the MCP server instead, override the CMD in Cloud Run settings.
CMD ["python", "-m", "backend.orchestrator"]
