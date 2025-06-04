FROM python:3.12
WORKDIR /app
COPY required.txt .
RUN pip install -r required.txt
COPY . .