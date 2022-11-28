## VPC Definition
resource "aws_vpc" "trading_instance" {
  cidr_block = "172.16.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true
  tags = {
    Name = "trading-vpc"
  }
}

## VPC Subnet
resource "aws_subnet" "trading_instance" {
  vpc_id = aws_vpc.trading_instance.id
  cidr_block = "172.16.0.0/16"
  availability_zone = "us-east-1c"
}

## AWS Network Interface
resource "aws_network_interface" "trading_instance" {
  subnet_id = aws_subnet.trading_instance.id
  private_ips= ["172.16.10.100"]

  tags = {
    Name = "trading-NI"
  }
}

# Gateway to redirect internet traffic to our vpc
resource "aws_internet_gateway" "trading_instance" {
  vpc_id = "${aws_vpc.trading_instance.id}"
  tags = {
    Name= "trading_platform_gateway"
  }
}

resource "aws_route_table" "trading_instance" {
  vpc_id = aws_vpc.trading_instance.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.trading_instance.id
  }
}

resource "aws_route_table_association" "trading_instance" {
  subnet_id      = aws_subnet.trading_instance.id
  route_table_id = aws_route_table.trading_instance.id
}

# Security group creation
resource "aws_security_group" "trading_instance" {
  name = "trading_platform_sg"
  vpc_id = aws_vpc.trading_instance.id

#  ingress {
#    cidr_blocks = ["0.0.0.0/0"]
#    from_port = 22
#    to_port = 22
#    protocol = "tcp"
#  }

  egress {
   from_port = 0
   to_port = 0
   protocol = "-1"
   cidr_blocks = ["0.0.0.0/0"]
 }
}

## Security Group rules
resource "aws_security_group_rule" "trading_instance" {
  security_group_id = aws_security_group.trading_instance.id
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "trading_instance2" {
  security_group_id = aws_security_group.trading_instance.id
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "trading_instance3" {
  security_group_id = aws_security_group.trading_instance.id
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "trading_instance4" {
  security_group_id = aws_security_group.trading_instance.id
  type              = "ingress"
  from_port         = 8080
  to_port           = 8080
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}
## AWS EC2
resource "aws_instance" "trading_instance" {
  # Disk image id
  ami = "ami-0b0dcb5067f052a63"

  # Type of instance (free tier)
  instance_type = "t2.micro"

  #id of the public subnet so that the instance is accessible via internet to do SSH
  subnet_id = aws_subnet.trading_instance.id

  #id of the security group which has ports open to all the IPs
  vpc_security_group_ids=[aws_security_group.trading_instance.id]

  //assigning public IP to the instance is required.
  key_name = "emr-key-pair"
  associate_public_ip_address=true
    tags = {
       Name = "Trading Platform"
    }


  provisioner "remote-exec" {
        inline = [
            # System configuration
            # Autocredits :)
            "echo 'Work Done By Miguel Cozar, Master of Artificial Intelligence at IIT \n Work part of CSP 554 Final Project' > readme.txt",
            # System setup
            "sudo yum update -y",
            "sudo yum install -y docker",
            "sudo service docker start",
            "sudo systemctl enable docker",
            "sudo usermod -a -G docker ec2-user",
            "sudo yum install -y git",

            # Install docker compose
            "sudo curl -L \"https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)\"  -o /usr/local/bin/docker-compose",
            "sudo mv /usr/local/bin/docker-compose /usr/bin/docker-compose",
            "sudo chmod +x /usr/bin/docker-compose",

            # Repo cloning
            "git clone https://github.com/mcozar99/trading_platform",

            # We give permissions to the docker coordinators
            "chmod 777 trading_platform/data_collector/system_coordinator.sh",
            "chmod 777 trading_platform/visualization/system_coordinator.sh",

            # Build images
            "sudo chmod 777 /var/run/docker.sock",
            "mkdir streamcollector",
            "mv trading_platform/docker/DataGatherer streamcollector",
            "mv streamcollector/DataGatherer streamcollector/Dockerfile",
            "cd streamcollector",
            "docker build -t stream .",
            "cd ..",
            "mkdir visualization",
            "mv trading_platform/docker/Visualizer visualization",
            "mv visualization/Visualizer visualization/Dockerfile",
            "cd visualization",
            "docker build -t visualization .",
            "cd ..",

            # Docker compose initialization
            "mv trading_platform/docker/docker-compose.yml .",
            "docker-compose up"
        ]

        # Connection to be used by provisioner to perform remote executions
        connection {
            # Use public DNS of the instance to connect to it.
            host          = "${aws_instance.trading_instance.public_dns}"
            type          = "ssh"
            user          = "ec2-user"
            private_key   = "${file("emr-key-pair.pem")}"
            timeout       = "1m"
            agent         = false
        }
    }
}


