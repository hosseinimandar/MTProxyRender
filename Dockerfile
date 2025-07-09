# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# No external Python packages are needed for this script

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Run main.py when the container launches
CMD ["python", "main.py"]
