# Start with python 3.11 image
FROM python:3.11

# Copy the current directory into /app on the image
WORKDIR /app
COPY . /app

# Entry point command
CMD ["python", "main.py"]