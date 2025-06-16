import pdfplumber
import re
import os

# Define file paths
input_pdf = "data/raw_data/pension_document.pdf"  # Updated input path
output_file = "data/processed_data/extracted_cleaned_text.txt"  # Updated output path

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Extract text from the PDF
with pdfplumber.open(input_pdf) as pdf:
    with open(output_file, "w", encoding="utf-8") as f:
        for page in pdf.pages:
            # Extract text from the page
            text = page.extract_text()

            # Remove standalone numbers (e.g., page numbers)
            text = re.sub(r'\b\d+\b', '', text)  # Matches standalone numbers

            # Optionally remove patterns like "Page X" (case-insensitive)
            text = re.sub(r'Page \d+', '', text, flags=re.IGNORECASE)

            # Write the cleaned text to the output file
            f.write(text)
            f.write("\n\n")  # Separate pages with double newlines

print(f"Cleaned text extraction completed. The output is saved in '{output_file}'.")