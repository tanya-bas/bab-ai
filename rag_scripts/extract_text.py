import pdfplumber
import os

# Define file paths
input_pdf = "data/raw_data/pension_document.pdf"  # Updated input path
output_file = "data/processed_data/extracted_text.txt"  # Updated output path

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Extract text from the PDF
with pdfplumber.open(input_pdf) as pdf:
    with open(output_file, "w", encoding="utf-8") as f:
        for page in pdf.pages:
            f.write(page.extract_text())
            f.write("\n\n")  # Separate pages with double newlines

print(f"Text extraction completed. The output is saved in '{output_file}'.")
