# Use the official Python image from the Docker Hub, specifically the 3.10-slim-bullseye version.
FROM python:3.10-slim-bullseye

# Update the package list and install necessary packages:
# - build-essential: Provides necessary tools for building software
# - default-libmysqlclient-dev: Development files for MySQL client
# - pkg-config: Tool to configure compiler and linker flags for libraries
# After that, upgrade pip to the latest version.
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev pkg-config \
  && pip install --no-cache-dir --upgrade pip

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file from the host machine to the /app directory in the container
COPY ./requirements.txt /app

# Install Python dependencies specified in the requirements.txt file
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy all files from the current directory on the host machine to the /app directory in the container
COPY . /app

# Expose port 5000 to allow access to the application running inside the container
EXPOSE 5000

# Specify the command to run when the container starts: run the server.py script with Python 3
CMD ["python3", "server.py"]
