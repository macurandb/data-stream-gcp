resource "google_project_iam_member" "bigquery_to_gcs_permissions" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${var.bigquery_service_account}"
}

resource "google_project_iam_member" "cloud_function_permissions" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${var.cloud_function_service_account}"
}
