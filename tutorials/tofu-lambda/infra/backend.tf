terraform {
  backend "s3" {
    region       = "eu-central-1"
    key          = "terraform.tfstate"
    bucket       = "tofu-lambda-state-bucket-example"
    use_lockfile = true
  }
}
