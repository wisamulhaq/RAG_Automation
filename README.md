# RAG Evaluation Automation

RAG Automation is a modular pipeline for automating Retrieval-Augmented Generation (RAG) workflows. It extracts, processes, and evaluates datasets from various document formats (PDF, DOCX, TXT, Markdown) to support RAG-based applications.

## Features

- Extracts text from PDF, DOCX, TXT, and Markdown files ([src/data_extraction/](src/data_extraction/))
- Generates and curates datasets for RAG ([src/dataset_generator/dataset_generator.py](src/dataset_generator/dataset_generator.py))
- Evaluates retrieval and generation quality using LLMs ([src/evaluator/evaluator.py](src/evaluator/evaluator.py))
- Easily extensible and configurable

## Project Structure

```
.env
.gitignore
generate_dataset.py
main.py
README.md
requirements.txt
run_evaluations.py
data/
    example.docx
    example.pdf
    example.txt
    markdown.md
outputs/
    curated_dataset.json
src/
    data_extraction/
        docx_extraction.py
        markdown_extraction.py
        pdf_extraction.py
        txt_extraction.py
    dataset_generator/
          dataset_generator.py   # Supports parameters for adding extra instructions or context for your use case, and lets you control the number of questions generated.
     evaluator/
          evaluator.py           # Accepts parameters to add more rules or specify the level of detail for LLM evaluation, allowing customization for your requirements.
tests/
```

## Getting Started

1. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Configure environment variables:**  
   Edit `.env` with your Azure OpenAI credentials.

3. **Add your documents:**  
   Place PDF, DOCX, TXT, or Markdown files in the `data/` directory.

4. **Generate a dataset:**  
    Adjust the parameters in `generate_dataset.py` to match your data source type (PDF, DOCX, TXT, or Markdown).  
    You can also provide extra instructions for question generation by editing the relevant arguments or prompts in the script.

     ```sh
     python generate_dataset.py
     ```

5. **Run evaluation:**
    ```sh
    python run_evaluations.py
    ```

## Outputs

- Curated datasets and results are saved in the `outputs/` directory, e.g. [outputs/curated_dataset.json](outputs/curated_dataset.json).

## Example Data

- Example input files are in [data/](data/)
- Example output: [outputs/curated_dataset.json](outputs/curated_dataset.json)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License