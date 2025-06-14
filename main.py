import argparse
from pathlib import Path
from extractor import ContactExtractor

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Extract names and phone numbers from images and PDFs')
    parser.add_argument('input_path', help='Path to input file or directory')
    parser.add_argument('--output', '-o', default='extracted_contacts.xlsx',
                       help='Path to output Excel file (default: extracted_contacts.xlsx)')
    
    args = parser.parse_args()
    input_path = Path(args.input_path)
    
    # Initialize the extractor
    extractor = ContactExtractor()
    
    # Process based on whether input is a file or directory
    if input_path.is_file():
        names, phone_numbers = extractor.process_file(input_path)
        if names or phone_numbers:
            results = [{
                'Source File': str(input_path),
                'Name': name,
                'Phone Number': phone
            } for name in names for phone in phone_numbers]
            
            import pandas as pd
            df = pd.DataFrame(results)
            df.to_excel(args.output, index=False)
            print(f"Results saved to {args.output}")
        else:
            print("No data was extracted from the file")
    
    elif input_path.is_dir():
        extractor.process_directory(input_path, args.output)
    
    else:
        print(f"Error: {input_path} does not exist")

if __name__ == '__main__':
    main()
