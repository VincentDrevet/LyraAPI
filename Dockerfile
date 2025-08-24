FROM python:3.12.7-alpine

ENV DATABASE_URL="sqlite:///Lyra.db"
ENV DEVICE_PASSWORD_SIZE=12

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD app .

ENTRYPOINT ["fastapi"]

CMD ["run"]

