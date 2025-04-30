from datetime import timedelta

# ─────────────────────────────────────────────────────────────────────
# Global DAG Defaults
# ─────────────────────────────────────────────────────────────────────

DEFAULT_DAG_ARGS = {
    'owner': 'minhkhoi',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=0, seconds=30),
}

DEFAULT_SCHEDULE_INTERVAL = "@daily"
DEFAULT_CATCHUP = False
DEFAULT_MAX_ACTIVE_RUNS = 1

# ─────────────────────────────────────────────────────────────────────
# Connection IDs
# ─────────────────────────────────────────────────────────────────────

S3_CONN_ID = "aws_default"

# ─────────────────────────────────────────────────────────────────────
# S3/Cloud Storage Config
# ─────────────────────────────────────────────────────────────────────

S3_BUCKET_NAME = "my-airflow-bucket"
S3_DATA_FOLDER = "data/"

# ─────────────────────────────────────────────────────────────────────
# Email Settings
# ─────────────────────────────────────────────────────────────────────

ALERT_EMAILS = ["pnmk0811@gmail.com"]