# main.py

from utils.io_utils import load_json, save_json
from utils.gemini_client import generate_answer
import re
from prompts.templates import basic_math_template, plan_and_solve_template 
import os
import argparse
import time

INPUT_FILE = "dataset/gsm8k.json"
OUTPUT_FILE = "generate_res/gsm8k.json"

# Mapping teknik ke fungsi template
from prompts.templates import (
    basic_math_template,
    plan_and_solve_template,
    plan_and_solve_fewshot_template,
    aqua_plan_and_solve_template,
    aqua_plan_and_solve_fewshot_template,
    lastletter_plan_and_solve,
    lastletter_plan_and_solve_fewshot
)

TEMPLATE_MAP = {
    "basic": basic_math_template,
    "plan-and-solve": plan_and_solve_template,
    "plan-and-solve-fewshot": plan_and_solve_fewshot_template,
    "aqua-plan-and-solve": aqua_plan_and_solve_template,
    "aqua-plan-and-solve-fewshot": aqua_plan_and_solve_fewshot_template,
    "lastletter-plan-and-solve": lastletter_plan_and_solve,
    "lastletter-plan-and-solve-fewshot": lastletter_plan_and_solve_fewshot,
}

def parse_args():
    parser = argparse.ArgumentParser(description="Run prompting with Gemini API.")
    parser.add_argument(
        "--technique",
        choices=TEMPLATE_MAP.keys(),
        default="basic",
        help="Prompting technique to use (default: basic)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="generate_res/dummy.json",
        help="Output file path (default: generate_res/gsm8k.json)"
    )
    parser.add_argument(
        "--dataset-type",
        choices=["gsm8k", "aqua", "lastletter"],
        required=True,
        help="Dataset type: gsm8k or aqua"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="dataset/gsm8k.json",
        help="Dataset file path (default: dataset/gsm8k.json)"
    )

    return parser.parse_args()

# main.py - processing lastletter dataset
def process_lastletter(dataset, prompt_fn, technique):
    results = []
    correct_count = 0

    for i, entry in enumerate(dataset):
        question = entry["question"]
        expected_answer = entry["answer"]

        prompt = prompt_fn(question)
        print(f"[{i+1}] LastLetter: {question[:60]}...")

        model_answer = generate_answer(prompt)

        if "Solve:" in model_answer:
            plan_part, solve_part = model_answer.split("Solve:", 1)
            reasoning = plan_part.strip() + "\nSolve:\n" + solve_part.strip()
            full_text = solve_part.strip()
        else:
            reasoning = model_answer.strip()
            full_text = model_answer.strip()

        match = re.search(r"Answer:\s*([a-zA-Z]+)", full_text)
        final_answer = match.group(1).lower() if match else None

        is_correct = final_answer == expected_answer if final_answer else False
        if is_correct:
            correct_count += 1

        if technique == "plan-and-solve-fewshot" or technique == "lastletter-plan-and-solve-fewshot":
            plan_match = re.search(r"Plan:\s*(.*?)Solve:", model_answer, re.DOTALL)
            solve_match = re.search(r"Solve:\s*(.*?)Answer:", model_answer, re.DOTALL)

            results.append({
                "question": question,
                "expected_answer": expected_answer,
                "plan": plan_match.group(1).strip() if plan_match else "",
                "solve": solve_match.group(1).strip() if solve_match else "",
                "generated_answer": final_answer,
                "correct": is_correct
            })
        else:
            results.append({
                "question": question,
                "expected_answer": expected_answer,
                "reasoning": reasoning,
                "generated_answer": final_answer,
                "correct": is_correct
            })

        if (i+1) % 15 == 0:
            print(f"Delaying for 1 minute after {i+1} iterations...")
            time.sleep(60)
            
    return results, correct_count
