# syntax=docker/dockerfile:1

FROM python:3.10.6
WORKDIR /dcr/app
COPY requirements.txt /dcr/app/requirements.txt
RUN pip install -r requirements.txt

COPY .env /dcr/app/.env
COPY main.py /dcr/app/main.py

CMD ["python", "main.py"]
EXPOSE 3000

