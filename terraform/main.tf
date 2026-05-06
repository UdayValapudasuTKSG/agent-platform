provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

# Enable APIs
resource "google_project_service" "aiplatform" {
  service = "aiplatform.googleapis.com"
}

resource "google_project_service" "cloudrun" {
  service = "run.googleapis.com"
}

resource "google_project_service" "secretmanager" {
  service = "secretmanager.googleapis.com"
}

# Staging Bucket for Reasoning Engine
resource "google_storage_bucket" "staging" {
  name          = "${var.project_id}-agent-staging"
  location      = var.region
  force_destroy = true
  uniform_bucket_level_access = true
}

# Secret Manager for storing Agent IDs
resource "google_secret_manager_secret" "agent_ids" {
  secret_id = "agent-platform-ids"
  replication {
    automatic = true
  }
}
