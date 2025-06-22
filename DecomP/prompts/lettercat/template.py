# prompts/lettercat/template.py

decomp_template = '''
QC: Take the last letters of the words in "Elon Musk Tesla" and concatenate them.
QS: [split] What are the words in "Elon Musk"?
QS: (project_values) [str_position] What is the last letter in "#1"?
QS: [merge] Concatenate #2 using a space.
QS: [EOQ]

QC: Take the letters at position 1 of the words in "Sundar Pichai Google" and concatenate them.
QS: [split] What are the words in "Sundar Pichai Google"?
QS: (project_values) [str_position] What is the letter at position 1 in "#1"?
QS: [merge] Concatenate #2 using a space.
QS: [EOQ]

QC: Take the letters at position 4 of the words in "Oren Etzioni AllenInstitute" and concatenate them.
QS: [split] What are the words in "Oren Etzioni AllenInstitute"?
QS: (project_values) [str_position] What is the letter at position 4 in "#1"?
QS: [merge] Concatenate #2 using a space.
QS: [EOQ]

QC: {input}

Output:
QS: <QS-1>
QS: <QS-2>
.....
QS: <QS-N>
'''

split_template = '''
Q: What are the words in "Alan Mathison Turing"?
Answer: ["Alan", "Mathison", "Turing"]

Q: What are the words in "John von Neumann"?
Answer: ["John", "von", "Neumann"]

Q: What are the letters in "Alan"?
Answer: ["A", "l", "a", "n"]

Q: What are the letters and their positions in "Mathison"?
Answer: "[(M, 1), (a, 2), (t, 3), (h, 4), (i, 5), (s, 6), (o, 7), (n, 8)]"

Q: What are the words and their positions in "Grace Brewster Murray Hopper"?
Answer: "[(Grace, 1), (Brewster, 2), (Murray, 3), (Hopper, 4)]"

Q: {input}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''

merge_template = '''
Q: Concatenate ["A", "l", "a", "n"].
Answer: "Alan"

Q: Concatenate ["b", "x", "o"] using a space.
Answer: "b x o"

Q: Concatenate ["a", "a", "g"] using a comma.
Answer: "a,a,g"

Q: Concatenate ["Alan", "Mathison", "Turing"] using a space.
Answer: "Alan Mathison Turing"

Q: Concatenate ["Allen", "Institute"].
Answer: "AllenInstitute"

Q: {input}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''

str_position_template = '''
QC: What is the letter at position 1 of the word "Augusta"?
QS: (select) [split] What are the letters and their positions in "Augusta"?
QS: (select) [arr_position] What is at position 1 in #1?
QS: [EOQ]

QC: What is the last letter of the word "Mathison"?
QS: (select) [split] What are the letters and their positions in "Mathison"?
QS: (select) [arr_position] What is the last letter in #1?
QS: [EOQ]

QC: What is the word at the position 4 in "Colorless green ideas sleep furiously"?
QS: (select) [split] What are the words and their positions in "Colorless green ideas sleep furiously"?
QS: (select) [arr_position] What is at the position 4 in #1?
QS: [EOQ]

QC: {input}

Output:
QS: <QS-1>
QS: <QS-2>
.....
QS: <QS-N>
'''

arr_position_template = '''
Q: What is at position 4 in "[("Colorless", 1), ("green", 2), ("ideas", 3), ("sleep", 4), ("furiously", 5)]"?
Answer: "sleep"

Q: What is at position 1 in "[(M, 1), (a, 2), (t, 3), (h, 4), (i, 5), (s, 6), (o, 7), (n, 8)]"?
Answer: "M"

Q: What is at the last position in "[(A, 1), (u, 2), (g, 3), (u, 4), (s, 5), (t, 6), (a, 7)]"?
Answer: "a"

Q: What is at position 1 in "[(Herbert, 1), (Alexander, 2), (Simon, 3)]"?
Answer: "Herbert"

Q: What is at last position in "[(Allen, 1), (Institute, 2), (for, 3), (Artificial, 4), (Intelligence, 5)]"?
Answer: "Intelligence"

Q: What is at position 4 in "[(A, 1), (l, 2), (e, 3), (x, 4), (a, 5), (n, 6), (d, 7), (e, 8), (r, 9)]"?
Answer: "x"

Q: {input}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''