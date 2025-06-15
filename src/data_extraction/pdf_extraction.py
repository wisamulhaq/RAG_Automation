import PyPDF2
import os
import json

def extract_all_pdfs_from_directory(directory_path, output_directory=None, output_filename="all_pdfs_extracted.json"):
    """
    Reads all PDF files in the given directory, extracts content from each page,
    and saves the extracted data to a JSON file in the specified output directory.

    Args:
        directory_path (str): The path to the directory containing PDF files.
        output_directory (str, optional): The directory where the JSON output will be saved. Defaults to current directory.
        output_filename (str, optional): The name of the JSON file to store the output. Defaults to 'all_pdfs_extracted.json'.

    Returns:
        str: The path to the output JSON file if data was extracted, else None.
    """
    all_extracted_data = []

    # Ensure the directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return None

    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            print(f"Processing: {pdf_path}")
            try:
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page_num, page in enumerate(reader.pages):
                        page_content = page.extract_text()
                        all_extracted_data.append({
                            "pdf_name": filename,
                            "page": page_num + 1,
                            "content": page_content.strip() if page_content else ""
                        })
                print(f"✓ Finished extracting from {filename}")
            except PyPDF2.errors.PdfReadError as e:
                print(f"✗ Error reading {filename}: {e}")
            except Exception as e:
                print(f"✗ Unexpected error with {filename}: {e}")

    # Save to a single JSON file if data was extracted
    if all_extracted_data:
        if output_directory is None:
            output_directory = os.getcwd()
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_extracted_data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ All extracted content saved to {output_path}")
        return output_path
    else:
        print("\n⚠️ No data extracted.")
        return None
