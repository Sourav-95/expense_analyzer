import sys
import os
from src.ETL_manager import extract_transaction_data

input_file = r'/raw_file/915010018577756.csv'
input_file = os.getcwd()+input_file

# Example usage
df = extract_transaction_data(
    file_path=input_file, 
    header_identifier='Tran Date', 
    footer_identifier='Charge breakup'
    )
# Check if Data is comming or not
print(df.head())

