# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Make port  available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]


# FROM python:3.9

# WORKDIR /app

# COPY . /app

# RUN pip install -r requirements.txt

# EXPOSE 8080

# CMD python app.py
