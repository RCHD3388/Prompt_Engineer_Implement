
starter_qa = '''
Input:  
Q: {question}  
Context: 
{context} 

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''

finisher_template = '''
Input: 
Q: {question}
Context: 
{context}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''

impli_rag_template = '''
Given the following context data and a specific question, please provide the top 3 most relevant contexts that help answer the question. The output should be formatted as follows:

Context:
C1: "..."
C2: "..."
C3: "..."

Context Data:
{context}

Question: {question}

Output:
C1: <Best Context>
C2: <Second Best Context>
C3: <Third Best Context>
'''