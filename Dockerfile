FROM python:3.11-slim

WORKDIR /code

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 user
USER user

# Expose port
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]