FROM ubuntu:18.04

WORKDIR /opt

COPY . /opt

USER root

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update -y

RUN apt-get install -y wget \
                       build-essential \
                       software-properties-common \
                       apt-utils \
                       libgl1-mesa-glx \
                       ffmpeg \
                       libsm6 \
                       libxext6 \
                       libffi-dev \
                       libbz2-dev \
                       zlib1g-dev \
                       libreadline-gplv2-dev \
                       libncursesw5-dev \
                       libssl-dev \
                       libsqlite3-dev \
                       tk-dev \
                       libgdbm-dev \
                       libc6-dev \
                       liblzma-dev \
                       libc-dev





RUN wget  https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz
RUN tar -xzvf Python-3.8.3.tgz
RUN cd Python-3.8.3/ && ./configure --with-ensurepip=install && make && make install

RUN pip3 install --upgrade pip 
RUN pip3 install streamlit

#RUN apt-get-update
RUN pip3 install -r requirements.txt

RUN apt-get -y install locales && locale-gen en_US.UTF-8

ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8' 

EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]

CMD [ "/opt/Streamlit_ply_o3d_updated.py"]
