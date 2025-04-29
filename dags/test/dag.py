from airflow.decorators import dag
from airflow.utils.dates import days_ago
from test.constants import DEFAULT_DAG_ARGS, DEFAULT_SCHEDULE_INTERVAL, DEFAULT_CATCHUP

from test.config import BASE_URL, CATEGORIES, OUTPUT_BASE_PATH
from test.tasks import extract_caterogy, extract_table_data, convert_data_to_dataframe, save_to_csv

import logging
import os

@dag(
    default_args=DEFAULT_DAG_ARGS,
    schedule_interval=DEFAULT_SCHEDULE_INTERVAL,
    start_date=days_ago(1),
    catchup=DEFAULT_CATCHUP,
    max_active_runs=1,
    tags=["example"],
)
def my_dag():
    result = extract_caterogy(BASE_URL, CATEGORIES)
    logging.info(f"Extracted categories: {result}")
    extract_table_data.expand(map_dict=result)
dag = my_dag()