# commaqa_controller.py

from utils.io_utils import load_json, save_json
import prompts.commaQA.template as commaQA_template
from utils.gemini_client import generate_answer
import re
import os
import time
import json
import ast

class CommAQAController:
    def __init__(self):
        self.dataset = load_json('dataset/commaqa.json')

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
    
    def get_Qproject_values_flat_unique(self, result_array):
        return
    
    def clean_text(self, text):
        return re.sub(r'\(.*?\)|\[.*?\]', '', text).strip()

    def get_references_array(self, qs, result_answers):
        references = result_answers[self.get_references(qs)[0]-1]
        print(f"references: {references}")
        array_ver = json.loads(references)
        print(array_ver)
        return array_ver

    def get_score(self, output, entry_answer):
        ans = ast.literal_eval(output[-1])
        ans_expected = entry_answer["spans"]
        total_number = len(ans_expected)

        temp_score = 0
        for ans_exp in ans_expected:
            if ans_exp in ans:
                temp_score += 1

        return temp_score/total_number

    def simple_subtask(self, qs, prompt_template, passage=""):
        cleaned_text = self.clean_text(qs)
        prompt = prompt_template.replace('{input}', cleaned_text).replace('{passage}', passage)
        generated_ans = generate_answer(prompt)
        return self.get_generated_answer(generated_ans)
    
    def project_values_flat_unique_subtask(self, qs, result_answers, prompt_template, passage=""):
        references = self.get_references_array(qs, result_answers)
        ans_list = []
        print(f"QA Prompt References: {references}")
        for ref in references:
            # format and generate prompt template
            formatted_qs = re.sub(r"#\d+", ref, qs)
            cleaned_text = self.clean_text(formatted_qs)
            prompt = prompt_template.replace('{input}', cleaned_text).replace('{passage}', passage)
            # generate answer
            generated_ans = generate_answer(prompt)
            ans_list.append(json.loads(self.get_generated_answer(generated_ans)))

        # convert to SET DataStructure add to process answer
        ans_set_list = list(set(item for sublist in ans_list for item in sublist))
        return json.dumps(ans_set_list)

    def chain_processing(self, qs_lines, passage=""):
        result_answers = []

        for index, qs in enumerate(qs_lines):
            # Cari yang dalam tanda kurung bulat (command)
            command_match = re.search(r"\[(.*?)\]", qs)
            command = command_match.group(1) if command_match else ''
            
            # Cari yang dalam tanda kurung kotak (type)
            type_match = re.search(r"\((.*?)\)", qs)
            query_type = type_match.group(1) if type_match else ''
            process_answer = ""

            if command == "simp_qa":
                if query_type == "select":
                    process_answer = self.simple_subtask(qs, commaQA_template.simp_qa_template, passage)
                
                elif query_type == "project_values_flat_unique":
                    process_answer = self.project_values_flat_unique_subtask(qs, result_answers, commaQA_template.simp_qa_template, passage)

            elif command == "pos_qa":
                if query_type == "select":
                    process_answer = self.simple_subtask(qs, commaQA_template.pos_qa_template, passage)

                elif query_type == "project_values_flat_unique":
                    process_answer = self.project_values_flat_unique_subtask(qs, result_answers, commaQA_template.pos_qa_template, passage)
                
            elif command == "aw_qa":
                if query_type == "select":
                    process_answer = self.simple_subtask(qs, commaQA_template.aw_qa_template, passage)

                elif query_type == "project_values_flat_unique":
                    process_answer = self.project_values_flat_unique_subtask(qs, result_answers, commaQA_template.aw_qa_template, passage)

            elif command == "EOQ":
                break
            
            print(f"Processing step {index+1}: {command} -> {process_answer}")
            result_answers.append(process_answer)

        return result_answers

    def generate_chain(self, question):
        template = commaQA_template.decomp_qa_template
        prompt = template.replace('{input}', question)
        decomp_chain = generate_answer(prompt)
        
        qs_lines = [line.replace("QS: ", "").strip() for line in decomp_chain.splitlines() if line.startswith("QS:")]
        return qs_lines
    
    def solve(self):
        
        output_log = []
        score = 0

        for key, value in self.dataset.items():
          for index, entry in enumerate(value.get('qa_pairs')):
              qs_lines = self.generate_chain(entry['question'])
              print(f"PROCESS START - {key} - {index}")
              print(f"lines: {qs_lines}")
              output = self.chain_processing(qs_lines, passage=value.get('passage'))
              
              current_score = self.get_score(output, entry['answer'])
              output_log.append({
                  'passage': value.get('passage'),
                  'question': entry['question'],
                  'qs_lines': qs_lines,
                  'result': output,
                  "score": current_score
              })
              print(f"score : {current_score}\n")
              score += current_score
              save_json(output_log, 'generate_res/dummy.json')

              time.sleep(60)  # To avoid hitting rate limits       

        print(f"final score: {score}")
        return True