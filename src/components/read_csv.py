import csv
import pandas as pd

def extract_transaction_data(file_path, header_identifier, footer_identifier):
    start_found = False                                                                     # Flags to identify when transactional data starts and ends
    transaction_lines = []

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            clean_line = [item.strip() for item in line]                                    # Clean up the line (strip spaces, avoid case issues)
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



