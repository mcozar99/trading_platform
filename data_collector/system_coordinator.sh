# Stream collector implementation
mkdir streamcollector
mv trading_platform/docker/DataGatherer streamcollector
mv streamcollector/DataGatherer streamcollector/Dockerfile
cd streamcollector

# Docker Image Built
sudo chmod 777 /var/run/docker.sock
docker build -t stream .
docker run -t -i -p 80:80 stream