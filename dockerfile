FROM python:alpine3.16

# 换源
RUN sed -i 's/archive.ubuntu.com/mirrors.cqu.edu.cn/g' /etc/apt/sources.list \
    && apt update -y \
    && apt upgrade -y \
    && apt install vim -y \
    && apt install wget -y \
    && apt install python -y \
    && apt install python3-pip -y \
    && mkdir -p ~/.pip \
    && touch ~/.pip/pip.conf \
    && echo "[global]" >> ~/.pip/pip.conf \
    && echo "index-url = https://mirrors.cqu.edu.cn/pypi/web/simple" >> ~/.pip/pip.conf
    # && pip config set global.index-url https://mirrors.cqu.edu.cn/pypi/web/simple

# 安装依赖
RUN apt install git

VOLUME [ "/workspace" ]

EXPOSE 8888