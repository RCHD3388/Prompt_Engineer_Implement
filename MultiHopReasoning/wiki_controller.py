from utils.io_utils import load_json, save_json
from utils.gemini_client import generate_answer
import prompts.wiki.template as wiki_template
import re
import os
import time
import json
import ast

class WikiController:
    def __init__(self):
        self.dataset = load_json('dataset/2wiki.json')

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

    def get_generated_answer(self, ans):
        if "Answer:" in ans:
            process_answer = ans.split("Answer: ", 1)[1].strip()
        else:
            process_answer = ans.strip()
        return process_answer

    def clean_text(self, text):
        return re.sub(r'\(.*?\)|\[.*?\]', '', text).strip()

    def get_references(self, qs): 
        references = re.findall(r'#(\d+)', qs)
        return [int(ref) for ref in references]

    def get_references_array(self, qs, result_answers):
        references = result_answers[self.get_references(qs)[0]-1]
        array_ver = json.loads(references)
        return array_ver
    
    def implic_RAG(self, question, entry):
        formatted_context_list = self.get_formatted_context(entry)
        fulltext_context = ""
        for context in formatted_context_list:
            fulltext_context += context

        prompt = wiki_template.impli_rag_template.replace('{question}', question).replace('{context}', fulltext_context)
        generated_ans = generate_answer(prompt)
        
        start = generated_ans.find("C1:")
        extracted_output = generated_ans[start:]

        return extracted_output
        

    def chain_processing(self, qs_lines, entry):
        result_answers = []

        for index, qs in enumerate(qs_lines):
            # Cari yang dalam tanda kurung bulat (command)
            command_match = re.search(r"\[(.*?)\]", qs)
            command = command_match.group(1) if command_match else ''

            process_answer = ""

            if command == "get_ent_qa":
                formatted_qs = self.replace_references(qs, result_answers)
                prompt = wiki_template.get_ent_qa_template.replace('{input}', formatted_qs).replace('{context}', entry['question'])
                generated_ans = generate_answer(prompt)
                print(f"Generated answer for get_ent_qa: {generated_ans}")
                process_answer = self.get_generated_answer(generated_ans)
                print(f"Processed answer for get_ent_qa: {process_answer}")
                
            elif command == "get_atr_qa":
                references = self.get_references_array(qs, result_answers)
                ans_list = []
                for ref in references:
                    # format and generate prompt template
                    formatted_qs = re.sub(r"#\d+", ref, qs)
                    cleaned_text = self.clean_text(formatted_qs)
                    print(f"Formatted question: {cleaned_text}")

                    context = self.implic_RAG(cleaned_text, entry)
                    print(f"Context: {context}\n")
                    prompt = wiki_template.get_atr_qa_template.replace('{question}', cleaned_text).replace('{context}', context)
                    
                    generated_ans = generate_answer(prompt)
                    formatted_ans = self.get_generated_answer(generated_ans)
                    ans_list.append(f"{ref} => {formatted_ans}")

                    print(ans_list)

                process_answer = ans_list
            elif command == "comp_qa":
                latest_ans = result_answers[-1]
                full_context = ""
                for ans in latest_ans:
                    full_context += f"{ans}\n"
                prompt = wiki_template.comp_qa_template.replace('{question}', qs).replace('{context}', full_context)
                generated_ans = generate_answer(prompt)
                process_answer = self.get_generated_answer(generated_ans)

                print(f"Processed answer for comp_qa: {process_answer}")
            elif command == "EOQ":
                break
            
            print(f"Processing step {index+1}: {command} -> {process_answer}")
            result_answers.append(process_answer)
            

        return result_answers

    
    def get_formatted_context(self, entry):
        formatted_data = []
        formatted_entry_context = json.loads(entry['context'])
        for index, context in enumerate(formatted_entry_context):
            fulltext = ""
            title = context[0]
            for text in context[1]:
                fulltext += text

            formatted_context_text = f"{index+1}. {title} => {fulltext}\n"
            formatted_data.append(formatted_context_text)
        
        return formatted_data

    def generate_chain(self, question):
        template = wiki_template.decomp_template
        prompt = template.replace('{input}', question)
        decomp_chain = generate_answer(prompt)
        
        qs_lines = [line.replace("QS: ", "").strip() for line in decomp_chain.splitlines() if line.startswith("QS:")]
        print(f"Decomposition chain generated: {qs_lines}")
        return qs_lines

    def solve(self):
        
        output_log = []
        score = 0      

        for entry in self.dataset:

            qs_lines = self.generate_chain(entry['question'])
            output = self.chain_processing(qs_lines, entry)

            def check_answer(output):
                return entry['answer'].lower() == output[-1].lower() if output else False

            output_log.append({
                'question': entry['question'],
                'qs_lines': qs_lines,
                "output": output,
                "is_correct": check_answer(output),
            })

            current_score = 1 if check_answer(output) else 0
            score += current_score

            save_json(output_log, 'generate_res/dummy.json')
            time.sleep(60)  # To avoid hitting rate limits

        print(f"final score: {score}")
        return True
