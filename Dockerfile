# Dockerfile
FROM python:3.8-slim

WORKDIR /app

# Copy the log generator script into the container
COPY log_generator.py .

# Install the kafka-python library
RUN pip install kafka-python

# Run the log generator script
CMD ["python", "log_generator.py"]
