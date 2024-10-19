import sys
import os
import pandas as pd
import pdfplumber
from src.exception import CustomException
from src.ETL_manager import DataIngestor
from src.ETL_manager import DataProcessor
from src.inputs import mapping
from src.inputs.column_structure import get_cols
import warnings
# from src.logger import logging
import logging
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

class DataTransformer():
    def __init__(self, input_file:str, col_name:list, data_name:str, 
                 transaction_col_name:str):
        self.input_file = os.getcwd()+input_file
        input_file = os.getcwd()+input_file
        self.col_name = col_name
        self.data_name = data_name
        self.transaction_col_name = transaction_col_name
    
    def transform_data_to_df(self):
        df = DataIngestor.read_statement(file_path=self.input_file, 
                                         col_names=self.col_name
                                         )
        logging.info(f'DATA INGESTION Completed..................')
        df = DataIngestor.clean_features(data=df, 
                                         data_name=self.data_name
                                         )
        logging.info(f'DATA CLEANING Completed...................')
        df = DataProcessor.remap_transactions(df, 
                                              transaction_col_name=self.transaction_col_name
                                              )
        logging.info(f'DATA REMAP TRANSACTION Completed..........')
        df = DataProcessor.map_expense_group(df)


        logging.info(f'Mapping Expense Group.....................')
        return df

data_trasformer = DataTransformer(input_file='/raw_file/exp_statement.csv',
                                  col_name=get_cols.col1(),
                                  data_name='Expense',
                                  transaction_col_name='Particulars'
                                  )

transform_df = data_trasformer.transform_data_to_df()
logging.info(f'DATA TRANSFORMATION Done')