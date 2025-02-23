# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the project into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including templates)
COPY . .

# Ensure the templates and static directories are correctly copied to the container
COPY app/templates /app/templates
COPY app/static /app/static

# Expose port 5000 (default for Flask)
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Run Flask app when the container starts
CMD ["flask", "run"]