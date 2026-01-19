variable "project_id" {
  description = "The ID of the Google Cloud project"
  type        = string
  default     = "streaming-project-483410"
}

variable "region" {
  description = "The region for the resources"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The zone for the resources"
  type        = string
  default     = "us-central1-a"
}

variable "bucket_name" {
  description = "The name of the GCS bucket"
  type        = string
  default     = "trinhducan-spark-483410"
}

variable "dataset_id" {
  description = "The ID of the BigQuery dataset"
  type        = string
  default     = "crypto_streaming_dataset"
}

variable "table_crypto_name" {
  description = "Table containing Coin price data"
  type        = string
  default     = "crypto_rates"
}
