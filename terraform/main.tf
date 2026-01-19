terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.19.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# API Dataproc
resource "google_project_service" "dataproc_api" {
  service            = "dataproc.googleapis.com"
  disable_on_destroy = false
}

resource "google_storage_bucket" "streaming_project_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = var.dataset_id
  location                    = var.region
  delete_contents_on_destroy  = true 
}

resource "google_bigquery_table" "crypto_rates" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = var.table_crypto_name
  deletion_protection = false  # <--- Dòng này cực quan trọng để fix lỗi Terraform

  schema = <<EOF
[
  { "name": "symbol", "type": "STRING", "mode": "NULLABLE" },
  { "name": "priceUsd", "type": "FLOAT", "mode": "NULLABLE" },
  { "name": "timestamp", "type": "TIMESTAMP", "mode": "NULLABLE" }
]
EOF
}