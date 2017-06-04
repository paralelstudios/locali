variable "domain" {
  type    = "string"
  default = "locali-dev.com"
}

variable "domain_www" {
  type    = "string"
  default = "www.locali-dev.com"
}

variable "domain_api" {
  type    = "string"
  default = "api.locali-dev.com"
}

variable "access_key" {}
variable "secret_key" {}

variable "region" {
  default = "us-east-1"
}

provider "aws" {
  region     = "${var.region}"
  secret_key = "${var.secret_key}"
  access_key = "${var.access_key}"
}

resource "aws_s3_bucket" "locali" {
  bucket = "${var.domain}"
  acl    = "public-read"

  website {
    index_document = "index.html"
  }
}

resource "aws_s3_bucket" "locali_www" {
  bucket = "${var.domain_www}"
  acl    = "public-read"

  website {
    redirect_all_requests_to = "${var.domain}"
  }
}

resource "aws_s3_bucket" "match-resources" {
  bucket = "locali-resources-dev"
}
