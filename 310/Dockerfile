FROM python:3.10

RUN apt update && apt install -y \
    git \
    cmake \
    build-essential \
    libgl1-mesa-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-ttf-dev \
    libsdl2-gfx-dev \
    libboost-all-dev \
    libdirectfb-dev \
    libst-dev \
    mesa-utils \
    xvfb \
    x11vnc \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip setuptools psutil wheel six

WORKDIR /root
RUN git clone -b v2.9 https://github.com/google-research/football.git
WORKDIR /root/football
RUN python3 -m pip install .