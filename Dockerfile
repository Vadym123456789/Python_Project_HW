# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port if your app needs it (adjust if needed)
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]