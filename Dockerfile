# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8080 (Google Cloud Run default)
EXPOSE 8080

# Command to run the application
# initial:app means "in initial.py, use the app object"
CMD ["uvicorn", "initial:app", "--host", "0.0.0.0", "--port", "8080"]
