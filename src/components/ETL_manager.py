import csv
import pandas as pd
import pdfplumber

class DataIngestor():
    @classmethod
    def read_csv_files(cls, file_path, header_identifier, footer_identifier):
        start_found = False                                      # Flags to identify when transactional data starts and ends
        transaction_lines = []

        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                clean_line = [item.strip() for item in line]     # Clean up the line (strip spaces, avoid case issues)
                if not start_found and any(header_identifier in item for item in clean_line):   
                    start_found = True
                    transaction_lines.append(line)                                              

                elif start_found:
                    if any(footer_identifier in item for item in clean_line):           
                        break                                                                   
                    transaction_lines.append(line)
        # Creating Dataframe to store    
        if transaction_lines:                                       
            df = pd.DataFrame(transaction_lines[1:], columns=transaction_lines[0])
            return df
        else:
            return pd.DataFrame()  
    

    @classmethod
    def read_pdf_files(cls, file_path, header_identifier, footer_identifier):
        start_found = False                                     # Flags to identify when transactional data starts and ends
        transaction_lines = []

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()                         # Extract text from the page
                if text:                                           # Ensure there's text on the page
                    lines = text.split('\n')                       # Split the text into lines
                    for line in lines:
                        clean_line = [item.strip() for item in line.split()]    # Clean up the line (strip spaces)
                        if not start_found and any(header_identifier in item for item in clean_line):   # Check for the header row to start extracting data
                            start_found = True
                            transaction_lines.append(clean_line)  # Include the header
                        elif start_found:
                            if any(footer_identifier in item.lower() for item in clean_line):   # Check if 'footer_row' appears anywhere in the line (case-insensitive)
                                break                               # Stop recording data when the unwanted section starts
                            transaction_lines.append(clean_line)    # Add transaction rows to the list
        if transaction_lines:                                       # Create a DataFrame from the extracted data
            df = pd.DataFrame(transaction_lines[1:], columns=transaction_lines[0])  # Skip the header
            return df
        else:
            return pd.DataFrame()                                   # Return an empty DataFrame if no data was found                                                                     
class DataProcessor():
    @classmethod
    def remap_transactions(cls, data, transaction_col_name:str):
        def extract_name(particulars):
            if isinstance(particulars, str):                    # Check if the value is a string (not None or NaN)
                try:
                    return particulars.split('/')[3]            # Split the string by '/' and return the 4th part (index 3)
                except IndexError:
                    return particulars                          # Return original if splitting fails
            else:
                return particulars                              # Return as is if it's None or NaN
        data[transaction_col_name] = data[transaction_col_name].apply(extract_name)
        return data
    




