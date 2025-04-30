import pandas as pd
from test.config import province_mapping, year_mapping, industry_mapping

def process_data_to_dataframe(data, metadata=None):
    """Process data in different possible formats to pandas DataFrame with value mapping"""
    try:
        value_mappings = {}
        if metadata and "variables" in metadata:
            for variable in metadata["variables"]:
                if "code" in variable and "values" in variable and "valueTexts" in variable:
                    var_code = variable["code"]
                    value_mappings[var_code] = dict(zip(variable["values"], variable["valueTexts"]))
        
        if isinstance(data, dict) and "data" in data:
            print("Converting standard API data format to DataFrame")
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
            print("Unknown data format, couldn't convert")
            return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None