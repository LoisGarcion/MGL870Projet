# Use an official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (optional, if the script serves something via Flask/FastAPI)
EXPOSE 5000

# Define the command to run the script
CMD ["python", "livedetection.py"]
