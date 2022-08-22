FROM jenkins/jenkins
USER root
RUN apt-get update
RUN apt-get install -y python3-pip
COPY ./requeriments.txt .
RUN pip install -r requeriments.txt
