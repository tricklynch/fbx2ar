FROM plattar/python-xrutils:release-1.89.6

USER root

WORKDIR /usr/src/app

RUN mkdir static
RUN apt update -y
RUN apt install -y python3 python3-pip
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "./routes.py" ]
