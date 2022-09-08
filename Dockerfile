FROM python:3.9.6-slim-buster
WORKDIR /opt/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install git
RUN apt-get update --allow-releaseinfo-change && \
    apt-get update && \
    apt-get upgrade -y
RUN apt-get install -y git
# Install project requirements
COPY . /opt/app/
RUN pip install --upgrade pip
RUN cp sample.env .env
RUN chmod +x /opt/app/requirements.txt
RUN pip install -r requirements.txt



CMD exec /bin/sh -c "trap : TERM INT; (while true; do sleep 1000; done) & wait"