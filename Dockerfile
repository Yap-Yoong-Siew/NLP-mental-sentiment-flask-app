FROM ubuntu:20.04

# Update the package lists and install necessary dependencies
RUN apt-get update \
    && apt-get install -y python3 python3-pip build-essential 

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the entrypoint command (modify it according to your application)
CMD ["python3", "lecturer_es.py"]
