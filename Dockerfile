FROM python:3-slim

ADD client.py /

ENV server_url="tcp://10.0.28.221:5555"

RUN pip install pyzmq

CMD [ "python", "./client.py" ]

