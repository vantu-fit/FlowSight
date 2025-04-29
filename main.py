import time
import os

from src.extract.data_extract import extract_table_data
from src.extract.metadata_extract import extract_and_save_metadata
from src.transform.data_transform import process_data_to_dataframe
from src.transform.data_joiner import process_province_data
from src.utils.api_utils import inspect_api_response
from src.utils.file_utils import save_to_csv
from src.config.settings import BASE_URL, CATEGORIES, OUTPUT_BASE_PATH, MAX_TABLES_PER_CATEGORY
from concurrent.futures import ThreadPoolExecutor, as_completed


def extract_table_data_wrapper(args):
    base_url, category_dbid, table = args
    return table.get('text', 'Unknown'), extract_table_data(base_url, category_dbid, table['id'])

def join_province_data(output_dir=None, data_folder=None):
    """Join province data from CSV files in the output directory"""
    if output_dir is None:
        output_dir = OUTPUT_BASE_PATH
    
    if data_folder is None:
        import glob
        data_folders = glob.glob(os.path.join(output_dir, "gso_data_csv"))
        if data_folders:
            data_folder = max(data_folders)
        else:
            print("No data folders found in output directory")
            return None
    print(f"\n=== Joining Province Data ===")
    print(f"Source folder: {data_folder}")
    
    # Create output folder if it doesn't exist
    joined_data_dir = os.path.join(output_dir, "joined_data")
    os.makedirs(joined_data_dir, exist_ok=True)
    output_file = os.path.join(joined_data_dir, "joined_data.csv")
    
    # Process and join province data
    input_pattern = os.path.join(data_folder, "*.csv")
    joined_df = process_province_data(input_pattern, output_file)
    if joined_df is not None:
        print(f"\n=== Province Data Join Complete ===")
        print(f"Created joined dataset with {len(joined_df)} rows and {len(joined_df.columns)} columns")
        print(f"Saved to: {os.path.abspath(output_file)}")
        return joined_df
    else:
        print("\n=== Province Data Join Failed ===")
        return None


def main(include_data=True, include_metadata=True, join_provinces=False):
    """Main execution with options to include data and/or metadata"""
    
    if include_metadata:
        metadata_folder = os.path.join(OUTPUT_BASE_PATH, f"gso_metadata")
        metadata_info = extract_and_save_metadata(BASE_URL, CATEGORIES, metadata_folder)
    
    extracted_data = {}
    output_csv_folder = None
    batch_size = 10
    
    if include_data:
        from src.config.scraping_settings import ENABLE_PARALLEL, MAX_WORKERS
        output_csv_folder = os.path.join(OUTPUT_BASE_PATH, f"gso_data_csv")
        os.makedirs(output_csv_folder, exist_ok=True)
        
        for category in CATEGORIES:
            print(f"\n=== Processing Category: {category['text']} ===")
            category_data = {}
            subcategories = inspect_api_response(BASE_URL, category['dbid'])
            
            if not subcategories:
                continue
                
            tables = [item for item in subcategories if item.get("type") == "t"][:MAX_TABLES_PER_CATEGORY]
            
            if ENABLE_PARALLEL and len(tables) > 1:
                # Xử lý song song với batch saving
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    batch_count = 0
                    table_batch = []
                    futures = {}
                    
                    for table in tables:
                        batch_count += 1
                        table_batch.append(table)
                        
                        if batch_count >= batch_size or table == tables[-1]:
                            futures.clear()
                            for t in table_batch:
                                args = (BASE_URL, category['dbid'], t)
                                future = executor.submit(extract_table_data_wrapper, args)
                                futures[future] = t.get('text', 'Unknown')
                            
                            # Xử lý kết quả
                            for future in as_completed(futures):
                                table_name, (data, metadata) = future.result()
                                if data:
                                    df = process_data_to_dataframe(data, metadata)
                                    if df is not None and not df.empty:
                                        safe_table_name = table_name.replace('/', '_')
                                        category_data[safe_table_name] = df
                                        print(f"Successfully extracted data: {safe_table_name} ({len(df)} rows)")
                            
                            # Lưu batch hiện tại
                            if category_data:
                                save_to_csv({category['text']: category_data}, output_csv_folder)
                                print(f"Saved batch of {len(category_data)} tables to {output_csv_folder}")

                            batch_count = 0
                            table_batch = []
                            time.sleep(1)
            else:
                for table in tables:
                    print(f"\n--- Processing Table: {table.get('text')} ---")
                    data, metadata = extract_table_data(BASE_URL, category['dbid'], table['id'])
                    
                    if data:
                        df = process_data_to_dataframe(data, metadata)
                        
                        if df is not None and not df.empty:
                            table_name = table.get('text', 'Unknown').replace('/', '_')
                            category_data[table_name] = df
                    
                    time.sleep(0.5)
            
            extracted_data[category['text']] = category_data
        
        total_tables = sum(len(tables) for tables in extracted_data.values())
        total_rows = sum(sum(len(df) for df in tables.values()) for tables in extracted_data.values())
        print(f"\nTotal: {total_tables} tables with {total_rows} rows extracted")
    
    if join_provinces:
        if output_csv_folder:
            join_province_data(OUTPUT_BASE_PATH, output_csv_folder)
        else:
            join_province_data()
    
    print("\nProcess completed!")

if __name__ == "__main__":
    main(include_data=True, include_metadata=True, join_provinces=True)

    # join_province_data()