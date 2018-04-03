1) Apache on CentOS

docker build -t testcentos -f Dockerfile.centos-apache .

docker run -d -p 8085:80 testcentos

docker ps

curl localhost:8085

docker logs <container-id>




