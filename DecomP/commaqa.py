from utils.io_utils import load_json, save_json

class CommAQAController:
    def __init__(self):
        self.dataset = load_json('dataset/commaqa.json')

    def print_questions(self):
        """Prints all questions from the dataset."""
        for entry in self.dataset:
            print(entry['question'])