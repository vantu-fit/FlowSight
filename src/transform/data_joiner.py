import os
import pandas as pd
import numpy as np
import glob
import re
from src.transform.preprocessors.investment_data_preprocessor import preprocess_fdi_data, filter_joined_data
from src.transform.preprocessors.population_data_processor import handle_special_tables, preprocess_and_split_data
from src.config.mappings import (
    PROVINCE_TO_REGION_MAPPING, 
    AGGREGATES_TO_EXCLUDE, 
    PROVINCE_NAME_STANDARDIZATION,
    )
from src.transform.translator import translate_column_names


def load_csv_files(directory_pattern):
    """
    Load CSV files from a directory pattern
    Returns a dictionary with filenames as keys and DataFrames as values
    """
    csv_files = glob.glob(directory_pattern)
    data_dict = {}
    
    for file_path in csv_files:
        try:
            filename = os.path.basename(file_path)
            print(f"Loading {filename}...")
            df = pd.read_csv(file_path)
            data_dict[filename] = df
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return data_dict


def identify_province_tables(data_dict):
    province_tables = {}
    province_columns = ['Tỉnh, thành phố', 'Tỉnh/thành phố', 'Địa phương']
    
    for filename, df in data_dict.items():
        has_province_column = any(col in df.columns for col in province_columns)
        if has_province_column:
            province_tables[filename] = df
            print(f"Found province data in {filename}")
    
    return province_tables


def clean_province_tables(province_tables):
    cleaned_tables = {}
    province_to_region = PROVINCE_TO_REGION_MAPPING
    valid_provinces = set(province_to_region.keys())
    
    for filename, df in province_tables.items():
        print(f"Cleaning {filename}...")
        
        province_col = None
        province_columns = ['Tỉnh, thành phố', 'Ðịa phương', 'Tỉnh/thành phố', 'Tỉnh']
        for col in province_columns:
            if col in df.columns:
                province_col = col
                break
        if province_col is None:
            print(f"No province column found in {filename}, skipping...")
            continue
        
        df = df.rename(columns={province_col: 'province'})
        
        before_count = len(df)
        df = df[~df['province'].isin(AGGREGATES_TO_EXCLUDE)]
        df = standardize_province_names(df)
        df = df[df['province'].isin(valid_provinces)]
        
        after_count = len(df)
        print(f"Removed {before_count - after_count} records (aggregated areas and non-provinces) from {filename}")
        
        if 'region' not in df.columns and province_to_region:
            df['region'] = df['province'].map(province_to_region)
            print(f"Added region information to {filename}")
        cleaned_tables[filename] = df
    return cleaned_tables


def identify_year_column(df):
    year_columns = ['Năm', 'năm', 'Year', 'year']
    for col in year_columns:
        if col in df.columns:
            return col
    for col in df.columns:
        if 'năm' in col.lower() or 'year' in col.lower():
            return col
    return None


def normalize_column_names(df):
    df.columns = [re.sub(r'[^\w\s]', '', col).strip().replace(' ', '_').lower() for col in df.columns]
    replacements = {
        'tinh_thanh_pho': 'province',
        'dia_phuong': 'province',
        'tinh': 'province',
        'nam': 'year',
    }
    for old, new in replacements.items():
        if old in df.columns:
            df = df.rename(columns={old: new})
    return df


def filter_tables_by_year(province_tables, year_mapping):
    filtered_tables = {}
    
    for filename, df in province_tables.items():
        if filename in year_mapping:
            year_value = year_mapping[filename]
            year_col = identify_year_column(df)
            
            if year_col:
                df[year_col] = df[year_col].astype(str)
                filtered_df = df[df[year_col].str.contains(year_value)]
                
                if not filtered_df.empty:
                    filtered_tables[filename] = filtered_df
                    print(f"Filtered {filename} to year {year_value}: {len(filtered_df)} records")
                else:
                    print(f"No records found for year {year_value} in {filename}")
            else:
                filtered_tables[filename] = df
                print(f"No year column in {filename}, using all records")
        else:
            filtered_tables[filename] = df
            print(f"No year mapping for {filename}, using all records")
    
    return filtered_tables


