FROM python:3.11-slim

WORKDIR /app

# Install Node.js for frontend build
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy frontend source
COPY frontend ./frontend
WORKDIR /app/frontend
RUN npm ci && npm run build

# Copy backend source
WORKDIR /app
COPY backend ./backend

# Set working directory to backend for startup
WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
