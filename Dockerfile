FROM ubuntu:22.04
LABEL org.opencontainers.image.source=https://github.com/petrutlucian94/mongo-webapp-sample

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip
RUN python3 -m pip install gunicorn

COPY ./mongo_webapp_sample ./mongo_webapp_sample
COPY ./pyproject.toml .
COPY ./requirements.txt .

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install .

EXPOSE 5000
ENTRYPOINT gunicorn -b 0.0.0.0:5000 -w 4 \
    'mongo_webapp_sample.cmd.api:register_app()'
