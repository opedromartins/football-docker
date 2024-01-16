FROM python:3.7

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
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda3/miniconda.sh && \
    bash /root/miniconda3/miniconda.sh -b -u -p /root/miniconda3
RUN echo 'export PATH="/root/miniconda3/bin:$PATH"' >> ~/.bashrc

WORKDIR /root

RUN . /root/.bashrc && \
    conda create -n gfootball python=3.7 -y && \
    conda init && \
    . /root/.bashrc && \
    conda activate gfootball && \
    conda install -c conda-forge boost gcc=11.4.0 -y && \
    pip install --upgrade pip setuptools psutil wheel six && \
    pip install gfootball

RUN . /root/.bashrc && \
    conda activate gfootball && \
    pip install tensorflow==1.15.* && \
    pip install dm-sonnet==1.* && \
    pip install git+https://github.com/openai/baselines.git@master && \
    pip install protobuf==3.20

RUN . /root/.bashrc && \
    conda activate gfootball && \
    pip install "ray[tune]==1.9.2" "ray[rllib]==1.9.2" gym==0.15.3

ENTRYPOINT ["/bin/bash"]