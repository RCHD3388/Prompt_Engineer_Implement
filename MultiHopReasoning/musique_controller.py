# musique_controller.py

from utils.io_utils import load_json, save_json
from utils.gemini_client import generate_answer
import prompts.musique.template as musique_template
import re
import os
import time
import json
import ast

class MusiqueController:
    def __init__(self):
        self.dataset = load_json('dataset/musique.json')

    def print_questions(self):
        """Prints all questions from the dataset."""
        for entry in self.dataset:
            print(entry['question'])

    def get_generated_answer(self, ans):
        if "Answer:" in ans:
            process_answer = ans.split("Answer: ", 1)[1].strip()
        else:
            process_answer = ans.strip()
        return process_answer
    
    def get_fullcontext (self, paragraphs):
        fulltext_context = ""
        for index, paragraph in enumerate(paragraphs):
            fulltext_context += f"{paragraph['title']} => {paragraph['paragraph_text']}\n"
        return fulltext_context

    def implic_RAG(self, question, paragraphs):
        
        fulltext_context = self.get_fullcontext(paragraphs)

        prompt = musique_template.impli_rag_template.replace('{question}', question).replace('{context}', fulltext_context)
        generated_ans = generate_answer(prompt)

        start = generated_ans.find("C1:")
        extracted_output = generated_ans[start:]

        output_lines = extracted_output.splitlines()
        output_cleaned = [line.split(":", 1)[-1].strip() for line in output_lines]

        # Gabungkan kembali konteks menjadi string yang bersih
        cleaned_output = "\n".join(output_cleaned)

        return cleaned_output

    def chain_processing(self, qs_lines, paragraphs):
        result_answers = []

        for index, qs in enumerate(qs_lines):
            process_answer = ""
            
            if index == 0:
                context = self.get_fullcontext(paragraphs)
                
                prompt = musique_template.starter_qa.replace('{question}', qs['question']).replace('{context}', context)
                generated_ans = generate_answer(prompt)
                process_answer = self.get_generated_answer(generated_ans)

            else:
                prev_ans = result_answers[-1]
                context = self.get_fullcontext(paragraphs)

                formatted_qs = re.sub(r"#\d+", prev_ans, qs['question'])

                prompt = musique_template.finisher_template.replace('{question}', formatted_qs).replace('{context}', context)
                generated_ans = generate_answer(prompt)
                process_answer = self.get_generated_answer(generated_ans)

            result_answers.append(process_answer)
        return result_answers

    
    def solve(self):
        
        output_log = []
        score = 0      

        for entry in self.dataset:
            
            output = self.chain_processing(entry['question_decomposition'], entry['paragraphs'])
            print("processing index: ", entry['id'])
            output_log.append({
                'question': entry['question'],
                'qs_lines': entry['question_decomposition'],
                'result': output,
                'expected_answer': entry['answer'],
                "is_correct": entry['answer'].lower() == output[-1].lower()
            })

            # break
            save_json(output_log, 'generate_res/dummy.json')
            time.sleep(20)  # To avoid hitting rate limits

        print(f"final score: {score}")
        return True
