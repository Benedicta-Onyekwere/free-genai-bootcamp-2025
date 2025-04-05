FROM python:3.10-slim

# Copy service files
COPY app /app
WORKDIR /app

# Install service requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run the service
CMD ["python", "chat.py"]