resource "google_storage_bucket" "bucket" {
  name     = var.gcs_bucket_name
  location = var.region
}
