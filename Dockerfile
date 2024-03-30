# Use Python 3.9.12 as the base image
FROM python:3.9.12-slim

# Expose port 8080 to allow communication to the outside world
EXPOSE 8080

# Set working directory within the container to /app
WORKDIR /app

# Copy requirements.txt from the current directory into the container's /app directory
COPY requirements.txt .

# Upgrade pip and install required Python packages from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Copy the main application file app.py from the current directory into the container's /app directory
COPY app.py .

# Copy the src folder and config.py from the current directory into the container's /app directory
COPY src ./src
COPY config.py .
COPY logger.py .

# Define the entry point command to run the Streamlit application with port 8080
ENTRYPOINT [ "streamlit", "run", "--server.port=8080"]

# Specify the default command to execute when the container starts, running app.py
CMD ["app.py"]
