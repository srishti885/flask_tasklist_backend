FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
