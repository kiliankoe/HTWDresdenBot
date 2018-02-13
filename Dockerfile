FROM python:3.6-slim

WORKDIR /htwbot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY htwdresden .
COPY htwdresden_bot .

CMD ["python", "main.py"]
