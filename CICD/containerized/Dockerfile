FROM bitnami/jenkins:2.440.2-debian-12-r0
USER root
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" 
RUN install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
RUN curl -LO https://get.helm.sh/helm-v3.11.2-linux-amd64.tar.gz -o helm-v3.11.2-linux-amd64.tar.gz 
RUN tar -zxvf helm-v3.11.2-linux-amd64.tar.gz && mv linux-amd64/helm /usr/local/bin/helm && chmod +x /usr/local/bin/helm
RUN apt-get update -y && apt-get install apt-transport-https ca-certificates gnupg curl -y 
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list 
RUN apt-get update && apt-get install google-cloud-cli -y
#RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get install google-cloud-sdk -y
RUN apt-get install google-cloud-sdk-gke-gcloud-auth-plugin -y
RUN mkdir /root/.ssh
ADD ssh_config /root/.ssh/config


