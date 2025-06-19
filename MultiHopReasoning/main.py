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
        default="musique",
        help="Dataset type ? (default: musique)"
    )

    return parser.parse_args()

def get_controller(task):
    if task == "musique":
        from musique_controller import MusiqueController
        return MusiqueController()
    elif task == "2wiki":
        from wiki_controller import WikiController
        return WikiController()
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