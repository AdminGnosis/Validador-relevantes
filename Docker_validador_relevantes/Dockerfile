FROM ubuntu:21.10

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

LABEL maintainer="Alexis G. Ariza "

RUN groupadd -r alexis && useradd -r -g alexis alexis
RUN chsh -s /usr/sbin/nologin root
RUN echo 'alexis:Teporingo271087' | chpasswd
RUN echo 'root:Teporingo271087' | chpasswd

RUN apt-get update
RUN apt-get install -y python3-pip
RUN echo "nameserver 192.168.0.1" > /etc/resolv.conf
RUN echo "search companydomain" >> /etc/resolv.conf

WORKDIR /ara
COPY . /ara

RUN pip3 install flask
RUN pip3 install pandas
RUN pip3 install openpyxl
RUN pip3 install lxml
RUN pip3 install requests
RUN pip3 install bs4
RUN pip3 install xlrd

ENV HOME /home/alexis

CMD python3 /ara/API_validador_relevantes/app.py
