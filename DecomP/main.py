# # main.py

# from utils.io_utils import load_json, save_json
# from utils.gemini_client import generate_answer
# import re
# import os
# import argparse
# import pandas as pd
# import time

# def parse_args():
#     parser = argparse.ArgumentParser(description="Run prompting with Gemini API.")
#     parser.add_argument(
#         "--output",
#         type=str,
#         default="generate_res/dummy.json",
#         help="Output file path (default: generate_res/dummy.json)"
#     )
#     parser.add_argument(
#         "--dataset",
#         type=str,
#         default="writing",
#         help="Dataset type ? game24 or writing (default: writing)"
#     )
#     parser.add_argument(
#         "--n-sample",
#         type=str,
#         default="5",
#         help="Generated samples for each input (default: 5)"
#     )

#     return parser.parse_args()

# def main():
#     args = parse_args()
#     print("Arguments parsed:")
#     for arg, value in vars(args).items():
#         print(f"{arg}: {value}")
#     print("\n")
        
# if __name__ == "__main__":
#     main()

import pandas as pd

splits = {'train': 'train.json', 'validation': 'validation.json'}
df = pd.read_json("hf://datasets/khaimaitien/qa-expert-multi-hop-qa-V1.0/" + splits["train"])