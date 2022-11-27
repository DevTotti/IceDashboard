FROM python:3.10

COPY src/ app/
WORKDIR /app
COPY requirements.txt /app
COPY server.py /app
COPY .env /app

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

ENV PORT 5000

CMD ["python", "server.py"]