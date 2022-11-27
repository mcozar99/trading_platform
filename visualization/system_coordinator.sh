# All the commands for the set up are installed in
# Visualization implementation
mkdir visualization
mv trading_platform/docker/Visualizer visualization
mv visualization/Visualizer visualization/Dockerfile
cd visualization

# Docker Image Built
sudo chmod 777 /var/run/docker.sock
docker build -t visualization .
docker run -t -i -p 5000:5000 visualization

