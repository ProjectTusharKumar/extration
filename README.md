# Contact Information Extractor

This Python utility extracts phone numbers and names from images and PDF files, saving the results to an Excel file.

## Features

- Extracts phone numbers using regular expressions
- Extracts names using SpaCy's Named Entity Recognition
- Supports multiple image formats (JPG, JPEG, PNG, TIFF, BMP)
- Supports PDF files
- Saves results to Excel files
- Process single files or entire directories

## Installation

1. Install the required system dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install -y tesseract-ocr poppler-utils
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install SpaCy's English language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

### Process a single file:
```bash
python main.py path/to/your/file.pdf --output results.xlsx
```

### Process an entire directory:
```bash
python main.py path/to/your/directory --output results.xlsx
```

## Output Format

The script generates an Excel file with the following columns:
- Source File: Path to the original file
- Name: Extracted name
- Phone Number: Extracted phone number

## Supported Formats

- Images: JPG, JPEG, PNG, TIFF, BMP
- Documents: PDF

## Notes

- The phone number extraction supports various formats including:
  - International numbers with country codes
  - Numbers with area codes
  - Different separators (spaces, dashes, dots)
- Name extraction uses SpaCy's Named Entity Recognition system
- For best results, ensure input images are clear and well-scanned