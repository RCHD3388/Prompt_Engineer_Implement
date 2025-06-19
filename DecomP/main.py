# main.py

from utils.io_utils import load_json, save_json
from utils.gemini_client import generate_answer
import re
import os
import argparse
import pandas as pd
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Run prompting with Gemini API.")
    parser.add_argument(
        "--output",
        type=str,
        default="generate_res/dummy.json",
        help="Output file path (default: generate_res/dummy.json)"
    )
    parser.add_argument(
        "--task",
        type=str,
        default="commaqa",
        help="Dataset type ? (default: commaqa)"
    )

    return parser.parse_args()

def get_controller(task):
    if task == "reverse":
        from reverse_controller import ReverseController
        return ReverseController()
    elif task == "lettercat":
        from lettercat_controller import LatterCatController
        return LatterCatController()
    elif task == "commaqa":
        from commaqa_controller import CommAQAController
        return CommAQAController()
    else:
        raise ValueError(f"Unsupported task: {task}")

def main():
    args = parse_args()
    print("Arguments parsed:")
    for arg, value in vars(args).items():
        print(f"{arg}: {value}")
    print("\n")

    controller = get_controller(args.task)

    # get decomposition chains
    controller.solve()
    
if __name__ == "__main__":
    main()