import csv
import os
import pandas as pd
import pdfplumber
from src.exception import CustomException
from src.inputs.column_structure import get_cols
from src.inputs import mapping

class DataIngestor():
    @classmethod
    def read_statement(cls, file_path, col_names):
        try:
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            file_ext = os.path.splitext(file_path)[-1].lower()                  # Determine the file extension
            

            # File reader
            if file_ext == '.csv':
                data = pd.read_csv(file_path, skiprows=20, names=col_names)
            elif file_ext == '.xlsx':
                data = pd.read_excel(file_path, skiprows=20, names=col_names)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}. Use only CSV or XLSX files")
            
            if data.empty:
                raise ValueError("The file is empty or the content couldn't be read correctly.")

            footer_index = data[data['Date'].apply(lambda x: len(str(x)) > 10)].index           # finding the footer index

            if not footer_index.empty:
                footer_index = footer_index[0]  
                data = data.iloc[:footer_index]  
            else:
                print(f"No footer found where 'Date' length is greater than 10. Proceeding without trimming footer.")
            data.reset_index(drop=True, inplace=True)
            return data
        
        except FileNotFoundError as fnf_error:
            print(f"Error: {fnf_error}")
        except pd.errors.ParserError as pe_error:
            print(f"Error parsing the file: {pe_error}")
        except KeyError as ke_error:
            print(f"Key error: {ke_error}")
        except ValueError as ve_error:
            print(f"Value error: {ve_error}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @classmethod
    def data_cleaner(cls, data: pd.DataFrame):
        if data.isnull().values.any():
            data = data.dropna(subset='Date', axis=0)
        if '*' in data:
            data = data[~data['Date'].astype(str).str.contains(r'\*', na=False)]
        if 'ChqNo' in data.columns:
            data = data.drop(columns='ChqNo', axis=1)
        
        return data
    
    @classmethod
    def clean_features(cls, data:pd.DataFrame, data_name:str):
        '''
            Step 1: This function removes the features which are not commonn in both the data's.
            Step 2: Next it calls "data_cleaner" function which removes null values, asteriks (*) & 
                    drop the feature 'Chqno'
        '''
        col_list1 = get_cols.col1()                 # Getting Column names of Statement 1 (Expense Account)
        col_list2 = get_cols.col2()                 # Getting Column names of Statement 2 (Salary Account)

        set1 = set(col_list1)
        set2 = set(col_list2)
        non_matching_col_names = set1.symmetric_difference(set2)
        
        try:
            if data_name == 'Expense':
                drop_colist_1 = [cols for cols in non_matching_col_names if cols in col_list1]
                data = data.drop(columns=drop_colist_1, axis=1)
            elif data_name == 'Salary':
                drop_colist_2 = [cols for cols in non_matching_col_names if cols in col_list2]
                data = data.drop(columns=drop_colist_2, axis=1)
        except CustomException as e:
            raise (f'Error occured as : \n {e}')

        data = DataIngestor.data_cleaner(data=data)
        return data

# class DataProcessor():
#     @classmethod
#     def remap_transactions(cls, data, transaction_col_name: str):
#         def extract_name(particulars):
#             if isinstance(particulars, str):  # Check if the value is a string
#                 parts = particulars.split('/')  # Split the string by '/'
#                 if len(parts) > 5:  # If there are more than 5 splits
#                     return f"{parts[3]} {parts[4]}"  # Return the 3rd and 4th parts
#                 else:
#                     try:
#                         return parts[3]  # Return only the 3rd part
#                     except IndexError:
#                         return particulars  # Return original if splitting fails
#             else:
#                 return particulars  # Return as is if it's None or NaN
#         # Apply the function to the specified column
#         data[transaction_col_name] = data[transaction_col_name].apply(extract_name)
#         return data

class DataProcessor():
    @classmethod
    def remap_transactions(cls, data, transaction_col_name: str):
        def extract_name(particulars):
            if isinstance(particulars, str):  # Check if the value is a string
                parts = particulars.split('/')  # Split the string by '/'
                if len(parts) > 5:  # If there are more than 5 splits
                    return f"{parts[3]} {parts[4]}"  # Return the 3rd and 4th parts
                else:
                    try:
                        return parts[3]  # Return only the 3rd part
                    except IndexError:
                        return particulars  # Return original if splitting fails
            else:
                return particulars  # Return as is if it's None or NaN

        def extract_last_word(particulars):
            if isinstance(particulars, str):
                last_word = particulars.split()[-1]  # Get the last part of the string
                # Return None if the last word is 'UPI', otherwise return the last word
                return None if last_word.lower() == 'upi' else last_word
            return None  # Return None for non-string values (e.g., NaN)

        # Apply the function to trim the PARTICULARS column
        data[transaction_col_name] = data[transaction_col_name].apply(extract_name)

        # Create a new column 'exp_name' with the last word or None if 'UPI'
        data['exp_name'] = data[transaction_col_name].apply(lambda x: extract_last_word(x))
        data[transaction_col_name] = data[transaction_col_name].str.replace('UPI', '', regex=False)
        data[transaction_col_name] = data[transaction_col_name].str.strip()

        # Reorder the columns to place 'exp_name' right after 'transaction_col_name'
        cols = list(data.columns)
        transaction_index = cols.index(transaction_col_name)
        # Insert 'exp_name' right after 'transaction_col_name'
        cols.insert(transaction_index + 1, cols.pop(cols.index('exp_name')))
        data = data[cols]

        return data
    
    # Create a reverse mapping function
    def map_expense_group(data):
        mapping_ = mapping.map_subcategory()
        def map_defined_expense(get_columns, mapping_dict):
            for group, records in mapping_dict.items():
                if get_columns in records:
                    return group
            return 'NA'  # Default group for unmapped records
        
        data['exp_group'] = data['exp_name'].apply(lambda x:map_defined_expense(x,mapping_dict=mapping_))


        if any(data['exp_group']=='NA'):
            data['exp_maps'] = data['Particulars'].apply(lambda x:map_defined_expense(x,mapping_dict=mapping_))

        #replace NA with actual NaN values
        data.replace('NA', pd.NA, inplace=True)
        data['exp_maps'] = data['exp_maps'].fillna(data['exp_group'])
        data = data.drop(columns = 'exp_group', axis=1)
        return data
        
