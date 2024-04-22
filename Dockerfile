FROM python:3.10.0

WORKDIR /root/MonarchX

COPY . .

RUN pip3 install --upgrade pip setuptools

RUN pip3 install -U pip && pip3 install -U -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

RUN curl -sL https://deb.nodesource.com/setup_17.x | bash -

RUN apt-get install -y nodejs

CMD ["python3", "-m", "MonarchX"]
