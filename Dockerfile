FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt
RUN pip install mysql-connector-python

CMD ["python", "pytodo.py"]