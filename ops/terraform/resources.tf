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

resource "aws_s3_bucket" "locali-resources" {
  bucket = "locali-resources-dev"
  acl    = "public-read"
}

resource "aws_iam_user" "locali" {
  name = "locali"
}

resource "aws_iam_access_key" "locali" {
  user    = "${aws_iam_user.locali.name}"
  pgp_key = "keybase:puhrez"
}

resource "aws_iam_user_policy" "locali" {
  name   = "locali-s3-policy"
  user   = "${aws_iam_user.locali.name}"
  policy = "${file("locali-s3-policy.json")}"
}

output "secret" {
  value = "${aws_iam_access_key.locali.encrypted_secret}"
}
