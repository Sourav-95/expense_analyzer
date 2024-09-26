import pdfplumber
import pandas as pd

def extract_transaction_data(file_path, header_identifier, footer_identifier):
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
