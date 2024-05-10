FROM ubuntu:14.04
RUN apt-get update -y \ 
    && apt-get install -y python-setuptools python3-pip
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt
ADD . /src
EXPOSE 5000
CMD ["python3", "/src/application.py"]
