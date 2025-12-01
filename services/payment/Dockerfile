# Base Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app/payment

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY ./app ./app

# Set the command to run the service
CMD ["python", "-m", "app.main"]
