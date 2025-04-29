variable "database_name" {}
variable "crawler_name" {}
variable "s3_bucket" {}
variable "crawler_schedule" {}
variable "classifier_name" {
    default = "csv_classifier"
}