import requests
import json
import logging 
import os

from test.utils import encode_url_path, inspect_api_response, convert_data_to_dataframe, save_to_csv
from test.config import MAX_TABLES_PER_CATEGORY, OUTPUT_BASE_PATH, BASE_URL
from test.transform.data_joiner import process_province_data

from airflow.decorators import task
from airflow.exceptions import AirflowException
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

import pandas as pd

@task
def extract_caterogy(base_url, caterogies, ti= None):
    """Extract categories from the API"""
    dbids = [category["dbid"] for category in caterogies]
    dbid_to_text = {category["dbid"]: category["text"] for category in caterogies}
    results = []
    for item in dbids:
        logging.info(f"Processing category: {item} ---")
        subcategories = inspect_api_response(base_url, item)
        if subcategories:
            tables = [item for item in subcategories if item.get("type") == "t"][:MAX_TABLES_PER_CATEGORY]
            logging.info(f"Found {len(tables)} tables in category {item}")
            results.extend([{"text": table.get("text"), "id": table.get("id"), "dbid": item, "dbid_text": dbid_to_text[item]} for table in tables])
    return results
    


@task
def extract_table_data(base_url=BASE_URL, map_dict=None, ti= None):
    if map_dict is None:
        raise AirflowException("No mapping dictionary provided")
    category = map_dict['dbid']
    table = map_dict['id']
    logging.info(f"Processing category: {category} ---")
    """Extract data from a table using category and table id"""
    path = f"{category}/{table}"
    url = base_url + encode_url_path(path)
    logging.info(f"\nAttempting to extract data from: {url}")
    
    try:
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        metadata_response = requests.get(url, headers=headers)
        if metadata_response.status_code != 200:
            logging.info(f"Failed to get metadata. Status code: {metadata_response.status_code}")
            return None, None
            
        metadata = metadata_response.json()
        logging.info("Successfully retrieved metadata!")
        
        if "variables" in metadata:
            query = {
                "query": [],
                "response": {"format": "json"}
            }
            
            for variable in metadata["variables"]:
                values = variable.get("values", [])
                query["query"].append({
                    "code": variable["code"],
                    "selection": {
                        "filter": "item" if values else "all",
                        "values": values if values else ["*"]
                    }
                })
                
            data_response = requests.post(url, json=query, headers=headers)
            logging.info(f"Data response status: {data_response.status_code}")
            
            if data_response.status_code == 200:
                try:
                    content = data_response.content.decode('utf-8-sig')
                    result = json.loads(content)
                    logging.info("Data retrieved successfully!")
                    df = convert_data_to_dataframe(result, metadata)
                    logging.info(f"Dataframe shape: {df.shape}")
                    logging.info(f"Dataframe head: {df.head(3).to_string()}")
                    table_name = map_dict.get('text', 'Unknown').replace('/', '_')
                    category_name = map_dict.get('dbid_text', 'Unknown').replace('/', '_')
                    safe_table_name = ''.join(c for c in table_name if c.isalnum() or c in '_- ')
                    safe_category = ''.join(c for c in category_name if c.isalnum() or c in '_- ')
                    file_name = f"{safe_category}_{safe_table_name}.csv"
                    file_path = os.path.join(OUTPUT_BASE_PATH, file_name)
                    logging.info(f"Saving data to {file_path}")
                    if save_to_csv(df, file_path):
                        logging.info(f"Data saved to {file_path}")
                        return True
                    else:
                        logging.error("Failed to save data")
                        raise AirflowException("Failed to save data")
                except Exception as e:
                    logging.error(f"Error parsing response: {e}")
                    raise AirflowException(f"Error parsing response: {e}")
            else:
                logging.error("Failed to get data:", data_response.text[:200])
                raise AirflowException(f"Failed to get data: {data_response.text[:200]}")
        else:
            logging.error("No variables found in metadata")
            raise AirflowException("No variables found in metadata")
            
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        raise AirflowException(f"Error extracting data: {e}")

@task
def join_table(output_dir, data_folder, ti=None):
    """Join all tables in the data directory into a single CSV file"""
    if output_dir is None:
        output_dir = OUTPUT_BASE_PATH
    
    if data_folder is None:
        import glob
        data_folders = glob.glob(os.path.join(output_dir, "gso_data_csv"))
        if data_folders:
            data_folder = max(data_folders)
        else:
            logging.info("No data folders found in output directory")
            return None
    logging.info(f"\n=== Joining Province Data ===")
    logging.info(f"Source folder: {data_folder}")
    
    # Create output folder if it doesn't exist
    joined_data_dir = os.path.join(output_dir, "joined_data")
    os.makedirs(joined_data_dir, exist_ok=True)
    output_file = os.path.join(joined_data_dir, "final.csv")
    
    # Process and join province data
    input_pattern = os.path.join(data_folder, "*.csv")
    joined_df = process_province_data(input_pattern, output_file)
    if joined_df is not None:
        logging.info(f"\n=== Province Data Join Complete ===")
        logging.info(f"Created joined dataset with {len(joined_df)} rows and {len(joined_df.columns)} columns")
        logging.info(f"Saved to: {os.path.abspath(output_file)}")
        joined_df.to_csv(output_file, index=False)
    else:
        logging.info("\n=== Province Data Join Failed ===")
        raise AirflowException("Failed to join province data")
    
@task 
def upload_to_s3(file_path, bucket_name, s3_key, conn_id='aws_default'):
    """Upload a file to S3"""
    hook = S3Hook(aws_conn_id=conn_id)
    hook.load_file(
        filename=file_path,
        bucket_name=bucket_name,
        key=s3_key,
        replace=True
    )
    logging.info(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    return f"s3://{bucket_name}/{s3_key}"