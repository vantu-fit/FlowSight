from datetime import datetime
import time
import os
from src.extract.data_extract import extract_table_data
from src.extract.metadata_extract import extract_and_save_metadata
from src.transform.data_transform import process_data_to_dataframe
from src.utils.api_utils import inspect_api_response
from src.utils.file_utils import save_to_csv
from src.config.settings import BASE_URL, CATEGORIES, OUTPUT_BASE_PATH, MAX_TABLES_PER_CATEGORY

def main(include_data=True, include_metadata=True):
    """Main execution with options to include data and/or metadata"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if include_metadata:
        metadata_folder = os.path.join(OUTPUT_BASE_PATH, f"gso_metadata_{timestamp}")
        metadata_info = extract_and_save_metadata(BASE_URL, CATEGORIES, metadata_folder)
    
    if include_data:
        extracted_data = {}
        
        for category in CATEGORIES:
            print(f"\n=== Processing Category: {category['text']} ===")
            category_data = {}
            
            subcategories = inspect_api_response(BASE_URL, category['dbid'])
            
            if subcategories:
                tables = [item for item in subcategories if item.get("type") == "t"][:MAX_TABLES_PER_CATEGORY]
                
                for table in tables:
                    print(f"\n--- Processing Table: {table.get('text')} ---")
                    
                    data, metadata = extract_table_data(BASE_URL, category['dbid'], table['id'])
                    
                    if data:
                        df = process_data_to_dataframe(data, metadata)
                        
                        if df is not None and not df.empty:
                            table_name = table.get('text', 'Unknown').replace('/', '_')
                            category_data[table_name] = df
                            print(f"Successfully extracted data: {len(df)} rows")
                            print("Sample data:")
                            print(df.head(3).to_string())
                    
                    time.sleep(3)
            
            extracted_data[category['text']] = category_data
        
        output_csv_folder = os.path.join(OUTPUT_BASE_PATH, f"gso_data_csv_{timestamp}")
        
        if any(tables for tables in extracted_data.values()):
            save_to_csv(extracted_data, output_csv_folder)
        else:
            print("No data was extracted to save")
        
        total_tables = 0
        total_rows = 0
        for category, tables in extracted_data.items():
            category_tables = len(tables)
            category_rows = sum(len(df) for df in tables.values())
            total_tables += category_tables
            total_rows += category_rows
            print(f"Category '{category}': {category_tables} tables, {category_rows} rows")
        
        print(f"\nTotal: {total_tables} tables with {total_rows} rows extracted")
    
    print("\nProcess completed!")

if __name__ == "__main__":
    main(include_data=True, include_metadata=True)