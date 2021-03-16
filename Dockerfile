FROM python:3

USER root

WORKDIR /usr/src/app

COPY --chown=myuser:myuser FBX2gltf ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN useradd -ms /bin/bash myuser && chown -R myuser /usr/src/app

USER myuser
CMD [ "python", "./routes.py" ]