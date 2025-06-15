import PyPDF2
import os
import json
from docx import Document

def extract_all_docx_paragraphs_from_directory(
    directory_path,
    output_directory=None,
    output_filename="docx_paragraphs.json"
):
    """
    Extracts content from DOCX files paragraph by paragraph and saves to JSON.

    Args:
        directory_path (str): Path to the directory containing DOCX files.
        output_dir (str, optional): Directory to save the output JSON file. Defaults to None (current directory).
        output_file_name (str, optional): Name of the output JSON file. Defaults to "docx_paragraphs.json".

    Returns:
        list: List of dicts with "docx_name", "paragraph", and "content".
    """
    all_extracted_data = []

    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return []

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".docx"):
            docx_path = os.path.join(directory_path, filename)
            print(f"Processing: {docx_path}")

            try:
                doc = Document(docx_path)
                paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

                for i, para in enumerate(paragraphs, start=1):
                    all_extracted_data.append({
                        "docx_name": filename,
                        "paragraph": i,
                        "content": para
                    })

                print(f"✓ Extracted {len(paragraphs)} paragraphs from {filename}")

            except Exception as e:
                print(f"✗ Error reading {filename}: {e}")

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

