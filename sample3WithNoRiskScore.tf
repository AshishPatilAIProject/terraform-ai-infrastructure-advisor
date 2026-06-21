resource "aws_s3_bucket" "secure_bucket" {
bucket = "my-secure-demo-bucket"
}

resource "aws_s3_bucket_versioning" "secure_bucket" {
bucket = aws_s3_bucket.secure_bucket.id

versioning_configuration {
status = "Enabled"
}
}

resource "aws_s3_bucket_server_side_encryption_configuration" "secure_bucket" {
bucket = aws_s3_bucket.secure_bucket.id

rule {
apply_server_side_encryption_by_default {
sse_algorithm = "AES256"
}
}
}

resource "aws_s3_bucket_public_access_block" "secure_bucket" {
bucket = aws_s3_bucket.secure_bucket.id

block_public_acls       = true
block_public_policy     = true
ignore_public_acls      = true
restrict_public_buckets = true
}
