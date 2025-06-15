import os
import json

def extract_all_txt_from_directory(directory_path, lines_per_chunk=50, output_directory=None, output_filename="txt_chunks.json"):
    """
    Extracts chunks of lines (default 50) from all TXT files in a directory and saves them to a JSON file.

    Args:
        directory_path (str): Path to the directory containing TXT files.
        lines_per_chunk (int): Number of lines per chunk.
        output_directory (str, optional): Directory to save the output JSON file. Defaults to current directory.
        output_filename (str): Name of the output JSON file.

    Returns:
        list: List of dicts with "txt_name", "chunk", and "content".
    """
    all_extracted_data = []

    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return []

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".txt"):
            txt_path = os.path.join(directory_path, filename)
            print(f"Processing: {txt_path}")

            try:
                with open(txt_path, 'r', encoding='utf-8') as file:
                    lines = [line.strip() for line in file if line.strip()]
                
                # Chunk the lines
                for i in range(0, len(lines), lines_per_chunk):
                    chunk_lines = lines[i:i + lines_per_chunk]
                    chunk_content = "\n".join(chunk_lines)
                    all_extracted_data.append({
                        "txt_name": filename,
                        "chunk": (i // lines_per_chunk) + 1,
                        "content": chunk_content
                    })

                print(f"✓ Extracted {len(all_extracted_data)} chunks from {filename}")

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
