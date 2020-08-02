FROM python:3.8-alpine as base

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python src/alert_bot.py
