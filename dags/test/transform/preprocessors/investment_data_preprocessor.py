import os
import pandas as pd
import glob

def preprocess_fdi_data(data_folder):
    new_dataframes = {}
    
    # File patterns to look for
    file_patterns = [
        "Đầu tư_Đầu tư trực tiếp của nước ngoài được cấp giấy phép năm 2023 phân theo địa phương.csv",
        "Đầu tư_Đầu tư trực tiếp của nước ngoài được cấp giấy phép phân theo địa phương Lũy kế các dự án còn hiệu lực đến ngày 31_12_2023.csv"
    ]
    
    # Process each file if found
    for pattern in file_patterns:
        # Construct full path
        file_path = os.path.join(data_folder, pattern)
        
        # Skip if file doesn't exist
        if not os.path.exists(file_path):
            print(f"File not found: {pattern}")
            continue
        
        try:
            print(f"Processing FDI file: {pattern}")
            
            # Read the original file
            df = pd.read_csv(file_path)
            
            # Extract base name for creating new filenames
            base_name = os.path.splitext(pattern)[0]
            
            # Create separate dataframes for project count and investment amount
            project_count_df = df[df['Số dự án và tổng vốn đăng ký'] == 'Số dự án'].copy()
            investment_amount_df = df[df['Số dự án và tổng vốn đăng ký'].str.contains('Tổng vốn đăng ký')].copy()
            
            # Remove the extra column and rename value to be more descriptive
            if not project_count_df.empty:
                project_count_df = project_count_df.drop(columns=['Số dự án và tổng vốn đăng ký'])
                project_count_df = project_count_df.rename(columns={'value': 'Số dự án'})
                new_file_name = f"{base_name}_Số dự án.csv"
                new_dataframes[new_file_name] = project_count_df
                print(f"Created project count table with {len(project_count_df)} rows")
                
                # Save the file
                output_path = os.path.join(data_folder, new_file_name)
                project_count_df.to_csv(output_path, index=False)
                print(f"Saved to: {output_path}")
            
            if not investment_amount_df.empty:
                investment_amount_df = investment_amount_df.drop(columns=['Số dự án và tổng vốn đăng ký'])
                investment_amount_df = investment_amount_df.rename(columns={'value': 'Tổng vốn đăng ký'})
                new_file_name = f"{base_name}_Tổng vốn đăng ký.csv"
                new_dataframes[new_file_name] = investment_amount_df
                print(f"Created investment amount table with {len(investment_amount_df)} rows")
                
                # Save the file
                output_path = os.path.join(data_folder, new_file_name)
                investment_amount_df.to_csv(output_path, index=False)
                print(f"Saved to: {output_path}")
        
        except Exception as e:
            print(f"Error processing {pattern}: {e}")
    
    print(f"Created {len(new_dataframes)} new preprocessed FDI tables")
    return new_dataframes

def filter_joined_data(joined_df, min_non_nan_values=2):
    """
    Filter the joined DataFrame to remove rows with insufficient non-NaN values.
    Keeps only rows that have at least min_non_nan_values non-NaN values (not counting region and province)
    
    Args:
        joined_df: The joined DataFrame to filter
        min_non_nan_values: Minimum number of non-NaN values required to keep a row
        
    Returns:
        Filtered DataFrame
    """
    if joined_df is None or joined_df.empty:
        return joined_df
    
    print(f"\n=== Filtering joined data to remove rows with insufficient data ===")
    print(f"Before filtering: {len(joined_df)} rows")
    
    # Identify join columns (region, province)
    join_columns = ['region', 'province']
    join_cols_in_df = [col for col in join_columns if col in joined_df.columns]
    
    # Get value columns (non-join columns)
    value_columns = [col for col in joined_df.columns if col not in join_columns]
    
    if not value_columns:
        print("No value columns found in joined data")
        return joined_df
        
    # Count non-NaN values in each row
    non_nan_counts = joined_df[value_columns].notna().sum(axis=1)
    
    # Filter rows with at least min_non_nan_values non-NaN values
    filtered_df = joined_df[non_nan_counts >= min_non_nan_values]
    
    print(f"After filtering: {len(filtered_df)} rows")
    print(f"Removed {len(joined_df) - len(filtered_df)} rows with insufficient data")
    
    return filtered_df
