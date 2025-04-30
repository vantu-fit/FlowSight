resource "aws_glue_catalog_database" "this" {
  name = var.database_name
}

resource "aws_iam_role" "glue_role" {
  name = "glue-crawler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "glue.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "glue_policy" {
  name = "glue-crawler-policy"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # S3 Permissions
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${var.s3_bucket}",
          "arn:aws:s3:::${var.s3_bucket}/*",
        ]
      },
      # CloudWatch Logs Permissions
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = [
          "arn:aws:logs:ap-southeast-1:911167929350:log-group:/aws-glue/*"
        ]
      },
      # Glue Permissions (full access)
      {
        Effect = "Allow",
        Action = [
          "glue:*"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_glue_classifier" "csv_classifier" {
  name = var.classifier_name

  csv_classifier {
    allow_single_column = true
    contains_header     = "PRESENT" 
    delimiter           = ","
    quote_symbol        = "\""
  }
}

resource "aws_glue_crawler" "this" {
  name          = var.crawler_name
  role          = aws_iam_role.glue_role.arn
  database_name = aws_glue_catalog_database.this.name
  schedule      = var.crawler_schedule

  s3_target {
    path = "s3://${var.s3_bucket}/data/"
  }

  classifiers = [aws_glue_classifier.csv_classifier.name]
}