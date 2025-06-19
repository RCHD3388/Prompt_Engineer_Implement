decomp_template = '''
QC: Which film came out first, The Love Route or Engal Aasan?  
QS: [get_ent_qa] Which films are being compared in the question?
QS: (foreach)[get_atr_qa] What is the release date of #1?
QS: [comp_qa] Which film came out first based on the release date?

QC: Are Matraville Sports High School and Wabash High School both located in the same country?  
QS: [get_ent_qa] Which schools are being compared in the question?
QS: (foreach)[get_atr_qa] What is the location of #1?
QS: [comp_qa] Are the schools located in the same country?

QC: Are Alison Skipper and Diane Gilliam Fisher from the same country?  
QS: [get_ent_qa] Who are the people being compared in the question?
QS: (foreach)[get_atr_qa] What is the nationality of #1?
QS: [comp_qa] Do they have the same nationality?

QC: Do the movies Bloody Birthday and The Beckoning Silence, originate from the same country?  
QS: [get_ent_qa] Which movies are being compared in the question?
QS: (foreach)[get_atr_qa] What is the country of origin of #1?
QS: [comp_qa] Do the movies originate from the same country?

QC: Are both businesses, Vakıfbank and Infopro Sdn Bhd, located in the same country?  
QS: [get_ent_qa] Which businesses are being compared in the question?
QS: (foreach)[get_atr_qa] What is the location of #1?
QS: [comp_qa] Are the businesses located in the same country?

QC: Does Mukasa Mbidde have the same nationality as Erich Maas?  
QS: [get_ent_qa] Who are the people being compared in the question?
QS: (foreach)[get_atr_qa] What is the nationality of #1?
QS: [comp_qa] Do they have the same nationality?

QC: {input}

Output:
QS: <QS-1>
QS: <QS-2>
.....
QS: <QS-N>  

'''

get_ent_qa_template = '''
QC: Are Matraville Sports High School and Wabash High School both located in the same country?  
Q: Which schools are being compared in the question?  
Answer: ["Matraville Sports High School", "Wabash High School"]

QC: Are Alison Skipper and Diane Gilliam Fisher from the same country?  
Q: Which people are being compared in the question?  
Answer: ["Alison Skipper", "Diane Gilliam Fisher"]

QC: Do the movies Bloody Birthday and The Beckoning Silence, originate from the same country?  
Q: Which movies are being compared in the question?  
Answer: ["Bloody Birthday", "The Beckoning Silence"]

QC: Are both businesses, Vakıfbank and Infopro Sdn Bhd, located in the same country?  
Q: Which businesses are being compared in the question?  
Answer: ["Vakıfbank", "Infopro Sdn Bhd"]

QC: Did the movies Pony Express (Film) and The Da Vinci Code (Film), originate from the same country?  
Q: Which people are being compared in the question?  
Answer: ["Sam Earle", "Felix Luckeneder"]

QC: Are Sam Earle and Felix Luckeneder from the same country?  
Q: Which locations are being compared in the question?  
Answer: ["Lesser Slave Lake", "Medeweger See"]

QC: Are both Lesser Slave Lake and Medeweger See located in the same country?  
Q: Which films are being compared in the question?  
Answer: ["Alsino And The Condor", "1922 (2017 Film)"]

QC: Are Alsino And The Condor and 1922 (2017 Film) both from the same country?  
Q: Which bands are being compared in the question?  
Answer: ["Cinematic Sunrise", "Kingston Falls"]

QC: Are the movies Carnival Of Souls and Uvanga, from the same country?  
Q: Which schools are being compared in the question?  
Answer: ["St. Mary High School (Rutherford, New Jersey)", "Mother Teresa High School"]

Input:  
QC: {context}  
Q: {input}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''


get_atr_qa_template = '''
Q: {question}
Context:
{context}

Output: 
Answer: <Your answer>
'''

comp_qa_template = '''
QS: {question}
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

