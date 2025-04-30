# import os
# import pandas as pd
# from groq import Groq
# import json
# from dotenv import load_dotenv

# def translate_column_names(df):
#     """
#     Translate column names from Vietnamese to English using Groq API with Meta Llama 4 model
#     Also adds unit annotations to column names based on data samples
    
#     Args:
#         df: DataFrame with Vietnamese column names
#         api_key: Optional Groq API key (if not provided, will attempt to load from environment)
        
#     Returns:
#         DataFrame with translated column names
#     """
#     if df is None or df.empty:
#         print("No data to translate")
#         return df
    
#     load_dotenv()
#     api_key = os.environ.get("GROQ_API_KEY")
    
#     if not api_key:
#         print("Warning: GROQ_API_KEY not found. Column names will not be translated.")
#         return df
    
#     try:
#         client = Groq(api_key=api_key)

#         sample_rows = df.head(2).to_dict(orient='records')
#         sample_json = json.dumps(sample_rows, ensure_ascii=False, indent=2)
        
#         current_cols = list(df.columns)
#         print(f"Translating {len(current_cols)} column names from Vietnamese to English...")
        
#         prompt = f"""Please translate these Vietnamese column names to English and add appropriate unit annotations:

# Column names: {current_cols}

# Here are two sample rows to help you understand the data type and units:
# {sample_json}

# For columns containing measurements, add appropriate units in parentheses. For example:
# - Area should include (km²) 
# - Money values should include (VND)
# - Percentages should include (%)
# - Population should be (people)
# - Density should be (people/km²)

# Ensure the English column names are short and concise, avoiding overly verbose terms.

# Return ONLY a JSON dictionary mapping each original Vietnamese column name to its English translation with units where applicable.
# Do not include any explanations, just the JSON dictionary.
# """

#         response = client.chat.completions.create(
#             model="meta-llama/llama-4-scout-17b-16e-instruct",
#             messages=[
#                 {"role": "system", "content": "You are a data specialist helping translate Vietnamese column names to English for a data analysis project. Your translations should be professional and include units where applicable."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.1,
#             max_tokens=1000
#         )
        
#         translation_text = response.choices[0].message.content
        
#         # Extract JSON from the response
#         translation_text = translation_text.strip()
#         if translation_text.startswith("```json"):
#             translation_text = translation_text.replace("```json", "").replace("```", "")
#         elif translation_text.startswith("```"):
#             translation_text = translation_text.replace("```", "")
            
#         try:
#             translation_dict = json.loads(translation_text)
            
#             # Rename columns using the translation dictionary
#             renamed_df = df.rename(columns=translation_dict)
            
#             # Print translation results
#             print("\nColumn translations:")
#             for old, new in translation_dict.items():
#                 print(f"  {old} -> {new}")
                
#             print(f"\nRenamed {len(translation_dict)} columns successfully")
#             return renamed_df
            
#         except json.JSONDecodeError as e:
#             print(f"Error parsing translation response: {e}")
#             print("Translation response:", translation_text)
#             return df
            
#     except Exception as e:
#         print(f"Error translating column names: {e}")
#         return df