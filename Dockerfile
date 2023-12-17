# Use an official Ubuntu runtime as the base image
FROM ubuntu:22.04
LABEL maintainer "tuan t. pham" <tuan@vt.edu>

# Set environment variables for package installation
ENV PKGS="python3 python3-pip" \
    DEBIAN_FRONTEND=noninteractive

# Update and upgrade packages, install required dependencies, and pip packages
RUN apt-get -yq update && apt-get dist-upgrade -yq \
    && apt-get -yq install --no-install-recommends ${PKGS} \
    && pip3 install flask pyserial

# Remove unnecessary files to reduce image size
RUN apt-get autoremove -yq \
    && apt-get autoclean \
    && rm -fr /tmp/* /var/lib/apt/lists/*

RUN mkdir -p /opt/temper/bin

COPY temper.py /opt/temper/bin
COPY temper-service.py /opt/temper/bin

# Change the working directory to /opt/temper/bin
WORKDIR /opt/temper/bin

# Expose port 2610 for the application
EXPOSE 2610

# Run the temper-service.py script as the entrypoint
ENTRYPOINT ["python3", "temper-service.py"]
