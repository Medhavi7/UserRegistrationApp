FROM python:3.10-slim

# Install build tools and libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    python3-dev \
    gcc \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install  -r requirements.txt

# Copy everything, including wait-for-db.sh
COPY . .

# Make the script executable
#RUN chmod +x /app/wait-for-db.sh

# Expose backend port
EXPOSE 8000

# Run init script then start FastAPI
#CMD ["sh", "-c", "./wait-for-db.sh db python create_tables.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
#CMD ["wait-for-db.sh" "db" "python" "create_tables.py" && "uvicorn main:app --host 0.0.0.0 --port 8000"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
