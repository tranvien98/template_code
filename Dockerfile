FROM python:3.10.16

WORKDIR /usr
USER root

RUN apt-get update
RUN apt-get install -y ffmpeg libsm6 libxext6
RUN apt install libmagic1 -y
RUN apt-get install -y virtualenv && \
    virtualenv --python=/usr/bin/python3 --system-site-packages uno_env && \
    uno_env/bin/pip install unoserver==2.1

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir --default-timeout=180 -r requirements.txt
COPY . .

CMD ["python", "main.py"]
