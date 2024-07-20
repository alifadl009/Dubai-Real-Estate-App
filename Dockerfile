FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libczmq-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    default-libmysqlclient-dev \
    apt-utils \
    python3-dev \
    python3-pip \
    git \
    wget \
    cron \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN chmod +x /app/run_scripts.sh

RUN echo "0 6 * * 0 /app/run_scripts.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron-job \
    && chmod 0644 /etc/cron.d/my-cron-job \
    && crontab /etc/cron.d/my-cron-job

RUN touch /var/log/cron.log

EXPOSE 8501

CMD cron && streamlit run main.py
# CMD streamlit run main.py
