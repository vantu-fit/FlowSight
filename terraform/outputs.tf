output "s3_bucket" {
  value = module.s3.bucket_name
}

output "glue_database" {
  value = module.glue.glue_database_name
}

output "redshift_endpoint" {
  value = module.redshift.endpoint
}
