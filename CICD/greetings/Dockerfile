FROM ubuntu:14.04
RUN apt-get update -y \ 
    && apt-get install -y python-setuptools python-pip python-mysqldb
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt
ADD . /src
EXPOSE 5000
CMD ["python", "/src/application.py"]
