import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from src.exception import CustomException
from src.logger import logging
import sys

def export_to_gsheet(dataframe:pd.DataFrame, credentials_path, spreadsheet_id):
    try:
        # Define the scope for Google Sheets and Drive APIs
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

        # Add credentials to the service account
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)

        # Open the spreadsheet by ID
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Select the first worksheet and clear it
        worksheet = spreadsheet.get_worksheet(0)
        worksheet.clear()

        # Export the DataFrame to the sheet
        set_with_dataframe(worksheet, dataframe)
        logging.info(f"Data exported to Google Sheet with ID: {spreadsheet_id}")
    except Exception as e:
        raise CustomException(e, sys)