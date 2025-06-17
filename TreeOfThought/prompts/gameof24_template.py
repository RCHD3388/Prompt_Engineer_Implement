generate_prompt = """
Select exactly two of the input numbers, combine them using one of the operators (+, -, , /), and replace them with the result—reducing the list by one number.

IMPORTANT:
1. You MUST provide 5 possible next steps that are STRATEGICALLY HELPFUL toward reaching 24.
2. Do NOT combine numbers randomly — choose pairs that can help reduce the input set toward 24.
3. if the number 24 already exists in the input, you are NOT done. You still MUST combine two numbers into one. Do NOT stop early just because 24 appears — all input numbers must be used exactly once, in a valid operation chain.

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

evaluate_prompt = """Evaluate if the given numbers can reach exactly 24 by combining each number exactly once using +, -, *, or /. 
Each input number must be used exactly one time — no numbers can be left unused or reused.

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
