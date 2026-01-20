variable "project_id" {
  description = "The ID of the Google Cloud project"
  type        = string
}

variable "region" {
  description = "The region for the resources"
  type        = string
}

variable "zone" {
  description = "The zone for the resources"
  type        = string
}

variable "bucket_name" {
  description = "The name of the GCS bucket"
  type        = string
}

variable "dataset_id" {
  description = "The ID of the BigQuery dataset"
  type        = string
}

variable "table_crypto_name" {
  description = "Table containing Coin price data"
  type        = string
}
