generate_prompt = """you are only allowed to choose two input numbers to obtain a new number
you MUST provide {n_sample} possible next steps

Input: 2 8 8 14
Possible next steps:
2 + 8 = 10 (left: 8 10 14)
8 / 2 = 4 (left: 4 8 14)
14 + 2 = 16 (left: 8 8 16)
2 * 8 = 16 (left: 8 14 16)
8 - 2 = 6 (left: 6 8 14)

Input: 4 5
Possible next steps:
4 + 5 = 9 (left: 9)
5 - 4 = 1 (left: 1)
4 * 5 = 20 (left: 20)

Input: 3 6 9
Possible next steps:
3 + 6 = 9 (left: 9 9)
9 - 6 = 3 (left: 3 3)
6 * 3 = 18 (left: 9 18)

Input: {input}
Possible next steps:
"""

evaluate_prompt = """Evaluate if given numbers can reach 24 (sure/likely/impossible). 
Each number can be used only and must be used once.
input: 10 14
10 + 14 = 24
evaluate: sure

input: 11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
evaluate: impossible

input: 4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
evaluate: sure

input: 5 7 8
(8 - 5) * 7 = 3 * 7 = 21
evaluate: likely

input: 10 10 11
too big
evaluate: impossible

input: 1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
evaluate: impossible

input: {input}
...
evaluate: {answer with sure/likely/impossible}
"""

final_prompt = """Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Given an input and an answer, give a judgement (sure/impossible) if the answer is correct, i.e. it uses each input exactly once and no other numbers, and reach 24.
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) = 24
Judge: 
sure
Input: 2 9 10 12
Answer: 2 * 12 * (10 - 9) = 24
Judge: 
sure
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) + 1 = 25
Judge: 
impossible
Input: {input}
Answer: {answer}
Judge:"""
