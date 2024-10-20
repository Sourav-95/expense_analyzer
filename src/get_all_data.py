import pandas as pd
import warnings
from src.logger import logging
from src.inputs.column_structure import get_cols
from src.data_transformer import DataTransformer
from src.ETL_manager import DataProcessor
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def get_data(no_of_file:int):
    DataTransformer_Account_1 = DataTransformer(input_file='/raw_file/expense_statement.csv',
                                    col_name=get_cols.col1(),
                                    data_name='Expense',
                                    transaction_col_name='Particulars'
                                    )
    DataTransformer_Account_2 = DataTransformer(input_file='/raw_file/hdfc_statement_c.csv',
                                    col_name=get_cols.col2(),
                                    data_name='Expense',
                                    transaction_col_name='Particulars'
                                    )
    
    if no_of_file > 1:
        Account_1 = DataTransformer_Account_1.transform_data_to_df()
        Account_2 = DataTransformer_Account_2.transform_data_to_df()
        Account_2.drop(index=Account_2.index[0], axis=0, inplace=True)

        all_accounts = pd.concat([Account_1, Account_2], ignore_index=True)
        all_accounts = DataProcessor.__clean_all_column__(all_accounts)

        logging.info(f'DATA TRANSFORMATION Completed and stored to dataframe')
        return all_accounts
    
    elif no_of_file == 1:
        Account_1 = DataTransformer_Account_1.transform_data_to_df()
        logging.info(f'DATA TRANSFORMATION Completed and stored to dataframe')
        return Account_1
    
# return_data = get_data(no_of_file=2)