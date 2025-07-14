resource "aws_s3_bucket" "state_bucket_example" {
  bucket = "state-bucket-example"
}

resource "aws_s3_bucket_ownership_controls" "state_bucket_example" {
  bucket = aws_s3_bucket.state_bucket_example.bucket

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "state_bucket_example" {
  bucket = aws_s3_bucket.state_bucket_example.bucket

  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "state_lock_table" {
  name = "tofu-lambda-state-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
