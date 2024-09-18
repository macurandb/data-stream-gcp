include {
  path = find_in_parent_folders()
}

terraform {
  source = "../../modules"
}

inputs = {
  project_id         = "your-dev-project-id"
  region             = "us-central1"
  gcs_bucket_name    = "your-dev-bucket"
  cloud_run_name     = "datastreamgcp-dev"
  file_name          = "data.parquet"
  image_uri          = "gcr.io/your-dev-project-id/datastreamgcp:latest"
  schedule           = "every 24 hours"
  service_account_email = "your-service-account@your-project.iam.gserviceaccount.com"
}
