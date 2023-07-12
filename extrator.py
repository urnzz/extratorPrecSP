import os
import shutil
import fitz  # pymupdf
import csv  # csv module

# Define the directories
pdf_dir = './pdfs'
processed_dir = './pdfs/processed'

# Create the processed directory if it doesn't exist
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

# Define the output CSV file
output_csv = './output.csv'

# Define the headers for the CSV file
headers = ["nº de ordem cronológica", "processo", "processo de origem", "vara", "reqte", "advogado", "entidade devedora", "advogados"]

# Open the output CSV file in write mode
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')
    writer.writeheader()
    
    # Loop through each file in the directory
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            # Create a Document instance
            doc = fitz.open(os.path.join(pdf_dir, filename))

            # Extract text from each page
            for page in doc:
                text = page.get_text()

                # Initialize an empty dictionary to store the data for this page
                data = {}

                # Split the text into lines
                lines = text.split('\n')
                
                # Process each line
                for line in lines:
                    # Check if the line contains ':'
                    if ':' in line:
                        # Split the line into key and value
                        parts = line.split(':', 1)
                        key = parts[0].strip().lower()
                        value = parts[1].strip()

                        # Check if the normalized key is in the headers
                        if key in headers:
                            # Store the value in the data dictionary
                            data[key] = value

                # Write the data to the CSV file
                writer.writerow(data)

            # Close the Document instance
            doc.close()

            # Move the file to the processed directory
            shutil.move(os.path.join(pdf_dir, filename), processed_dir)
