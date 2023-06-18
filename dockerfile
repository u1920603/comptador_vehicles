FROM python:3.8.16

WORKDIR /code

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get clean && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
      xcb \
      libglib2.0-0 \
      libgl1-mesa-glx && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

ENV QT_X11_NO_MITSHM=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/code"

RUN pip install --upgrade pip
COPY vehicle_counter/requirements.txt /code/
RUN pip install -r requirements.txt

COPY . ./code/

ENTRYPOINT [ "python", "main.py"]
