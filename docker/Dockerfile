FROM python:3.11-slim

LABEL maintainer="GMV"
LABEL org.opencontainers.image.title="ai-service-ui"
LABEL org.opencontainers.image.description="Servicio de IA para proyecto INESADATA-MOV"
LABEL org.opencontainers.image.vendor="GMV"

# Install dependencies
RUN --mount=type=cache,id=apt-dev,target=/var/cache/apt \
    set -x \
    # && apt-get update && apt-get install -y --no-install-recommends \
    && apt-get update && apt-get install -y git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Allow build time variables via --build-arg
ARG PIP_URL

# System env vars
ENV USER_NAME=aiserviceui \
    APP_HOME=/ai_service_ui \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV PATH="$APP_HOME/venv/bin:$PATH"
ENV PYTHONPATH "${APP_HOME}:/"
WORKDIR $APP_HOME

# Install requirements
COPY requirements/requirements.txt requirements/requirements.txt
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    pip install --no-cache-dir pip==24.2 \
    && pip install --no-cache-dir -r requirements/requirements.txt

# Add our user and group first to make sure their IDs get assigned consistently
RUN groupadd -r ${USER_NAME} && useradd -r -m -g ${USER_NAME} ${USER_NAME}
RUN mkdir -p ${APP_HOME}/logs && chmod 777 ${APP_HOME}/logs

COPY --chown=${USER_NAME}:0 --chmod=755 .${APP_HOME} .

# User by default
USER ${USER_NAME}

# Define the port of the container
EXPOSE 80

CMD ["sh", "-c", "streamlit run run.py --server.address=0.0.0.0"]