import requests
import json
import os
import time
from datetime import datetime
from src.utils.api_utils import encode_url_path, inspect_api_response
from src.utils.file_utils import save_metadata_to_json

def extract_mapping_info(metadata):
    """Extract mapping information from metadata"""
    mapping_info = {}
    
    if "variables" in metadata:
        for variable in metadata["variables"]:
            if "code" in variable and "text" in variable:
                var_code = variable["code"]
                var_text = variable["text"]
                
                if "values" in variable and "valueTexts" in variable:
                    values = variable["values"]
                    value_texts = variable["valueTexts"]
                    sample_size = min(5, len(values))
                    mapping_info[var_code] = {
                        "text": var_text,
                        "mapping_sample": dict(zip(values[:sample_size], value_texts[:sample_size])),
                        "total_values": len(values)
                    }
                else:
                    mapping_info[var_code] = {
                        "text": var_text,
                        "mapping_sample": {},
                        "total_values": 0
                    }
    
    return mapping_info

def extract_and_save_metadata(base_url, categories, output_folder="gso_metadata"):
    """Extract and save metadata for all tables in selected categories"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder {output_folder} to store metadata")
    
    metadata_info = {}
    total_metadata_files = 0
    
    for category in categories:
        print(f"\n=== Extracting Metadata for Category: {category['text']} ===")
        category_folder = os.path.join(output_folder, category['text'].replace('/', '_'))
        
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
        
        subcategories = inspect_api_response(base_url, category['dbid'])
        
        if subcategories:
            tables = [item for item in subcategories if item.get("type") == "t"]
            print(f"Found {len(tables)} tables in category {category['text']}")
            
            category_metadata = {}
            
            for table in tables:
                table_id = table.get('id')
                table_name = table.get('text', 'Unknown')
                print(f"\n--- Extracting metadata for: {table_name} ---")
                
                path = f"{category['dbid']}/{table_id}"
                url = base_url + encode_url_path(path)
                
                try:
                    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
                    metadata_response = requests.get(url, headers=headers)
                    
                    if metadata_response.status_code == 200:
                        content = metadata_response.content.decode('utf-8-sig')
                        metadata = json.loads(content)
                        
                        safe_table_name = ''.join(c for c in table_name if c.isalnum() or c in '_- ')
                        metadata_file = os.path.join(category_folder, f"{safe_table_name}.json")
                        
                        save_metadata_to_json(metadata, metadata_file)
                        
                        mapping_info = extract_mapping_info(metadata)
                        category_metadata[table_name] = {
                            "id": table_id,
                            "updated": table.get("updated"),
                            "variables": len(metadata.get("variables", [])),
                            "mappings": mapping_info
                        }
                        
                        total_metadata_files += 1
                    else:
                        print(f"Failed to get metadata. Status code: {metadata_response.status_code}")
                
                except Exception as e:
                    print(f"Error: {e}")
                
                time.sleep(2)
            
            metadata_info[category['text']] = category_metadata
    
    summary_file = os.path.join(output_folder, "metadata_summary.json")
    save_metadata_to_json({
        "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categories": len(categories),
        "metadata_files": total_metadata_files,
        "metadata_info": metadata_info
    }, summary_file)
    
    print(f"\nTotal metadata files saved: {total_metadata_files}")
    print(f"Summary file saved to {os.path.abspath(summary_file)}")
    
    return metadata_info