def join_province_tables(tables_dict):
    """
    Join multiple tables on province column, ensures one row per province.
    Only join data from the latest common year across tables and removes year columns.
    
    Args:
        tables_dict: Dictionary of tables with filename as key and dataframe as value
        
    Returns:
        Joined dataframe with one row per province
    """
    if not tables_dict:
        return None
    
    processed_tables = {}
    for filename, df in tables_dict.items():
        df_copy = df.copy()
        
        year_col = identify_year_column(df_copy)
        
        if year_col:
            try:
                df_copy[year_col] = pd.to_numeric(df_copy[year_col], errors='coerce')
                df_copy = df_copy.sort_values(['province', year_col], ascending=[True, False])
            except:
                print(f"Could not convert year column in {filename} to numeric, using original values")
                df_copy = df_copy.sort_values(['province', year_col], ascending=[True, False])
            
            df_copy = df_copy.drop_duplicates(subset=['province'])
            
            if year_col in df_copy.columns:
                print(f"Dropping year column '{year_col}' from {filename}")
                df_copy = df_copy.drop(columns=[year_col])
        else:
            df_copy = df_copy.drop_duplicates(subset=['province'])
        
        processed_tables[filename] = df_copy
    
    all_provinces = set()
    for df in processed_tables.values():
        if 'province' in df.columns:
            all_provinces.update(df['province'].unique())
    
    if all_provinces:
        result_df = pd.DataFrame({'province': list(all_provinces)})
        print(f"Created base dataframe with {len(result_df)} unique provinces")
    else:
        print("No province data found in any table")
        return None
    
    sorted_tables = sorted(
        [(filename, df) for filename, df in processed_tables.items()],
        key=lambda x: len(x[1])
    )
    
    for i, (filename, df) in enumerate(sorted_tables):
        filename = os.path.basename(filename)
        
        join_cols = ['province']
        if 'region' in result_df.columns and 'region' in df.columns:
            join_cols.append('region')
        
        value_cols = [col for col in df.columns if col not in join_cols and col != 'year']
        
        if not value_cols:
            print(f"No value columns found in {filename}, skipping")
            continue
        
        print(f"Joining {filename} with value columns: {value_cols}")
        
        try:
            result_df = pd.merge(
                result_df, df[join_cols + value_cols], 
                on=join_cols, 
                how='outer'
            )
            print(f"Joined table now has {len(result_df)} rows and {len(result_df.columns)} columns")
        except Exception as e:
            print(f"Error joining {filename}: {e}")
            print("Skipping this table and continuing...")
        
        import gc
        gc.collect()
    
    if 'province' in result_df.columns:
        unique_provinces = result_df['province'].nunique()
        print(f"Final table contains {unique_provinces} unique provinces")
    
    return result_df


