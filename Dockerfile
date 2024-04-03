# Use an official Python runtime as the base image
FROM python:3.9-slim-buster
LABEL maintainer "tuan t. pham" <tuan@vt.edu>

# Set environment variables for package installation
ENV PKGS="python3-pip" \
    DEBIAN_FRONTEND=noninteractive

# Update and upgrade packages, install required dependencies
RUN apt-get -yq update && apt-get -yq install --no-install-recommends ${PKGS} \
    && pip3 install --no-cache-dir flask pyserial

# Remove unnecessary packages to reduce image size
RUN apt-get autoremove -yq && apt-get autoclean && rm -rf /var/lib/apt/lists/*

# Create the necessary directory structure
RUN mkdir -p /opt/temper/bin

# Copy over your application files
COPY temper.py /opt/temper/bin
COPY temper-service.py /opt/temper/bin

# Change the working directory to /opt/temper/bin
WORKDIR /opt/temper/bin

# Expose port 2610 for the application
EXPOSE 2610

# Run the temper-service.py script as the entrypoint
ENTRYPOINT ["python3", "temper-service.py"]

# Add a healthcheck to ensure your application is running
HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD ["python3", "-c", "import flask; flask.Flask(__name__).run(port=2610)"] || exit 1
