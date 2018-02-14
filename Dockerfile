FROM python:3.6-slim

WORKDIR /htwbot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