def process_province_data(input_directory_pattern, output_file=None):
    print(f"\n=== Processing province data from {input_directory_pattern} ===")
    data_folder = os.path.dirname(input_directory_pattern)

    preprocess_fdi_data(data_folder)
    preprocess_and_split_data(
    data_folder="output/gso_data_csv",
    file_name="Dân số và lao động_Dân số trung bình phân theo địa phương giới tính và thành thị nông thôn.csv",
    expected_cols=["Tỉnh, thành phố", "Dân số trung bình", "Năm", "value"],
    category_col="Dân số trung bình",
    category_mapping={
        'Nam': 'Số nam giới',
        'Nữ': 'Số nữ giới',
        'Thành thị': 'Số dân thành thị',
        'Nông thôn': 'Số dân nông thôn'
    })
    preprocess_and_split_data(
    data_folder="output/gso_data_csv",
    file_name="Dân số và lao động_Diện tích dân số và mật độ dân số phân theo địa phương.csv",
    expected_cols=["Địa phương", "Năm", "Chỉ tiêu", "value"],
    category_col="Chỉ tiêu",
    category_mapping={
        'Diện tích(Km2)': 'Diện tích(Km2)',
        'Mật độ dân số (Người/km2)': 'Mật độ dân số'
    })
    
    data_dict = load_csv_files(input_directory_pattern)
    print(f"Loaded {len(data_dict)} CSV files")
    if not data_dict:
        print("No data to process")
        return None
    
    province_tables = identify_province_tables(data_dict)
    print(f"Found {len(province_tables)} tables with province data")
    if not province_tables:
        print("No province tables found")
        return None

    cleaned_tables = clean_province_tables(province_tables)
    # special_tables = split_area_density_data(cleaned_tables)
    # processed_tables = handle_special_tables(cleaned_tables)
    renamed_tables = rename_value_columns(cleaned_tables)
    filtered_tables = filter_tables_by_specific_year(renamed_tables)
    if not filtered_tables:
        print("No suitable data found, cannot continue")
        return None
    
    joined_df = join_province_tables(filtered_tables)
    if joined_df is None:
        print("Failed to join province tables")
        return None
    
    joined_df = filter_joined_data(joined_df, min_non_nan_values=2)
    join_columns = ['region', 'province']
    value_columns = [col for col in joined_df.columns if col not in join_columns and col != 'year']
    
    final_columns = []
    for col in join_columns:
        if col in joined_df.columns:
            final_columns.append(col)
    
    final_df = joined_df[final_columns + value_columns]
    print(f"Final table has {len(final_df)} rows and {len(final_df.columns)} columns")

    if 'region' in final_df.columns and 'province' in final_df.columns:
        final_df = final_df.sort_values(by=['region', 'province'])
        print("Sorted final table by 'region' and 'province'")
    else:
        print("Could not sort: 'region' or 'province' column missing")
    
    if 'region' in final_df.columns:
        numeric_columns = final_df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_columns:
            if final_df[col].isna().any():  
                region_means = final_df.groupby('region')[col].mean().round(2)
                
                def impute_value(row):
                    if pd.isna(row[col]):
                        return region_means.get(row['region'], row[col])
                    return row[col]
                
                final_df[col] = final_df.apply(impute_value, axis=1)
                print(f"Imputed missing values in column '{col}' using region means")
        
        missing_values = final_df[numeric_columns].isna().sum().sum()
        if missing_values > 0:
            print(f"Warning: {missing_values} missing values remain after imputation (possibly in regions with all NaN values)")
        else:
            print("All missing values in numeric columns successfully imputed")
    else:
        print("Could not impute missing values: 'region' column missing")
    
    string_columns = final_df.select_dtypes(include=['object']).columns
    columns_to_drop = [col for col in string_columns if col not in ['region', 'province']]
    if columns_to_drop:
        final_df = final_df.drop(columns=columns_to_drop)
        print(f"Dropped string columns: {columns_to_drop}")
    else:
        print("No string columns to drop")
    print(f"Final table after dropping string columns has {len(final_df)} rows and {len(final_df.columns)} columns")
    
    final_df.columns = translate_column_names(final_df.columns)

    if output_file is None:
        output_file = "final_data.csv"
    print(f"\nSaving joined table to {output_file}...")
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved joined province data to {output_file}")
    
    return final_df


def standardize_province_names(df):
    """
    Standardize province names to match the official 63 provinces of Vietnam
    """
    if 'province' in df.columns:
        df['province'] = df['province'].replace(PROVINCE_NAME_STANDARDIZATION)
        df['province'] = df['province'].apply(lambda x: 'Thừa Thiên - Huế' 
                                            if isinstance(x, str) and 'Thừa Thiên' in x 
                                            else x)
        df['province'] = df['province'].apply(lambda x: 'Bà Rịa - Vũng Tàu' 
                                            if isinstance(x, str) and 'Bà Rịa' in x 
                                            else x)
    return df


def rename_value_columns(province_tables):
    """
    Rename 'value' columns in tables to match the table name
    """
    renamed_tables = {}
    
    for filename, df in province_tables.items():
        df_copy = df.copy()
        
        if 'value' in df_copy.columns:
            table_name = filename.split('_', 1)[1] if '_' in filename else filename
            table_name = table_name.replace('.csv', '')
            df_copy = df_copy.rename(columns={'value': table_name})
            print(f"Renamed 'value' column to '{table_name}' in {filename}")
        
        renamed_tables[filename] = df_copy
    
    return renamed_tables


def filter_tables_by_specific_year(province_tables):
    """
    Filter tables to include only those that have "2022" in their year column
    Remove tables that don't have this year
    
    Args:
        province_tables: Dictionary of dataframes
    
    Returns:
        Dictionary of filtered dataframes, only those with 2022 data
    """
    filtered_tables = {}
    target_years = ["2022"]
    
    for filename, df in province_tables.items():
        year_col = identify_year_column(df)
        
        if year_col:
            df[year_col] = df[year_col].astype(str)
            
            has_target_year = False
            for target_year in target_years:
                if df[df[year_col] == target_year].shape[0] > 0:
                    has_target_year = True
                    filtered_df = df[df[year_col] == target_year].copy()
                    filtered_tables[filename] = filtered_df
                    print(f"Filtered {filename} to year {target_year}: {len(filtered_df)} records")
                    break
            
            if not has_target_year:
                print(f"No suitable data found in {filename}, table excluded from joining")
        else:
            print(f"No year column in {filename}, unable to filter by year, table excluded")
    
    print(f"After filtering by year, {len(filtered_tables)} tables remain with 2022 data")
    return filtered_tables

