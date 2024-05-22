# Use a specific version of the Python image as a base image
FROM python:3.11

# Set environment variables for Python and Django
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL development libraries and other dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install other dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . /app/

# Expose the port that Django runs on
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
