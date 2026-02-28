FROM ubuntu:24.04

USER root

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl wget git neovim nano less \
    iproute2 iputils-ping net-tools dnsutils \
    build-essential \
    unzip zip \
    python3 python3-pip python3-venv \
    software-properties-common \
    openssh-client \
    tzdata locales && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
WORKDIR /root
CMD ["bash"]
