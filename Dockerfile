# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional: for pip and python-dotenv)
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install python-dotenv

# Copy backend source files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Set environment variable for Python (optional, for unbuffered output)
ENV PYTHONUNBUFFERED=1

# Default command to run FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]