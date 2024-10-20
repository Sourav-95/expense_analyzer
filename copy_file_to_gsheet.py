from src.logger import logging
from src.exception import CustomException
from src.get_all_data import get_data
from utils.gsheet_api_connection import export_to_gsheet
import sys
import os


return_data = get_data(no_of_file=1)
credentials_file_name = 'clientKey.json'
credentials_path = os.path.join(os.getcwd(), credentials_file_name)

spreadsheet_id = '1zMUR3CwrJr6idrNZGLLhaiWl9JmA7-CKIJAw42hyehc'

if return_data is not None:
    logging.info("Exporting to Google Sheets")
    export_to_gsheet(return_data, credentials_path, spreadsheet_id)
