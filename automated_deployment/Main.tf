terraform {
  required_version = ">= 0.12.24"
}

variable "aws_access_key" {
  type=string
  description = "Your AWS access key"
}

variable "aws_secret_key" {
  type=string
  description = "Your AWS secret key"
}

provider "aws" {
  region = "us-east-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

