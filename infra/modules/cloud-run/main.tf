resource "google_cloud_run_service" "cloud_run" {
  name     = var.cloud_run_name
  location = var.region
  project  = var.project_id

  template {
    spec {
      containers {
        image = var.image_uri

        env {
          name  = "BUCKET_NAME"
          value = var.gcs_bucket_name
        }

        env {
          name  = "FILE_NAME"
          value = var.file_name
        }
      }
    }
  }

  autogenerate_revision_name = true
}

resource "google_cloud_run_service_iam_member" "invoker" {
  service = google_cloud_run_service.cloud_run.name
  location = google_cloud_run_service.cloud_run.location
  role = "roles/run.invoker"
  member = "allUsers"
}
