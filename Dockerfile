FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make start script executable
RUN chmod +x start.sh

# Default port
ENV PORT=10000
EXPOSE ${PORT}

# Use start script
CMD ["./start.sh"]
