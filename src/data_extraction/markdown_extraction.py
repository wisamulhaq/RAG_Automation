import os
import json

def extract_all_markdown_from_directory(
    directory_path,
    output_directory=None,
    output_filename="extracted_markdown.json"
):
    """
    Reads all markdown files in a directory and extracts content under each main heading (lines starting with '# ').
    Optionally saves the extracted data to a JSON file.

    Args:
        directory_path (str): The path to the directory containing markdown files.
        output_directory (str, optional): Directory to save the output JSON file. Defaults to None (uses directory_path).
        output_file_name (str, optional): Name of the output JSON file. Defaults to "extracted_markdown.json".

    Returns:
        list: A list of dictionaries, each with keys: "markdown_name", "heading", "content".
    """
    all_extracted_data = []

    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return []

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".md"):
            md_path = os.path.join(directory_path, filename)
            print(f"Processing: {md_path}")

            try:
                with open(md_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                current_heading = None
                current_content = []

                for line in lines:
                    if line.startswith("# "):  # Top-level heading
                        if current_heading:
                            all_extracted_data.append({
                                "markdown_name": filename,
                                "heading": current_heading.strip(),
                                "content": ''.join(current_content).strip()
                            })
                        current_heading = line[2:].strip()
                        current_content = []
                    else:
                        current_content.append(line)

                # Catch the last heading block
                if current_heading:
                    all_extracted_data.append({
                        "markdown_name": filename,
                        "heading": current_heading.strip(),
                        "content": ''.join(current_content).strip()
                    })

                print(f"✓ Finished extracting from {filename}")
            except Exception as e:
                print(f"✗ Error reading {filename}: {e}")

    # Determine output directory
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
