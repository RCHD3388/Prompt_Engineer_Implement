# prompts/writing_template.py

generate_sample_plan_prompt = """Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}

Make a plan only for the passage. Your output MUST be of the following format:

Plan:
paragraph 1: [write the first paragraph plan here]
paragraph 2: [write the second paragraph plan here]
paragraph 3: [write the third paragraph plan here]
paragraph 4: [write the fourth paragraph plan here]
"""


generate_sample_passage_prompt = """Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}

Write the passage based on that plan.

Plan:
{plan}

Your output should be of the following format:

Passage:
<Your output passage here>
"""


plan_vote_prompt = '''Given a creative writing plan and several proposed paragraph ideas (choices), analyze which idea aligns best with the plan in terms of coherence, creativity, relevance, and thematic fit.

Conclude with a final decision in this format:
"The best choice is {s}", where s is the integer ID of the best choice.

Choices:
{choices}
'''

passage_vote_prompt = '''Given several complete passages written based on the same creative writing prompt, analyze which passage is the most effective in terms of coherence, creativity, emotional impact, narrative consistency, and how well it fulfills the intended prompt or structure.

Evaluate each passage critically and justify your reasoning. At the end, conclude with your final decision in this format:
"The best passage is {s}", where s is the integer ID of the best passage.

Passages:
{choices}
'''

score_prompt = '''Analyze the following passage, then at the last line conclude "Thus the coherency score is {s}", where s is an integer from 1 to 10.
'''