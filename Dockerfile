FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 8501
EXPOSE 8000

# Start Streamlit
CMD ["streamlit", "run", "streamlit/app.py", "--server.address=0.0.0.0"]