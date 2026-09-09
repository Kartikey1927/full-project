terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# S3 Bucket for Prometheus & Chaos Backups
resource "aws_s3_bucket" "observability_storage" {
  bucket_prefix = "minikube-observability-backup-"
  force_destroy = true
}

# Restrict Public Access to S3
resource "aws_s3_bucket_public_access_block" "storage_privacy" {
  bucket                  = aws_s3_bucket.observability_storage.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Dedicated IAM User for Minikube Operations
resource "aws_iam_user" "minikube_sync_user" {
  name = "minikube-observability-sync"
}

# IAM Access Key for Authentication
resource "aws_iam_access_key" "minikube_key" {
  user = aws_iam_user.minikube_sync_user.name
}

# IAM Policy Document Data Source
data "aws_iam_policy_document" "s3_access" {
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.observability_storage.arn,
      "${aws_s3_bucket.observability_storage.arn}/*"
    ]
  }
}

# Attach Policy to IAM User
resource "aws_iam_user_policy" "s3_access_policy" {
  name   = "MinikubeS3SyncPolicy"
  user   = aws_iam_user.minikube_sync_user.name
  policy = data.aws_iam_policy_document.s3_access.json
}

output "s3_bucket_name" {
  value = aws_s3_bucket.observability_storage.id
}

output "aws_access_key_id" {
  value = aws_iam_access_key.minikube_key.id
}

output "aws_secret_access_key" {
  value     = aws_iam_access_key.minikube_key.secret
  sensitive = true
}
