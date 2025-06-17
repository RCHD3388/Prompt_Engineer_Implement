# main.py

from utils.io_utils import load_json, save_json
from utils.gemini_client import generate_answer
import re
import os
import argparse
import pandas as pd
import prompts.gameof24_template as gameof24_template
import time
generate_prompt = gameof24_template.generate_prompt



def parse_args():
    parser = argparse.ArgumentParser(description="Run prompting with Gemini API.")
    parser.add_argument(
        "--output",
        type=str,
        default="generate_res/dummy.json",
        help="Output file path (default: generate_res/dummy.json)"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="writing",
        help="Dataset type ? game24 or writing (default: writing)"
    )
    parser.add_argument(
        "--n-sample",
        type=str,
        default="5",
        help="Generated samples for each input (default: 5)"
    )

    return parser.parse_args()


def handle_game24(args):
    dataset_path = os.path.join("dataset", "game24.csv")
    dataset = pd.read_csv(dataset_path)

    current_input_list = [[]]
    new_target_input = []
    generated_samples = []

    output_info = []
    for index, row in dataset.iterrows():
        logging_info = {
            "index": index,
            "input": row["Puzzles"],
            "steps": [],
            "final_score": 0,
        }
        print("\nSolve Puzzle Record : ", index)
        for step_index, _ in enumerate(range(3)):
            generated_samples = []
            if step_index == 0:
                current_input_list = [list(map(int, row["Puzzles"].split()))]
            else: 
                current_input_list = new_target_input.copy()

            # STEP 1 GENERATE SAMPLES
            for index, i in enumerate(current_input_list):
                current_input_string = ' '.join(map(str, i))
                prompt = re.sub(r"\{input\}", current_input_string, generate_prompt)
                prompt = re.sub(r"\{n_sample\}", args.n_sample, prompt)
                generated_samples_string = generate_answer(prompt)
                generated_samples_string_split = generated_samples_string.split('\n')

                if step_index != 0:
                    generated_samples_string_split = [logging_info["steps"][step_index - 1]["new_target_path"][index] + item for item in generated_samples_string_split]
                
                generated_samples.extend(generated_samples_string_split[0:])

            # STEP 2 EVALUATE SAMPLES
            candidate_input_list = []
            for sample in generated_samples:
                match = re.search(r'\(left:\s*([0-9.\s]+(?:\.\.\.)?)\)$', sample)
                if match:
                    raw_values = match.group(1).strip().split()
                    cleaned_values = [val.replace('...', '') for val in raw_values]
                    try:
                        numbers = [float(v) if '.' in v else int(v) for v in cleaned_values]
                        candidate_input_list.append(numbers)
                    except ValueError:
                        # Lewati jika parsing gagal (misalnya string tidak valid)
                        continue
            
            print(candidate_input_list)
            print("Evaluating candidates...")
            
            candidate_scores = [0] * len(candidate_input_list)
            for index, candidate in enumerate(candidate_input_list):
                # for _ in range(3):
                candidate_string = ' '.join(map(str, candidate))
                prompt = re.sub(r"\{input\}", candidate_string, gameof24_template.evaluate_prompt)
                result = generate_answer(prompt)
                
                match = re.search(r'evaluate:\s*(\w+)', result)
                if match:
                    hasil = match.group(1)
                    if hasil == "sure":
                        candidate_scores[index] += 10
                    elif hasil == "likely":
                        candidate_scores[index] += 1
                    else :
                        candidate_scores[index] += 0.01
                    
            time.sleep(60)
            
            print("Candidate scores:", candidate_scores)

            # STEP 3 FINALIZE ANSWER
            new_target_input = []
            candidate_with_score = [(index, score) for index, score in enumerate(candidate_scores)]
            sorted_candidate = sorted(candidate_with_score, key=lambda x: x[1], reverse=True)

            top_3_index = [x[0] for x in sorted_candidate[:3]]
            new_target_input = [candidate_input_list[i] for i in top_3_index]

            logging_info["steps"].append({
                "step": step_index + 1,
                "generated_samples": generated_samples,
                "candidate_input_list": [str(x) for x in candidate_input_list],
                "candidate_scores": candidate_scores,
                "new_target_input": [str(x) for x in new_target_input],
                "new_target_path": [generated_samples[i] for i in top_3_index]
            })
        
        logging_info["final_score"] = "passed" if logging_info["steps"][2]["new_target_input"][0] == "[24]" else "failed"
        output_info.append(logging_info)
        time.sleep(60)  # Sleep to avoid rate limiting issues

    # Save output_info to file based on the output argument
    output_path = args.output
    save_json(output_info, output_path)

    return

def handle_writing(args):
    with open(os.path.join("dataset", "writing.txt"), "r") as f:
        writing_data = [line.strip() for line in f.readlines()]
    
    output_info = []
    for idx, data in enumerate(writing_data):
        logging_info = {
            "id": idx + 1,
            "input": data,
            "steps": []
        }

        # ToT Prompting 


        output_info.append(logging_info)
    
    # Save output_info to file based on the output argument
    output_path = args.output
    save_json(output_info, output_path)
    return


def main():
    args = parse_args()
    print("Arguments parsed:")
    for arg, value in vars(args).items():
        print(f"{arg}: {value}")
    print("\n")

    if args.dataset == "game24":
        handle_game24(args)
    elif args.dataset == "writing":
        handle_writing(args)
        
if __name__ == "__main__":
    main()
