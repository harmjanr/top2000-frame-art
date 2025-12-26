ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install required system packages
RUN apk add --no-cache \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    rust \
    git \
    ttf-dejavu \
    fontconfig

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt && \
    python3 -c "from samsungtvws.async_art import SamsungTVAsyncArt; print('samsungtvws.async_art imported successfully')"

# Copy application files
COPY app.py .
COPY now_playing.py .
COPY track_cover.py .
COPY image_generator.py .
COPY samsung_frame_upload.py .
COPY run.sh .
COPY resources/ ./resources/

# Make run script executable
RUN chmod a+x run.sh

# Run the application
CMD [ "./run.sh" ]
