FROM python:3.10-slim-buster
ENV PYTHONUBUFFERED=1
WORKDIR /django

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt



# add directory for chromedriver
RUN apt-get update && apt-get install -y wget
ENV PATH="/usr/local/bin:$PATH"
RUN apt-get update && apt-get install -y unzip


# install ffmpeg to push audio files through websockets
RUN apt-get update && apt-get install -y ffmpeg


COPY . .


# add files in chromedriver folder
RUN wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin && \
    rm chromedriver_linux64.zip


