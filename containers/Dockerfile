FROM ubuntu:18.04

WORKDIR /opt

COPY . /opt

USER root

RUN apt-get update

#RUN apt-get install -y python3.8-dev python3-pip
RUN apt-get install -y python3-pip


RUN pip3 install --upgrade pip 

RUN pip3 install streamlit

RUN pip install -r requirements.txt

RUN apt-get -y  install wget

RUN apt-get -y install locales && locale-gen en_US.UTF-8

ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8' 

ENTRYPOINT ["streamlit", "run"]

CMD ["Streamlit_ply_o3d_updated.py"]
