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

module "rust_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"
  version = "~> 7.20"

  function_name = "hello-world-api"

  handler = "bootstrap"
  runtime = "provided.al2023"
  architectures = ["arm64"]

  trigger_on_package_timestamp = false

  source_path = [
    {
      path = "${path.module}/../lambdas/hello-lambda"
      commands = [
        "cargo lambda build --release --arm64",
        "cd target/lambda/hello-lambda",
        ":zip",
      ],
      patterns = [
        "!.*",
        "bootstrap",
      ]
    }
  ]
  
  create_lambda_function_url = true
}

output "function_url" {
  value = module.rust_lambda_function.lambda_function_url
  description = "The URL of the Lambda function"
}