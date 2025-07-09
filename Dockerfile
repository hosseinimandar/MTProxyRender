# Use a minimal and official Python image
FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /app

# Copy the main script into the container
COPY main.py .

# Expose the internal port the proxy will run on
EXPOSE 8888

# Command to run when the container starts
CMD ["python", "main.py"]
