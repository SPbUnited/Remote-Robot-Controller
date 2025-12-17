FROM python:3.8-bullseye
# FROM balenalib/raspberrypi3-python:3-bookworm

WORKDIR /rcu

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies needed to build lgpio from source
# swig is essential for the Python bindings
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    swig \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install the Python lgpio library
# You can install it directly or via a requirements.txt file
RUN pip install lgpio 
# Note: rpi-lgpio is the PyPI package that uses the lgpio library


COPY . .

ENTRYPOINT ["/rcu/start.py"]
