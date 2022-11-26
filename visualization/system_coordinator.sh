### Define all the commands to configure our EC2 instance and put it to work
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
sudo yum install git

# Repo downloading
git clone https://github.com/mcozar99/trading_platform

# Stream collector implementation
mkdir streamcollector
mv trading_platform/docker/DataGatherer streamcollector
mv streamcollector/DataGatherer streamcollector/Dockerfile
cd streamcollector