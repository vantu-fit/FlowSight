import pandas as pd
import os


def split_table_by_category(df, category_col, category_mapping, output_format='dict', output_dir=None):
    result = {}
    for category, new_col_name in category_mapping.items():
        filtered_df = df[df[category_col] == category].copy()
        filtered_df = filtered_df.rename(columns={'value': new_col_name})
        result[category] = filtered_df
    if output_format == 'csv':
        if output_dir is None:
            raise ValueError("output_dir must be provided when output_format is 'csv'")
        for category, df in result.items():
            new_col_name = category_mapping[category]
            filename = f"{new_col_name}.csv"  
            df.to_csv(os.path.join(output_dir, filename), index=False, encoding='utf-8-sig')
        return None
    return result


def preprocess_and_split_data(
    data_folder,
    file_name,
    expected_cols,
    category_col,
    category_mapping,
    delete_original=True
):
    file_path = os.path.join(data_folder, file_name)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    print(f"Preprocessing file: {file_name}")
    
    df = pd.read_csv(file_path)
    
    if not all(col in df.columns for col in expected_cols):
        print(f"Expected columns not found in {file_name}, skipping preprocessing")
        return
    
    split_table_by_category(
        df,
        category_col=category_col,
        category_mapping=category_mapping,
        output_format='csv',
        output_dir=data_folder
    )
    
    if delete_original:
        os.remove(file_path)
    

def handle_special_tables(province_tables):
    """
    Process special cases:
    - For tables with "Dân số trung bình" column, keep only rows where it equals "Tổng số"
    - For tables with "Tỷ suất" column containing "Tỷ suất nhập cư" and "Tỷ suất di cư thuần",
      split into separate tables with renamed value columns
    """
    processed_tables = {}
    
    for filename, df in province_tables.items():
        if 'Dân số trung bình' in df.columns:
            if 'Tổng số' in df['Dân số trung bình'].values:
                df_filtered = df[df['Dân số trung bình'] == 'Tổng số'].copy()
                print(f"Filtered {filename} to keep only 'Tổng số' rows - {len(df_filtered)} rows remaining")
                processed_tables[filename] = df_filtered
            else:
                processed_tables[filename] = df.copy()
        
        elif 'Tỷ suất' in df.columns:
            if 'Tỷ suất nhập cư' in df['Tỷ suất'].values and 'Tỷ suất di cư thuần' in df['Tỷ suất'].values:
                df_immigration = df[df['Tỷ suất'] == 'Tỷ suất nhập cư'].copy()
                if not df_immigration.empty:
                    new_col_name = 'Tỷ suất nhập cư'
                    if 'value' in df_immigration.columns:
                        df_immigration = df_immigration.rename(columns={'value': new_col_name})
                    new_filename = filename.replace('.csv', '_nhap_cu.csv')
                    processed_tables[new_filename] = df_immigration
                    print(f"Created separate table for immigration rates: {new_filename}")
                
                df_net_migration = df[df['Tỷ suất'] == 'Tỷ suất di cư thuần'].copy()
                if not df_net_migration.empty:
                    new_col_name = 'Tỷ suất di cư thuần'
                    if 'value' in df_net_migration.columns:
                        df_net_migration = df_net_migration.rename(columns={'value': new_col_name})
                    new_filename = filename.replace('.csv', '_di_cu_thuan.csv')
                    processed_tables[new_filename] = df_net_migration
                    print(f"Created separate table for net migration rates: {new_filename}")
            else:
                processed_tables[filename] = df.copy()
        else:
            processed_tables[filename] = df.copy()
    
    return processed_tables