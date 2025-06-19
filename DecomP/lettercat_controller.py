from utils.io_utils import load_json, save_json
import prompts.lettercat.template as lettercat_template
from utils.gemini_client import generate_answer
import re
import os
import time
import json

class LatterCatController:
    def __init__(self):
        self.dataset = load_json('dataset/lettercat.json')

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
    
    def get_references(self, qs): 
        references = re.findall(r'#(\d+)', qs)
        return [int(ref) for ref in references]

    def get_generated_answer(self, ans):
        if "Answer:" in ans:
            process_answer = ans.split("Answer: ", 1)[1].strip()
        else:
            process_answer = ans.strip()
        return process_answer

    def chain_processing(self, qs_lines):
        result_answers = []

        for index, qs in enumerate(qs_lines):
            match = re.search(r'\[([^\]]+)\]', qs)
            match = match.group(1)
            process_answer = ""

            if match == "split":
                split_prompt = lettercat_template.split_template.replace('{input}', qs)
                generated_ans = generate_answer(split_prompt)
                print(f"Generated answer for split: {generated_ans}")
                process_answer = self.get_generated_answer(generated_ans)
            
            elif match == "str_position":
                references = self.get_references(qs)
                word_lists = json.loads(result_answers[references[0]-1])
                ans_list = []

                time.sleep(60)

                for word in word_lists:
                    formatted_qs = re.sub(r"#\d+", word, qs)
                    print("Formatted qs: ")
                    print(formatted_qs)
                    cleaned_formatted_qs = re.sub(r'\(.*?\)|\[.*?\]', '', formatted_qs).strip()
                    print("Cleaned formatted qs: ")
                    print(cleaned_formatted_qs)

                    str_pos_decomp_chain = self.generate_chain(lettercat_template.str_position_template, cleaned_formatted_qs)
                    ans_list.append(self.chain_processing(str_pos_decomp_chain)[-1])

                print(f"Split Result: {ans_list}")
                print(ans_list)
                process_answer = str(ans_list)

            elif match == "arr_position":    
                formatted_qs = self.replace_references(qs, result_answers)
                arr_pos_prompt = lettercat_template.arr_position_template.replace('{input}', formatted_qs)
                generated_ans = generate_answer(arr_pos_prompt)
                process_answer = self.get_generated_answer(generated_ans)
            
            elif match == "merge":
                formatted_qs = self.replace_references(qs, result_answers)
                print("Merge Process")
                print(formatted_qs)
                merge_prompt = lettercat_template.merge_template.replace('{input}', formatted_qs)
                generated_ans = generate_answer(merge_prompt)
                print(f"Generated answer for merge: {generated_ans}")
                process_answer = self.get_generated_answer(generated_ans)
            
            elif match == "EOQ":
                break
            
            # print(f"Processing step {index+1}: {match} -> {process_answer}")
            result_answers.append(process_answer)

        return result_answers

    def generate_chain(self, template, question):
        prompt = template.replace('{input}', question)
        decomp_chain = generate_answer(prompt)
        
        qs_lines = [line.replace("QS: ", "").strip() for line in decomp_chain.splitlines() if line.startswith("QS:")]
        return qs_lines
    
    def solve(self):
        
        output_log = []

        for entry in self.dataset:
            
            print(f"Processing question: {entry['question']}")
            template = lettercat_template.decomp_template
            qs_lines = self.generate_chain(template, entry['question'])
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
