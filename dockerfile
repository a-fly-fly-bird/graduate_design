FROM python:3.9.16-buster

VOLUME [ "/workspace" ]

# 换源
RUN sed -i 's/archive.ubuntu.com/mirrors.cqu.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's/deb.debian.org/mirrors.cqu.edu.cn/g' /etc/apt/sources.list \
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

# 安装依赖
RUN apt install git -y \
    && apt install cmake -y \
    && git clone --depth 1 https://github.com/a-fly-fly-bird/graduate_design.git \
    && cd graduate_design \
    && pip install -r requirements.txt

EXPOSE 8888

WORKDIR /workspace/graduate_design/

CMD ["python3", "-m", "gaze_guy.kits.web_socket.server_flask"]
