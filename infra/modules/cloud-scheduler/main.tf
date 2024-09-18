resource "google_cloud_scheduler_job" "job" {
  name        = "invoke-cloud-run"
  schedule    = "0 0 * * *"  # Every day at midnight
  time_zone   = "UTC"

  http_target {
    uri         = google_cloud_run_service.cloud_run.status[0].url
    http_method = "POST"
    oidc_token {
      service_account_email = var.service_account_email
    }
  }
}
