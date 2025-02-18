FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache ffmpeg libsndfile && \
    pip install --no-cache-dir pipdeptree soundfile setuptools_rust

# RUN pip install -U openai-whisper==20240930

# Copy the requirements file
COPY requirements.txt .


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Expose the port
EXPOSE $PORT

# Command to run the application
CMD ["python", "src/app.py"]
