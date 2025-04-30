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
            filename = f"{new_col_name}.csv"  # Sử dụng tên cột mới làm tên file
            df.to_csv(os.path.join(output_dir, filename), index=False, encoding='utf-8-sig')
        return None
    return result


def split_population_by_gender(data_folder):
    target_file = "Dân số và lao động_Dân số trung bình phân theo địa phương giới tính và thành thị nông thôn.csv"
    file_path = os.path.join(data_folder, target_file)
    
    if not os.path.exists(file_path):
        print(f"Population data file not found: {file_path}")
        return
    
    print(f"Preprocessing population data file: {target_file}")
    
    df = pd.read_csv(file_path)
    
    expected_cols = ["Tỉnh, thành phố", "Dân số trung bình", "Năm", "value"]
    if not all(col in df.columns for col in expected_cols):
        print(f"Expected columns not found in {target_file}, skipping preprocessing")
        return

    category_mapping = {
        'Nam': 'Số nam giới',
        'Nữ': 'Số nữ giới'
    }
    
    split_table_by_category(
        df,
        category_col='Dân số trung bình',
        category_mapping=category_mapping,
        output_format='csv',
        output_dir=data_folder
    )

    os.remove(file_path)  
    print(f"Created two population data files:")
    print(f"- Male population: Số nam giới.csv")
    print(f"- Female population: Số nữ giới.csv")


def split_area_density_data(province_tables):
    processed_tables = {}
    target_table_name = "Dân số và lao động_Diện tích dân số và mật độ dân số phân theo địa phương.csv"

    if target_table_name not in province_tables:
        print(f"Target table '{target_table_name}' not found, skipping special handling")
        return province_tables

    # Lấy bảng nguồn
    source_df = province_tables[target_table_name].copy()
    
    if "Chỉ tiêu" not in source_df.columns:
        print(f"'Chỉ tiêu' column not found in {target_table_name}, skipping special handling")
        processed_tables[target_table_name] = source_df
        return processed_tables

    # Thêm các bảng khác trực tiếp
    for filename, df in province_tables.items():
        if filename != target_table_name:
            processed_tables[filename] = df
    
    print(f"Processing {target_table_name}...")

    # Bước 1: Điền giá trị thiếu trong cột 'value'
    print("Step 1: Filling missing values in 'value' column...")
    if source_df['value'].isna().any():
        mean_values = source_df.groupby(['province', 'Chỉ tiêu'])['value'].mean().reset_index()
        
        def impute_value(row):
            if pd.isna(row['value']):
                match = mean_values[
                    (mean_values['province'] == row['province']) &
                    (mean_values['Chỉ tiêu'] == row['Chỉ tiêu'])
                ]
                if not match.empty:
                    return match['value'].iloc[0]
            return row['value']
        
        source_df['value'] = source_df.apply(impute_value, axis=1)
        
        remaining_nans = source_df['value'].isna().sum()
        if remaining_nans > 0:
            print(f"Warning: {remaining_nans} missing values remain after imputation (no valid mean available)")
        else:
            print("All missing values in 'value' column successfully imputed")
    else:
        print("No missing values in 'value' column")

    # Bước 2: Lọc dữ liệu cho năm 2022
    print("\nStep 2: Filtering for year 2022...")
    source_df = source_df[source_df['Năm'] == 2022]
    if source_df.empty:
        print(f"No data found for year 2022 in {target_table_name}, skipping")
        return processed_tables
    print(f"Filtered to {len(source_df)} rows for year 2022")

    # Bước 3: Chia tách thành hai DataFrame
    print("\nStep 3: Splitting into separate DataFrames for 'Diện tích (Km2)' and 'Mật độ dân số (Người/km2)'...")
    
    # Định nghĩa ánh xạ danh mục
    category_mapping = {
        'Diện tích(Km2)': 'Diện tích (Km2)',
        'Mật độ dân số (Người/km2)': 'Mật độ dân số (Người/km2)'
    }
    
    # Sử dụng hàm tiện ích để chia tách
    split_result = split_table_by_category(
        source_df,
        category_col='Chỉ tiêu',
        category_mapping=category_mapping,
        output_format='dict'
    )
    
    # Thêm kết quả vào processed_tables với tên file phù hợp
    area_filename = f"{target_table_name}_Dien_tich_Km2.csv"
    density_filename = f"{target_table_name}_Mat_do_dan_so_Nguoi_km2.csv"
    
    processed_tables[area_filename] = split_result['Diện tích(Km2)']
    processed_tables[density_filename] = split_result['Mật độ dân số (Người/km2)']
    
    print(f"Created separate table for 'Diện tích (Km2)': {area_filename} with {len(split_result['Diện tích(Km2)'])} rows")
    print(f"Created separate table for 'Mật độ dân số (Người/km2)': {density_filename} with {len(split_result['Mật độ dân số (Người/km2)'])} rows")
    
    return processed_tables

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