FROM plattar/python-xrutils:latest

USER root

WORKDIR /usr/src/app

RUN apt update -y
RUN apt install -y python3 python3-pip
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "./routes.py" ]
