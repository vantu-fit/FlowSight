# FlowSight Data Pipeline

This repository contains the infrastructure and workflow definitions for the FlowSight data processing pipeline. The pipeline automates the process of ingesting, cataloging, and analyzing data using AWS services (S3, Glue, Athena) and Apache Airflow.

## Data Architecture

![FlowSight Data Architecture](docs/images/data_architecture.png)

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform installed
- Docker and Docker Compose installed
- Python 3.x

## Environment Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/flowsight-pipeline.git
   cd flowsight-pipeline
   ```

2. Create a `.env` file in the root directory with your AWS and other account settings:

## Deployment Steps

### 1. Deploy AWS Infrastructure with Terraform

First, deploy the required AWS resources using Terraform:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

This will create:
- S3 buckets for data storage
- Glue crawler (gov-flowsight-crawler)
- AWS Glue Data Catalog for Athena querying

### 2. Start Airflow Using Docker Compose

Return to the root directory and start Airflow:

```bash
cd ..
docker compose up -d
```

### 3. Access Airflow UI

- Open your browser and navigate to: http://localhost:8080
- Log into Airflow using your credentials (defined in .env)

### 4. Configure AWS Connection in Airflow

1. In the Airflow UI, navigate to **Admin > Connections**
2. Click the "+" button to add a new connection
3. Create a connection with the following parameters:
   - Connection Id: `aws_default`
   - Connection Type: `Amazon Web Services`
   - AWS Access Key ID: Your AWS access key (or leave blank if using IAM roles)
   - AWS Secret Access Key: Your AWS secret key (or leave blank if using IAM roles)
   - Extra: `{"region_name": "your-aws-region"}`
4. Click "Save"

### 5. Trigger Data Pipeline

In the Airflow UI:
1. Navigate to DAGs
2. Find the `flowsight_dag` 
3. Trigger the DAG manually or configure it to run on a schedule

### 6. Run Glue Crawler

After data has been processed and landed in S3:

1. Go to the AWS Console
2. Navigate to AWS Glue
3. Trigger the Glue crawler named `gov-flowsight-crawler`

### 7. Query Data Using Athena

Once the crawler has updated the data catalog:

1. Go to Amazon Athena in the AWS Console
2. Create a workgroup if you haven't already
3. Configure the S3 output location for query results
4. Use the Glue Data Catalog to explore and query your data

### 8. Visualize Data with Amazon QuickSight

To create visualizations and dashboards with the processed data:

1. Log in to Amazon QuickSight console
2. Navigate to **Datasets** and choose **New dataset**
3. Select **S3** as the data source
4. Choose the `gov-flowsight-bucket` as your source bucket
5. Configure the data import settings:
   - Choose whether to use a manifest file or select data directly
   - Set appropriate permissions to allow QuickSight to access the S3 bucket
   - Configure the appropriate data format (CSV, JSON, etc.)
6. Finish the dataset creation and proceed to build visualizations or dashboards

## Troubleshooting

- **AWS Credentials**: Ensure your AWS credentials have the necessary permissions for S3, Glue, and Athena
- **Terraform Errors**: Check the error messages and ensure all required variables are set
- **Airflow Connection Issues**: Verify that the connections are properly configured in Airflow
