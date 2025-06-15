import json
from src.evaluator.evaluator import evaluate_response
import os

def run_evaluations(
    dataset_path: str = os.path.join(os.path.dirname(__file__), 'outputs', 'curated_dataset.json'),
    criteria: str = "relevance, factual accuracy, completeness",
    detail_level: str = "brief"
) -> None:
    """
    Run evaluations on a list of questions and their corresponding responses.

    Args:
        dataset_path (str): Path to the dataset JSON file.
        criteria (str): Evaluation criteria to use.
        detail_level (str): Level of detail in the evaluation explanation.
    """
    with open(dataset_path, 'r') as file:
        dataset = json.load(file)

    for entry in dataset:
        questions = json.loads(entry["questions"])
        content = entry["content"]
        for question_item in questions:
            question = question_item["question"]
      
            evaluation = evaluate_response(
                question,
                content,
                content,
                criteria=criteria,
                detail_level=detail_level
            )
            print(evaluation)
            # Save each evaluation as a JSON object in the output folder
            output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
            os.makedirs(output_dir, exist_ok=True)
            result = {
                "question": question,
                "content": content,
                "evaluation": evaluation
            }
            result_path = os.path.join(output_dir, 'results.json')
            # Append each result to the results.json file
            if os.path.exists(result_path):
                with open(result_path, 'r+') as f:
                    try:
                        results = json.load(f)
                    except json.JSONDecodeError:
                        results = []
                    results.append(result)
                    f.seek(0)
                    json.dump(results, f, indent=2)
                    f.truncate()
            else:
                with open(result_path, 'w') as f:
                    json.dump([result], f, indent=2)

if __name__ == "__main__":
    run_evaluations()
