import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def read_data_from_gsheet(sheet_id: str, sheet_name: str, credentials_file: str) -> pd.DataFrame:
    """
    Function to read data from Google Sheets and return it as a pandas DataFrame.

    Parameters:
    sheet_id (str): The Google Sheet ID (found in the sheet URL)
    sheet_name (str): The specific sheet name inside the Google Sheet
    credentials_file (str): The path to the service account JSON credentials file

    Returns:
    pd.DataFrame: Data from the Google Sheet as a pandas DataFrame
    """
    
    # Define the scope for accessing Google Sheets and Google Drive
    scope = ['https://www.googleapis.com/auth/spreadsheets', 
             'https://www.googleapis.com/auth/drive']

    # Authenticate using the service account key JSON file
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(credentials)

    # Construct the full Google Sheets URL
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"

    # Open the Google Sheet by its ID
    spreadsheet = client.open_by_url(sheet_url)

    # Select the sheet by name
    sheet = spreadsheet.worksheet(sheet_name)

    # Get all values from the sheet as a list of lists
    data = sheet.get_all_values()

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])  # Skip the header row while keeping column names

    return df
