# Start with python 3.11 image
FROM python:3.11-slim

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy the current directory into /app on the image
WORKDIR /app
COPY . /app

# Entry point command
CMD ["python", "main.py"]