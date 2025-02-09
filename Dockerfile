# Dockerfile
FROM python:3.8-slim

WORKDIR /app

# Copy the scripts into the container
COPY log_generator.py .
COPY log_consumer.py .

# Install required Python packages
RUN pip install kafka-python elasticsearch

# By default, run the log generator (this can be overridden by the service command)
CMD ["python", "log_generator.py"]
