FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy all files
COPY . /app

# Install OS-level dependencies for Playwright (and some general purpose tools)
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip fonts-liberation libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils libgbm1 \
    libgtk-3-0 libxshmfence1 libxss1 libxext6 libxfixes3 libx11-6 \
    libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 \
    iputils-ping \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip & install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install TikTokApi

# Install Playwright and its browser binaries
RUN python -m playwright install --with-deps

# Expose port
EXPOSE 8001

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
