
#
# ------ Docker App ------
FROM ubuntu:18.04

LABEL maintainer="GMV BDA"

# Set environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Create a working directory
COPY  ./ /app/
WORKDIR /app/

# Install packages needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-pip \
    python3-tk \
    python3.6 \
    python3.6-dev \
    python3-setuptools \
    libsm6 \
    libxext6 \
    libxrender-dev \
    default-libmysqlclient-dev \
    openjdk-11-jre-headless && \
    rm -rf /var/lib/apt/lists/* && \
    # Install python requirements
    pip3 install --no-cache-dir -r requirements.txt &&

EXPOSE 5000

CMD python3.6 app/app.py metrics_filename=metrics/metrics_train.json --pkl_filename=models/model.pkl
