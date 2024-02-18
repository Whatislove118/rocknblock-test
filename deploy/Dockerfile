FROM python:3.11 as base
ENV PYTHONUNBUFFERED=1
RUN apt install gcc -y
RUN apt-get update && apt-get install -y procps && apt install gettext -y
RUN apt install -y cron
RUN python -m pip install --upgrade pip setuptools

COPY requirements.txt /
RUN pip install -r requirements.txt 

RUN mkdir /app/
WORKDIR /app/

ADD src /app/

FROM base as api
COPY deploy/api/entrypoint.sh .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
