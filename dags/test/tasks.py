import requests
import json
import logging 
import os

from test.utils import encode_url_path, inspect_api_response, convert_data_to_dataframe, save_to_csv
from test.config import MAX_TABLES_PER_CATEGORY, OUTPUT_BASE_PATH, BASE_URL

from airflow.decorators import task
from airflow.exceptions import AirflowException

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
    