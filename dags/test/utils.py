import requests
import urllib.parse
import logging
import os
import json
import pandas as pd
import logging

from test.config import province_mapping, year_mapping, industry_mapping

#------- API Utility Functions -------#
def encode_url_path(path):
    """Properly encode URL path components"""
    components = path.split('/')
    encoded = '/'.join(urllib.parse.quote(component) for component in components)
    return encoded

def inspect_api_response(base_url, path=""):
    """Print full details of API response to understand the structure"""
    url = base_url + encode_url_path(path)
    try:
        logging.info(f"Inspecting URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Success! Response contains {len(data)} items")
            return data
        else:
            logging.error(f"Failed with status code: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error: {e}")
        return None
    
#------- Data Processing Functions -------#
def save_to_csv(data_dict, folder_name="gso_data_csv"):
    """Save extracted data to CSV files in a folder"""
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            logging.info(f"Created folder {folder_name} to store CSV files")
        
        files_saved = 0
        for category, tables in data_dict.items():
            for table_name, df in tables.items():
                safe_table_name = ''.join(c for c in table_name if c.isalnum() or c in '_- ')
                safe_category = ''.join(c for c in category if c.isalnum() or c in '_- ')
                file_name = f"{safe_category}_{safe_table_name}.csv"
                file_path = os.path.join(folder_name, file_name)
                
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                files_saved += 1
                print(f"Saved data to {file_path}")
        
        if files_saved > 0:
            logging.info(f"\nTotal {files_saved} CSV files saved to folder: {os.path.abspath(folder_name)}")
        else:
            logging.info("No data to save")
        return files_saved
            
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return 0

def save_metadata_to_json(metadata, file_path):
    """Save metadata to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"Metadata saved to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving metadata to {file_path}: {e}")
        return False

def convert_data_to_dataframe(data, metadata=None):
    """Process data in different possible formats to pandas DataFrame with value mapping"""
    try:
        value_mappings = {}
        if metadata and "variables" in metadata:
            for variable in metadata["variables"]:
                if "code" in variable and "values" in variable and "valueTexts" in variable:
                    var_code = variable["code"]
                    value_mappings[var_code] = dict(zip(variable["values"], variable["valueTexts"]))
        
        if isinstance(data, dict) and "data" in data:
            logging.info("Converting standard API data format to DataFrame")
            rows = []
            for item in data.get("data", []):
                row = {}
                for i, key in enumerate(item.get("key", [])):
                    col_name = data.get("columns", [])[i].get("text", f"column_{i}")
                    
                    if col_name in value_mappings and key in value_mappings[col_name]:
                        row[col_name] = value_mappings[col_name][key]
                    elif col_name in ["Tỉnh, thành phố", "Địa phương", "Ðịa phương"] and key in province_mapping:
                        row[col_name] = province_mapping[key]
                    elif col_name == "Năm" and key in year_mapping:
                        row[col_name] = year_mapping[key]
                    elif col_name == "Ngành công nghiệp" and key in industry_mapping:
                        row[col_name] = industry_mapping[key]
                    else:
                        row[col_name] = key
                
                value = item.get("values", [None])[0]
                row["value"] = None if value == ".." else value
                rows.append(row)
                
            df = pd.DataFrame(rows)
            try:
                df["value"] = pd.to_numeric(df["value"], errors="coerce")
            except:
                pass
            return df
        else:
            logging.error("Unknown data format, couldn't convert")
            return None
    except Exception as e:
        logging.error(f"Error processing data: {e}")
        return None
    
def save_to_csv(df, file_path):
    logging.info(f"Saving data to {file_path}")
    logging.info(f"Example data: {df.head(3).to_string()}")
    if df is None:
        logging.error("No data to save")
    else:
        logging.info(f"Data type: {type(df)}")
        logging.info(f"Data shape: {df.shape}")
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        logging.info(f"Data saved to {file_path}")
    return True