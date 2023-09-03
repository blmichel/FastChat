import json
import os
import argparse

def display_scores(bench_name, num_turns=1):
    # Define the path to the JSONL file where the scores are saved
    file_path = os.path.join('data', bench_name, 'textstats', 'flesch_scores.jsonl')

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist!")
        return

    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line.strip())
 #           print(f"Scores for model: {data['model_id']}):")

            for doc_scores in data['turn_scores']:
                avg_fre = sum(turn_score['fre'] for turn_score in doc_scores[:num_turns]) / num_turns
                avg_fkgl = sum(turn_score['fkgl'] for turn_score in doc_scores[:num_turns]) / num_turns
            print(f"Average scores for {data['model_id']} - FRE: {avg_fre:.2f}, FKGL: {avg_fkgl:.2f} (over {num_turns} turns)")

            if num_turns > 1:
                print(f"\tOverall Average - FRE: {data['average_scores']['Average FRE']:.2f}, FKGL: {data['average_scores']['Average FKGL']:.2f}")
                print("===" * 10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display Flesch Reading Ease and Flesch-Kincaid Grade Level scores.")
    parser.add_argument('--bench-name', required=True, help="Name of the benchmark.")
    parser.add_argument('--num-turns', type=int, default=1, choices=[1, 2], help="Number of turns' scores to display (1/2).")
    args = parser.parse_args()

    display_scores(args.bench_name, args.num_turns)
