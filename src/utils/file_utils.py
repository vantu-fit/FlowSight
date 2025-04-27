import pandas as pd
import json
import os

def save_to_csv(data_dict, folder_name="gso_data_csv"):
    """Save extracted data to CSV files in a folder"""
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Created folder {folder_name} to store CSV files")
        
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
            print(f"\nTotal {files_saved} CSV files saved to folder: {os.path.abspath(folder_name)}")
        else:
            print("No data to save")
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