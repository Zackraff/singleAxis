FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host", "0.0.0.0"]