import os
import json
import argparse
from textstat import flesch_reading_ease, flesch_kincaid_grade

def compute_scores(bench_name):
    # Define paths
    input_dir = os.path.join('data', bench_name, 'model_answer')
    output_path = os.path.join('data', bench_name, 'textstats', 'flesch_scores.jsonl')

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Process and compute scores
    with open(output_path, 'w') as outfile:
        for filename in os.listdir(input_dir):
            with open(os.path.join(input_dir, filename), 'r') as file:
                lines = file.readlines()
            data = [json.loads(line) for line in lines]

            turns_scores = []
            total_fre, total_fkgl = 0, 0
            total_turns = 0

            for entry in data:
                turn_text = entry.get('choices', [{}])[0].get('turns', [])
                turn_scores = [{'fre': flesch_reading_ease(text), 'fkgl': flesch_kincaid_grade(text)} for text in turn_text]
                total_fre += sum(turn_score['fre'] for turn_score in turn_scores)
                total_fkgl += sum(turn_score['fkgl'] for turn_score in turn_scores)
                total_turns += len(turn_scores)
                turns_scores.append(turn_scores)

            avg_fre = total_fre / total_turns
            avg_fkgl = total_fkgl / total_turns

            # Store the scores with the filename, model_id, and average scores
            result = {
                "model_id": data[0]['model_id'],
                "turn_scores": turns_scores,
                "average_scores": {"Average FRE": avg_fre, "Average FKGL": avg_fkgl}
            }
            outfile.write(json.dumps(result) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute Flesch Reading Ease and Flesch-Kincaid Grade Level scores.")
    parser.add_argument('--bench-name', required=True, help="Name of the benchmark.")
    args = parser.parse_args()
    compute_scores(args.bench_name)
