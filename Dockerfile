FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default port for local development
ENV PORT=8000

# Make the script executable
RUN chmod +x /app/start.sh

# Use shell form to allow environment variable substitution
CMD /app/start.sh
