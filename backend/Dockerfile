FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install daphne psycopg2-binary channels channels-redis

# Copy project files
COPY . .

# Run entrypoint script or default command
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
