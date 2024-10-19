import csv
import os
import pandas as pd
import pdfplumber
from src.exception import CustomException
from src.inputs.column_structure import get_cols
from src.inputs import mapping
# from src.logger import logging
import logging

class DataIngestor():
    @classmethod
    def read_statement(cls, file_path, col_names):
        try:
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            logging.info(f'Determining the file extension')
            file_ext = os.path.splitext(file_path)[-1].lower()                  # Determine the file extension
            logging.info(f'File extension found: {file_ext}')

            # File reader
            if file_ext == '.csv':
                logging.info(f'Reading file.................')
                data = pd.read_csv(file_path, skiprows=20, names=col_names)
                
            elif file_ext == '.xlsx':
                logging.info(f'Reading file.................')
                data = pd.read_excel(file_path, skiprows=20, names=col_names)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}. Use only CSV or XLSX files")
            
            if data.empty:
                raise ValueError("The file is empty or the content couldn't be read correctly.")

            logging.info(f'Finding the footer index...............')
            footer_index = data[data['Date'].apply(lambda x: len(str(x)) > 10)].index           # finding the footer index

            if not footer_index.empty:
                footer_index = footer_index[0]  
                data = data.iloc[:footer_index]  
            else:
                logging.info(f"No footer found where 'Date' length is greater than 10. Proceeding without trimming footer.")
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
            logging.info(f'Null values found......Dropping the Null values......')
        if data['Date'].astype(str).str.contains(r'\*').any():
            data = data[~data['Date'].astype(str).str.contains(r'\*', na=False)]
            logging.info('* found in Date column... Dropping rows with *.')
        if 'ChqNo' in data.columns:
            data = data.drop(columns='ChqNo', axis=1)
            logging.info(f'Dropping the column CHQ No')
        
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
                logging.info(f'Dataset Name is - Expense, dropping the unmatched columns accordingly')
            elif data_name == 'Salary':
                drop_colist_2 = [cols for cols in non_matching_col_names if cols in col_list2]
                data = data.drop(columns=drop_colist_2, axis=1)
                logging.info(f'Dataset Name is - Salary, dropping the unmatched columns accordingly')
        except CustomException as e:
            raise (f'Dataset name is not defined. Error occured as : \n {e}')

        data = DataIngestor.data_cleaner(data=data)
        data[['Debit', 'Credit', 'Balance']] = data[['Debit', 'Credit', 'Balance']].apply(pd.to_numeric, errors='ignore')
        return data

class DataProcessor():
    @classmethod
    def remap_transactions(cls, data, transaction_col_name: str):
        def extract_name(particulars):
            if isinstance(particulars, str):  # Ensure the value is a string
                parts = particulars.split('/')  # Split by '/'
                if parts[-1] == '':  # Handle cases where the last part is empty
                    parts = parts[:-1]  # Remove the empty last part
                if len(parts) > 5:  # If there are more than 5 parts after adjustment
                    return f"{parts[3]} {parts[4]}"  # Return the 3rd and 4th parts
                elif len(parts) > 3:  # If there are 4 or 5 parts
                    return parts[3]  # Return only the 3rd part
                else:
                    return particulars.strip()  # Return original, stripping whitespace
            return particulars  # Return as is if it's None or NaN

        def extract_last_word(particulars):
            if isinstance(particulars, str):
                parts = particulars.split()  # Split by whitespace
                if parts:  # Check if there are any words
                    last_word = parts[-1]  # Get the last word
                    # Return None if the last word is 'UPI', otherwise return the last word
                    return None if last_word.lower() == 'upi' else last_word
            return None  # Return None for non-string or empty values

        logging.info(f'Remapping Transactions............')
        # Clean the 'transaction_col_name' column before applying transformations
        data[transaction_col_name] = data[transaction_col_name].fillna('').str.strip()

        # Apply the function to trim the PARTICULARS column
        data[transaction_col_name] = data[transaction_col_name].apply(extract_name)

        # Create a new column 'exp_name' with the last word or None if 'UPI'
        data['exp_name'] = data[transaction_col_name].apply(lambda x: extract_last_word(x))

        # Replace 'UPI' and strip whitespace in the 'transaction_col_name'
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
        logging.info(f'Grouping the Expenses according to the dictionary given')
        data['exp_group'] = data['exp_name'].apply(lambda x:map_defined_expense(x,mapping_dict=mapping_))


        if any(data['exp_group']=='NA'):
            data['exp_maps'] = data['Particulars'].apply(lambda x:map_defined_expense(x,mapping_dict=mapping_))

        #replace NA with actual NaN values
        data.replace('NA', pd.NA, inplace=True)
        data['exp_maps'] = data['exp_maps'].fillna(data['exp_group'])
        data = data.drop(columns = 'exp_group', axis=1)
        return data
    
    def __rearrange_cols__(data):
        # Get the list of columns
        cols = data.columns.tolist()

        # Move the 7th column (index 6) to the 4th position (index 3)
        cols.insert(3, cols.pop(6))

        # Reorder the dataframe
        data = data[cols]

        return data
        
