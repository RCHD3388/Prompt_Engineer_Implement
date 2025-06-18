decomp_chain = '''Generate a Question Set (QS) based on the given Question Context (QC) WITHOUT PROVIDING Answer (A). Each QS step should logically follow from the previous one, leading to the final answer, but do not include the answer. Use consistent format and tags as shown below.

QC: Reverse the sequence "driving license, button, packet, identity card, shoe".
QS: [extract] The sequence is "1. driving license, 2. button, 3. packet, 4. identity card, 5. shoe". The sequence is 5 items long, which is more than the minimum length of 4, so we split it. Half of 5 is 5 / 2 = 2.5. Dropping the decimal, we get that the first half will be 2 items long, ending in "2. button". The first half (2 items) is "1. driving license, 2. button".
QS: [extract] The first half of the sequence ends with "2. button", so the second half starts after "2. button" with "3. packet". The full sequence is 5 items long, and the first half is 2 items long, so the second half will be 5 - 2 = 3 items long. The second half of the sequence (3 items) is "3. packet, 4. identity card, 5. shoe".
QS: [remove_numbers] Remove the numbers from #1.
QS: [remove_numbers] Remove the numbers from #2.
QS: [reverse] Reverse the sequence #3. 
QS: [reverse] Reverse the sequence #4.
QS: [join] #6 #5
QS: [EOQ]

QC: Reverse the sequence "newspaper, glasses, laptop, bottle".
QS: [extract] The sequence is "1. newspaper, 2. glasses, 3. laptop, 4. bottle". The sequence is 4 items long, which is equal to the minimum length of 4, so we split it. Half of 4 is 4 / 2 = 2.0. Dropping the decimal, we get that the first half will be 2 items long. The first half (2 items) of the sequence is "1. newspaper, 2. glasses".
QS: [extract] The first half of the sequence ends with "2. glasses", so the second half starts after "2. glasses" with "3. laptop". The full sequence is 4 items long and the first half is 2 items long, so the second half will be 4 - 2 = 2 items long, ending in "2. glasses". The second half of the sequence (2 items) is "3. laptop, 4. bottle".
QS: [remove_numbers] Remove the numbers from #1.
QS: [remove_numbers] Remove the numbers from #2.
QS: [reverse] Reverse the sequence #3. 
QS: [reverse] Reverse the sequence #4.
QS: [join] #6 #5
QS: [EOQ]

QC: {input}

Output:
QS: <QS-1>
QS: <QS-2>
.....
QS: <QS-N>
'''

join_template = '''
Q: "bottle, laptop" "glasses, newspaper".
Answer: bottle, laptop, glasses, newspaper

Q: "identity card, packet, button" "magazine, notebook, glasses".
Answer: identity card, packet, button, magazine, notebook, glasses

Q: "passport, umbrella, radio, mobile phone, photo" "player".
Answer:  passport, umbrella, radio, mobile phone, photo, player

Q: "mirror, case" "toothbrush, alarm clock".
Answer: mirror, case, toothbrush, alarm clock

Q: "light bulb, clip, umbrella" "driving licence, watch".
Answer: light bulb, clip, umbrella, driving licence, watch

Q: {input}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''

remove_numbers_template = '''
Q: Remove the numbers from "4. bottle, 3. laptop, 2. glasses, 1. newspaper".
Answer: bottle, laptop, glasses, newspaper

Q: Remove the numbers from "1. identity card, 2. packet, 3. button".
Answer: identity card, packet, button

Q: Remove the numbers from "1. player, 2. passport, 3. umbrella, 4. radio".
Answer: player, passport, umbrella, radio

Q: {input}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''

cot_template = '''
QC: Reverse the sequence "newspaper, glasses, laptop, bottle".
QS: First is newspaper. Second is glasses. Third is laptop. Fourth is bottle. Now to reverse, change the order to: Fourth is bottle. Third is laptop. Second is glasses. First is newspaper. So the answer is "bottle, laptop, glasses, newspaper".
Answer: bottle, laptop, glasses, newspaper

QC: Reverse the sequence "laptop, photo, clip".
QS: First is laptop. Second is photo. Third is clip. Now to reverse, change the order to: Third is clip. Second is photo. First is laptop. So the answer is "clip, photo, laptop".
Answer: clip, photo, laptop

QC: Reverse the sequence "driving license, button, packet, identity card, pineapple".
QS: First is driving license. Second is button. Third is packet. Fourth is identity card. Fifth is pineapple. Now to reverse, change the order to: Fifth is pineapple. Fourth is identity card. Third is packet. Second is button. First is driving license. So the answer is "pineapple, identity card, packet, button, driving license".
Answer: pineapple, identity card, packet, button, driving license

Q: {input}
QS: <your qs answer here>

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer): 
Answer: <your final answer here>
'''