# main.py - processing gsm8k dataset
def process_gsm8k(dataset, prompt_fn, technique):
    results = []
    correct_count = 0

    for i, entry in enumerate(dataset):
        question = entry["question"]
        expected_answer = entry["answer"]

        prompt = prompt_fn(question)
        print(f"[{i+1}] GSM8K: {question[:60]}...")

        model_answer = generate_answer(prompt)

        if "Solve:" in model_answer:
            plan_part, solve_part = model_answer.split("Solve:", 1)
            reasoning = plan_part.strip() + "\nSolve:\n" + solve_part.strip()
            full_text = solve_part.strip()
        else:
            reasoning = model_answer.strip()
            full_text = model_answer.strip()

        match = re.search(r"Answer:\s*([-+]?\d*\.\d+|\d+)", full_text)
        final_answer = float(match.group(1)) if match else None

        is_correct = (round(final_answer, 2) == round(expected_answer, 2)) if final_answer is not None else False
        if is_correct:
            correct_count += 1

        if technique == "plan-and-solve-fewshot":
            plan_match = re.search(r"Plan:\s*(.*?)Solve:", model_answer, re.DOTALL)
            solve_match = re.search(r"Solve:\s*(.*?)Answer:", model_answer, re.DOTALL)

            results.append({
                "question": question,
                "expected_answer": expected_answer,
                "plan": plan_match.group(1).strip() if plan_match else "",
                "solve": solve_match.group(1).strip() if solve_match else "",
                "generated_answer": final_answer,
                "correct": is_correct
            })
        else:
            results.append({
                "question": question,
                "expected_answer": expected_answer,
                "reasoning": reasoning,
                "generated_answer": final_answer,
                "correct": is_correct
            })

        if (i+1) % 15 == 0:
            print(f"Delaying for 1 minute after {i+1} iterations...")
            time.sleep(60)

    return results, correct_count
# main.py - processing aqua dataset
def process_aqua(dataset, prompt_fn, technique):
    results = []
    correct_count = 0

    for i, entry in enumerate(dataset):
        question = entry["question"]
        options = entry["options"]
        expected_choice = entry["correct"]

        prompt = prompt_fn(question, options)
        print(f"[{i+1}] AQUA: {question[:60]}...")

        model_answer = generate_answer(prompt)

        # Ekstrak pilihan jawaban akhir
        choice_match = re.search(r"Answer:\s*([A-E])", model_answer)
        predicted_choice = choice_match.group(1) if choice_match else ""

        is_correct = predicted_choice == expected_choice
        if is_correct:
            correct_count += 1

        # Handle output format tergantung teknik
        if technique == "aqua-plan-and-solve":
            # Ambil seluruh reasoning sebelum "Answer:"
            reasoning_match = re.search(r"(.*)Answer:\s*[A-E]", model_answer, re.DOTALL)
            reasoning_text = reasoning_match.group(1).strip() if reasoning_match else model_answer.strip()

            results.append({
                "question": question,
                "options": options,
                "plan-and-solve": reasoning_text,
                "generated_answer": predicted_choice,
                "expected_answer": expected_choice,
                "correct": is_correct
            })
        else:
            # Default untuk few-shot dan lainnya
            plan_match = re.search(r"Plan:\s*(.*?)(Solve:|Answer:)", model_answer, re.DOTALL | re.IGNORECASE)
            solve_match = re.search(r"Solve:\s*(.*?)(Answer:)", model_answer, re.DOTALL | re.IGNORECASE)

            plan = plan_match.group(1).strip() if plan_match else ""
            solve = solve_match.group(1).strip() if solve_match else ""

            results.append({
                "question": question,
                "options": options,
                "plan": plan,
                "solve": solve,
                "generated_answer": predicted_choice,
                "expected_answer": expected_choice,
                "correct": is_correct
            })

        if (i+1) % 15 == 0:
            print(f"Delaying for 1 minute after {i+1} iterations...")
            time.sleep(60)

    return results, correct_count


def main():
    args = parse_args()
    technique = args.technique
    dataset_type = args.dataset_type
    prompt_fn = TEMPLATE_MAP[technique]
    dataset = load_json(args.dataset)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    if dataset_type == "gsm8k":
        results, correct_count = process_gsm8k(dataset, prompt_fn, technique)
    elif dataset_type == "aqua":
        results, correct_count = process_aqua(dataset, prompt_fn, technique)
    elif dataset_type == "lastletter":
        results, correct_count = process_lastletter(dataset, prompt_fn, technique)
    else:
        raise ValueError("Unsupported dataset type")

    accuracy = correct_count / len(results) * 100
    print(f"\n✅ Accuracy: {correct_count}/{len(results)} correct → {accuracy:.2f}%")
    save_json(results, args.output)

if __name__ == "__main__":
    main()
