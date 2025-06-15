import json
from typing import List, Dict

from src.data_extraction.markdown_extraction import extract_all_markdown_from_directory
from src.data_extraction.docx_extraction import extract_all_docx_paragraphs_from_directory
from src.data_extraction.pdf_extraction import extract_all_pdfs_from_directory
from src.data_extraction.txt_extraction import extract_all_txt_from_directory

from src.dataset_generator.dataset_generator import dataset_generator


def curate_dataset_with_questions(
    input_path: str,
    output_file_path: str,
    doc_type: str,
    num_questions: int = 1,
) -> None:
    """
    Extracts data from the specified document type and generates a dataset with questions.

    Args:
        input_path (str): Path to the input file or directory.
        output_file_path (str): Path to save the final JSON with questions included.
        doc_type (str): Type of document to extract ('pdf', 'docx', 'txt', 'markdown').
    """
    # Step 1: Extract data based on doc_type
    match doc_type.lower():
        case "pdf":
            extracted_paths = extract_all_pdfs_from_directory(input_path)
        case "docx":
            extracted_paths = extract_all_docx_paragraphs_from_directory(input_path)
        case "txt":
            extracted_paths = extract_all_txt_from_directory(input_path)
        case "markdown":
            extracted_paths = extract_all_markdown_from_directory(input_path)
        case _:
            raise ValueError(f"Unsupported document type: {doc_type}")

    all_curated_data = []

    with open(extracted_paths, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        for chunk in chunks:
            print(chunk)
            questions = dataset_generator(chunk, num_questions)
            chunk["questions"] = questions
            all_curated_data.append(chunk)

    # Step 3: Save the combined JSON with questions
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(all_curated_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Curated dataset saved to {output_file_path}")


curate_dataset_with_questions(
    input_path="data",
    output_file_path="outputs/curated_dataset.json",
    doc_type="txt"
)