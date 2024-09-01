# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the app files into the container at /app
COPY ./src /app/
COPY ./requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 8000

# Run the Flask app
CMD ["python3", "pocket.py"]
