# Use an official Python runtime as a parent image
FROM python:3.10

# Install dependencies for Chromium and Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libasound2 \
    libx11-xcb1 \
    libgbm1 \
    libgtk-3-0 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright and browsers
RUN pip install --upgrade pip playwright && playwright install-deps && playwright install

# Create and set the working directory
WORKDIR /usr/src/app

# Copy requirements file first, to leverage Docker layer caching if no changes
COPY req.txt .

# Upgrade pip and install dependencies from req.txt
RUN pip install -r req.txt

# Install additional Python packages
RUN pip install python-dotenv gunicorn

# Copy the rest of the application code into the container
COPY . .

# Create the static directory and set permissions
RUN mkdir -p /usr/src/app/static && chmod -R 755 /usr/src/app/static

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000

# Set default environment variables
ENV DEBUG=1
ENV DJANGO_SETTINGS_MODULE=web_changes_detector.settings
ENV DJANGO_SECRET_KEY=changeme

# Command to run Gunicorn and Celery
CMD ["python", "manage.py", "run_background_task"]
