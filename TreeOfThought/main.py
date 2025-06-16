import argparse
import os
from utils.io_utils import load_json, save_json
from prompts.tot_templates import tot_initial_prompt
from utils.gemini_client import generate_response

def parse_args():
    parser = argparse.ArgumentParser(description="Tree-of-Thought Prompting with Gemini")
    parser.add_argument("--technique", type=str, default="tot", help="Prompting technique (default: tot)")
    parser.add_argument("--dataset", type=str, required=True, help="Path to dataset (JSON)")
    parser.add_argument("--dataset-type", type=str, required=True, choices=["gsm8k", "aqua"], help="Type of dataset format")
    parser.add_argument("--output", type=str, required=True, help="Path to save generated results (JSON)")
    return parser.parse_args()

def main():
    args = parse_args()

    print(f"\n🔧 Setup ready: technique={args.technique}, dataset={args.dataset}, type={args.dataset_type}")
    print(f"📥 Output will be saved to: {args.output}")

    # Di tahap selanjutnya, proses akan disesuaikan di sini
    # data = load_json(args.dataset)
    # result = ...
    # save_json(result, args.output)

if __name__ == "__main__":
    main()
