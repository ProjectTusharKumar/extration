import cv2
import pytesseract
import pandas as pd
import spacy
import re
from pdf2image import convert_from_path
from pathlib import Path
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContactExtractor:
    def __init__(self):
        # Load the English language model for SpaCy
        self.nlp = spacy.load("en_core_web_sm")
        
        # Phone number regex pattern
        self.phone_pattern = re.compile(
            r'''(?:
                (?:\+?\d{1,3}[-.\s]?)?  # optional country code
                (?:\(?\d{3}\)?[-.\s]?)   # area code
                \d{3}[-.\s]?             # first 3 digits
                \d{4}                     # last 4 digits
            )''', re.VERBOSE
        )

    def extract_from_image(self, image_path):
        """Extract text from an image file."""
        try:
            # Read image using OpenCV
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(gray)
            return text
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            return ""

    def extract_from_pdf(self, pdf_path):
        """Extract text from a PDF file by converting it to images first."""
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            texts = []
            
            # Process each page
            for image in images:
                # Convert PIL image to OpenCV format
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray)
                texts.append(text)
            
            return "\n".join(texts)
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            return ""

    def extract_phone_numbers(self, text):
        """Extract phone numbers from text using regex."""
        return self.phone_pattern.findall(text)

    def extract_names(self, text):
        """Extract names from text using SpaCy NER."""
        doc = self.nlp(text)
        names = [ent.text for ent in doc.ents if ent.label_ in ["PERSON"]]
        return names

    def process_file(self, file_path):
        """Process a single file (image or PDF) and extract information."""
        file_path = Path(file_path)
        text = ""
        
        if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
            text = self.extract_from_image(file_path)
        elif file_path.suffix.lower() == '.pdf':
            text = self.extract_from_pdf(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_path}")
            return [], []

        phone_numbers = self.extract_phone_numbers(text)
        names = self.extract_names(text)
        
        return names, phone_numbers

    def process_directory(self, directory_path, output_file='extracted_contacts.xlsx'):
        """Process all supported files in a directory and save results to Excel."""
        directory = Path(directory_path)
        results = []
        
        # Process all supported files
        supported_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.pdf'}
        for file_path in directory.glob('**/*'):
            if file_path.suffix.lower() in supported_extensions:
                logger.info(f"Processing file: {file_path}")
                names, phone_numbers = self.process_file(file_path)
                
                # Create entries for each combination of name and phone number
                for name in names:
                    for phone in phone_numbers:
                        results.append({
                            'Source File': str(file_path),
                            'Name': name,
                            'Phone Number': phone
                        })
        
        # Create DataFrame and save to Excel
        if results:
            df = pd.DataFrame(results)
            df.to_excel(output_file, index=False)
            logger.info(f"Results saved to {output_file}")
        else:
            logger.warning("No data was extracted from the files")
