resource "google_bigquery_data_transfer_config" "scheduled_query" {
  display_name        = "Scheduled Query Export"
  data_source_id      = "scheduled_query"
  destination_dataset_id = var.destination_dataset
  project             = var.project_id
  location            = var.region

  params {
    query = <<EOT
      SELECT * FROM `your_project.your_dataset.your_table`
      WHERE conditions;
    EOT
  }

  schedule = var.schedule
  disabled = false

  destination_bucket_uri          = var.gcs_bucket_uri
}
