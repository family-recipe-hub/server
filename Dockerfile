# Use the official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project files
COPY . .

# Expose the port
EXPOSE 8000

# Run Gunicorn as the entry point
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "family_recipe_hub.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]