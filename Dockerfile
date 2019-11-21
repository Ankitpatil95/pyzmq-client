FROM python:3-slim

COPY . /

ENV server_url="tcp://10.0.28.216:5555"
ENV FLASK_APP="client.py"

# install dependencies
RUN pip install -r requirements.txt --no-cache-dir


CMD [ "flask", "run" ]

