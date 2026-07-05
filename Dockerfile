# Use official Python image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install dependencies
# RUN pip install django
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Expose port
EXPOSE 8010

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8010"]