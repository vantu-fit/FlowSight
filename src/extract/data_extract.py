import json
from src.utils.api_utils import encode_url_path, session, USE_SESSION_POOL
import requests

def extract_table_data(base_url, category, table_id):
    """Extract data from a table using category and table id"""
    path = f"{category}/{table_id}"
    url = base_url + encode_url_path(path)
    print(f"\nAttempting to extract data from: {url}")
    
    try:
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        metadata_response = session.get(url, headers=headers) if USE_SESSION_POOL else requests.get(url, headers=headers)
        if metadata_response.status_code != 200:
            print(f"Failed to get metadata. Status code: {metadata_response.status_code}")
            return None, None
            
        metadata = metadata_response.json()
        print("Successfully retrieved metadata!")
        
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
                
            data_response = session.post(url, json=query, headers=headers) if USE_SESSION_POOL else requests.post(url, json=query, headers=headers)
            print(f"Data response status: {data_response.status_code}")
            
            if data_response.status_code == 200:
                try:
                    content = data_response.content.decode('utf-8-sig')
                    result = json.loads(content)
                    print("Data retrieved successfully!")
                    return result, metadata
                except Exception as e:
                    print(f"Error parsing response: {e}")
                    return None, None
            else:
                print("Failed to get data:", data_response.text[:200])
                return None, None
        else:
            print("No variables found in metadata")
            return None, None
            
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None, None