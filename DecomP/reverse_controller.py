# reverse_controller.py

from utils.io_utils import load_json, save_json
import prompts.reverse.template as reverse_template
from utils.gemini_client import generate_answer
import re
import os
import time

class ReverseController:
    def __init__(self):
        self.dataset = load_json('dataset/reverse.json')

    def print_questions(self):
        """Prints all questions from the dataset."""
        for entry in self.dataset:
            print(entry['question'])

    def replace_references(self, s, result_array):
        def replacer(match):
            index = int(match.group(1))-1  # Ambil angka dari #3 misalnya
            if 0 <= index < len(result_array):
                return result_array[index]
            else:
                return f"<Invalid index #{index}>"
        
        # Ganti semua #angka dengan nilai yang sesuai
        return re.sub(r"#(\d+)", replacer, s)

    def extract_qs(self, text):
        matches = re.findall(r'.* (?:is|reverse) \"(.*)\"\.', text)
        return matches[0] if matches else ""
    
    def get_generated_answer(self, ans):
        if "Answer:" in ans:
            process_answer = ans.split("Answer: ", 1)[1].strip()
        else:
            process_answer = ans.strip()
        return process_answer

    def chain_processing(self, qs_lines):
        result_answers = []

        for index, qs in enumerate(qs_lines):
            match = re.match(r"\[(\w+)]", qs)
            match = match.group(1)
            process_answer = ""

            if match == "extract":
                process_answer = self.extract_qs(qs)

            elif match == "remove_numbers":
                formatted_qs = self.replace_references(qs, result_answers)
                rm_num_prompt = reverse_template.remove_numbers_template.replace('{input}', formatted_qs)
                generated_ans = generate_answer(rm_num_prompt)
                print(f"Generated answer for remove_numbers: {generated_ans}")
                process_answer = self.get_generated_answer(generated_ans)
            
            elif match == "reverse":
                formatted_qs = self.replace_references(qs, result_answers)
                cot_prompt = reverse_template.cot_template.replace('{input}', formatted_qs)
                print(f"COT prompt for reverse: {cot_prompt}")
                generated_ans = generate_answer(cot_prompt)
                print(f"Generated answer for reverse: {generated_ans}")
                process_answer = self.get_generated_answer(generated_ans)
            
            elif match == "join":
                formatted_qs = self.replace_references(qs, result_answers)
                join_prompt = reverse_template.join_template.replace('{input}', formatted_qs)
                generated_ans = generate_answer(join_prompt)
                process_answer = self.get_generated_answer(generated_ans)
            
            elif match == "EOQ":
                break
            
            print(f"Processing step {index+1}: {match} -> {process_answer}")
            result_answers.append(process_answer)

        return result_answers

    def generate_chain(self, question):
        template = reverse_template.decomp_chain
        prompt = template.replace('{input}', question)
        decomp_chain = generate_answer(prompt)
        
        qs_lines = [line.replace("QS: ", "").strip() for line in decomp_chain.splitlines() if line.startswith("QS:")]
        print(f"Decomposition chain generated: {qs_lines}")
        return qs_lines
    
    def solve(self):
        
        output_log = []

        for entry in self.dataset:
            
            qs_lines = self.generate_chain(entry['question'])
            output = self.chain_processing(qs_lines)
            
            output_log.append({
                'question': entry['question'],
                'qs_lines': qs_lines,
                'result': output,
                "is_correct": entry['answer']["spans"][0] == output[-1] if output else False
            })

            save_json(output_log, 'generate_res/dummy.json')
            time.sleep(60)  # To avoid hitting rate limits

        return True
