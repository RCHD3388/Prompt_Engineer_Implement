# prompts/templates.py

def basic_math_template(question: str) -> str:
    return f"""
You are a helpful and accurate math problem solver.

Question:
{question}

Provide only the final numerical answer.
"""

def plan_and_solve_template(question: str) -> str:
    return f"""
You are a helpful and logical math tutor. When solving a math problem, follow these steps:

1. First create a plan with bullet points.
2. Then solve the problem step-by-step.
3. Finally, output the final answer in the format: Answer: <FINAL ANSWER MUST BE NUMBER ONLY>.

Question:
{question}

Plan:
- 

Solve:
"""

def plan_and_solve_fewshot_template(question: str) -> str:
    few_shot_examples = """
You are a logical and helpful math tutor. For each question, follow this format:

Plan:
- step 1
- step 2
...

Solve:
<detailed solution steps>

Answer: <final numeric answer>

---

Question: Jamie buys 3 pens for $2 each and a notebook for $4. What is the total cost?

Plan:
- Calculate cost of pens.
- Add cost of notebook.

Solve:
3 pens × $2 = $6
$6 + $4 = $10

Answer: 10

---

Question: A box contains 5 red balls, 3 green balls, and 2 blue balls. How many total balls are there?

Plan:
- Add all the balls.

Solve:
5 + 3 + 2 = 10

Answer: 10

---

Question: {question}

Plan:
- 
"""
    return few_shot_examples.strip().replace("{question}", question)

def aqua_plan_and_solve_template(question: str, options: list[str]) -> str:
    options_text = "\n".join(options)
    return f"""
You are a helpful and logical math tutor. For the following multiple-choice math question, follow these steps:
1. **Analyze** the question carefully and determine the key values.
2. **Plan** how to solve the question using logical steps.
3. **Solve** the problem step-by-step with clarity.
4. At the end, clearly write your final answer in the format: Answer: <MUST BE FINAL OPTION LETTER ONLY>

Question:
{question}

Options:
{options_text}

Begin your solution:

Plan:
- 
""".strip()

def aqua_plan_and_solve_fewshot_template(question: str, options: list[str]) -> str:
    options_text = "\n".join(options)
    few_shot_examples = """
You are a logical and accurate math tutor. For each multiple-choice math problem, follow this format:
- First write a step-by-step plan
- Then solve the question
- Then select the correct answer using: Answer: <option letter>

---

Question: Sarah has 5 pencils. She gives 2 to her friend. How many does she have left?

Options:
A) 1
B) 2
C) 3
D) 4
E) 5

Plan:
- Start with total pencils
- Subtract the number she gave away

Solve:
5 - 2 = 3

Answer: C

---

Question: {question}

Options:
{options_text}

Plan:
- 
""".strip()
    return few_shot_examples.replace("{question}", question).replace("{options_text}", options_text)

def lastletter_plan_and_solve(question: str) -> str:

    return f"""
You are a helpful and logical assistant. When solving a word problem, follow these steps:

1. First create a plan with bullet points.
2. Then solve the problem step-by-step.
3. Finally, output the final answer in the format: Answer: <FINAL ANSWER MUST BE A LOWERCASE STRING>.

Question:
{question}

Plan:
- 
Solve:
""".strip()

def lastletter_plan_and_solve_fewshot(question: str) -> str:
    few_shot_examples = """
You are a logical and helpful assistant. For each string manipulation task, follow this format:

Plan:
- Break the sentence into individual words.
- Take the last letter of each word.
- Concatenate the letters.
- Convert to lowercase if needed.

Solve:
Whitney Erika Tj Benito → ["Whitney", "Erika", "Tj", "Benito"]
Last letters → ["y", "a", "j", "o"]
Concatenate → "yajo"

Answer: yajo

---

Question: Lucky Mireya Jj Kc

Plan:
- Break the sentence into individual words.
- Take the last letter of each word.
- Concatenate the letters.
- Convert to lowercase if needed.

Solve:
Lucky Mireya Jj Kc → ["Lucky", "Mireya", "Jj", "Kc"]
Last letters → ["y", "a", "j", "c"]
Concatenate → "yajc"

Answer: yajc

---

Question: Caleb Chase Eleazar Chanel

Plan:
- Break the sentence into individual words.
- Take the last letter of each word.
- Concatenate the letters.
- Convert to lowercase if needed.

Solve:
Caleb Chase Eleazar Chanel → ["Caleb", "Chase", "Eleazar", "Chanel"]
Last letters → ["b", "e", "r", "l"]
Concatenate → "berl"

Answer: berl

---

Question: {question}

Plan:
- 
""".strip()
    return few_shot_examples.replace("{question}", question)