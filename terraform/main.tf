module "s3" {
  source      = "./modules/s3"
  bucket_name = var.bucket_name
}

module "glue" {
  source           = "./modules/glue"
  database_name    = var.glue_db_name
  crawler_name     = var.crawler_name
  s3_bucket        = module.s3.bucket_name
  crawler_schedule = null
  classifier_name = "csv_classifier"
}
