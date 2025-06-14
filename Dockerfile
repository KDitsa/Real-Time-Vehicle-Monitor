FROM python:3.12
WORKDIR /app
COPY requirement.txt .
RUN pip install -r requirement.txt
COPY . .