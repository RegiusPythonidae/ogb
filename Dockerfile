FROM python:3.14-slim-bookworm

WORKDIR /app

COPY . .

RUN apt-get update && apt-get -y install gcc build-essential python3-dev
RUN pip install gunicorn
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--timeout", "200", "app:app"]