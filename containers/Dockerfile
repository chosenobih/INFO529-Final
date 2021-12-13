FROM ubuntu:18.04

WORKDIR /opt

COPY . /opt

USER root


RUN apt-get update

#RUN apt-get install -y python3.8-dev /

RUN apt-get install -y  python3-pip


COPY requirements.txt requirements.txt

COPY Streamlit_ply_o3d_updated.py Streamlit_ply_o3d_updated.py

COPY . .

RUN pip3 install --upgrade pip 

RUN pip3 install streamlit

RUN apt-get -y install wget
RUN apt-get -y install zlib1g-dev
RUN wget  https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz

RUN tar -xzvf Python-3.8.3.tgz

RUN cd Python-3.8.3/ && ./configure --with-ensurepip=install && make && make install

RUN pip install -r requirements.txt

EXPOSE 8501

RUN apt-get -y install locales && locale-gen en_US.UTF-8

ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8' 

ENTRYPOINT ["streamlit", "run"]

CMD ["Streamlit_ply_o3d_updated.py"]
