FROM python:3
MAINTAINER Jan-Philippe Lavoie "janphilippelavoie@gmail.com"
COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
