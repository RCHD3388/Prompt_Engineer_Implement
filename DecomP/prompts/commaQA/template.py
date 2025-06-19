
decomp_qa_template = '''Generate a Question Set (QS) based on the given Question Context (QC) WITHOUT PROVIDING Answer (A). Each QS step should logically follow from the previous one, leading to the final answer, but do not include the answer. Use consistent format and tags as shown below.

What awards have movies produced by people born in 1910 won?
QS: (select) [simp_qa] Who were born in the year 1910?
QS: (project_values_flat_unique) [pos_qa] For which movies was #1 the producer?
QS: (project_values_flat_unique) [aw_qa] Which awards were given to #2?
QS: [EOQ]

QC: What movies have people from the country Stridery acted in?
QS: (select) [simp_qa] Who is from the country Stridery?
QS: (project_values_flat_unique) [pos_qa] Which movies has #1 been an actor in?
QS: [EOQ]

QC: What awards have the actors of the Erowid winning movies received?
QS: (select) [aw_qa] Which movies were given the Erowid award?
QS: (project_values_flat_unique) [pos_qa] Who are the actors in the movie #1?
QS: (project_values_flat_unique) [aw_qa] Which awards were given to #2?
QS: [EOQ]

QC: What awards did the movies directed by the Modiparity winners receive?
QS: (select) [aw_qa] Who has been awarded the Modiparity award?
QS: (project_values_flat_unique) [pos_qa] Which movies has #1 directed?
QS: (project_values_flat_unique) [aw_qa] Which awards were given to #2?
QS: [EOQ]

QC: What awards have movies written by people born in 1935 won?
QS: (select) [simp_qa] Who were born in the year 1935?
QS: (project_values_flat_unique) [pos_qa] What movies has #1 written?
QS: (project_values_flat_unique) [aw_qa] Which awards were given to #2?
QS: [EOQ]

QC: What movies have the directors from Legault directed?
QS: (select) [simp_qa] Who is from the country Legault?
QS: (project_values_flat_unique) [pos_qa] What movies has #1 been the director of?
QS: [EOQ]

QC: {input}

Output:
QS: <QS-1>
QS: <QS-2>
.....
QS: <QS-N>    
'''

pos_qa_template = '''
movie: Premercy ; directed by: Muntaril. movie: Skirtsicine ; director: Teeplemole. movie: Featsaw ; directed by: Monsterscar. movie: Zalate ; director: Monsterscar. movie: Zalate ; awarded: Hallowcock. movie: Featsaw ; awarded: Zorgion. movie: Premercy ; award: Chowwurst. movie: Skirtsicine ; award: Hallowcock. award: Goatfly ; winner: Teeplemole. person: Monsterscar ; award: Glodome. person: Muntaril ; award: Goatfly. movie: Featsaw ; release year: 1973. movie: Zalate ; release year: 1964. movie: Skirtsicine ; release year: 1973. movie: Premercy ; year: 1961. Teeplemole was an actor in the movie Skirtsicine. Muntaril was an actor in the movie Skirtsicine. Monsterscar was an actor in the movie Premercy. Muntaril was an actor in the movie Featsaw. Teeplemole was an actor in the movie Zalate. Muntaril was born in the year 1910. Teeplemole was born in 1910. Monsterscar was born in 1942. Teeplemole is from the country of Piperfish. Monsterscar is from the country of Piperfish. Muntaril is from the country of Clony. Muntaril produced the movie Skirtsicine with others. Monsterscar was one of the producers of the movie Featsaw. Monsterscar produced the movie Premercy with others. Monsterscar produced the movie Zalate with others. Teeplemole was one of the producers of the movie Featsaw. Teeplemole produced the movie Zalate with others. Muntaril produced the movie Premercy with others. Monsterscar wrote for the movie Premercy. Muntaril was one of the writers for the movie Zalate. Muntaril wrote for the movie Featsaw. Teeplemole wrote for the movie Featsaw. Monsterscar was one of the writers for the movie Zalate. Teeplemole was one of the writers for the movie Skirtsicine.
Q: For which movies was Teeplemole the producer?
Answer: ["Featsaw", "Zalate"]

Q: For which movies was Muntaril the producer?
Answer: ["Premercy]

movie: Nilitude ; director: Monsterscar. movie: Dewbar ; directed by: Metatoun. movie: Warpstone ; directed by: Gastrat. movie: Partnershipmaker ; director: Metatoun. movie: Dewbar ; award: Tachychronograph. movie: Partnershipmaker ; awarded: Tachychronograph. movie: Nilitude ; award: Paleodactyl. movie: Warpstone ; award: Sabonade. person: Gastrat ; award: Trifogation. award: Polyquadrase ; winner: Monsterscar. award: Trifogation ; winner: Metatoun. movie: Warpstone ; release year: 1956. movie: Dewbar ; release year: 1984. movie: Nilitude ; year: 1984. movie: Partnershipmaker ; year: 1962. Gastrat was an actor in the movie Partnershipmaker. Metatoun was an actor in the movie Partnershipmaker. Metatoun was an actor in the movie Nilitude. Gastrat acted in the movie Nilitude. Monsterscar was an actor in the movie Dewbar. Gastrat acted in the movie Warpstone. Metatoun acted in the movie Warpstone. Metatoun was born in 1939. Gastrat was born in the year 1933. Monsterscar was born in 1933. Metatoun grew up in the nation of Moulole. Gastrat is from the country of Stridery. Monsterscar grew up in the nation of Moulole. Monsterscar produced the movie Nilitude with others. Monsterscar was one of the producers of the movie Warpstone. Metatoun was one of the producers of the movie Warpstone. Gastrat was one of the producers of the movie Nilitude. Metatoun produced the movie Partnershipmaker with others. Metatoun produced the movie Dewbar with others. Monsterscar was one of the producers of the movie Partnershipmaker. Gastrat produced the movie Dewbar with others. Metatoun wrote for the movie Partnershipmaker. Gastrat wrote for the movie Warpstone. Gastrat was one of the writers for the movie Dewbar. Monsterscar was one of the writers for the movie Nilitude. Metatoun wrote for the movie Warpstone.
Q: Which movies has Gastrat been an actor in?
Answer: ["Partnershipmaker", "Nilitude", "Warpstone"]

Q: Which movies has Monsterscar been an actor in?
Answer: ["Dewbar"]

movie: Pastillobox ; directed by: Firmline. movie: Clenestration ; directed by: Carblock. movie: Pestok ; directed by: Bioperatology. movie: Vitrilateral ; director: Bioperatology. movie: Vitrilateral ; award: Antipositive. movie: Clenestration ; awarded: Handt. movie: Pastillobox ; awarded: Handt. movie: Pestok ; awarded: Gutney. movie: Pestok ; writer: Firmline. movie: Clenestration ; written by: Carblock. movie: Pastillobox ; written by: Bioperatology. movie: Pestok ; writer: Bioperatology. movie: Clenestration ; written by: Firmline. movie: Vitrilateral ; writer: Bioperatology. movie: Pastillobox ; writer: Carblock. movie: Vitrilateral ; written by: Carblock. movie: Pestok ; release year: 1986. movie: Clenestration ; year: 1986. movie: Vitrilateral ; year: 1999. movie: Pastillobox ; release year: 1984. Carblock was an actor in the movie Pastillobox. Firmline was an actor in the movie Vitrilateral. Bioperatology was an actor in the movie Clenestration. Firmline acted in the movie Pastillobox. Carblock was an actor in the movie Clenestration. Bioperatology was an actor in the movie Pestok. Firmline was born in the year 1904. Bioperatology was born in the year 1935. Carblock was born in 1935. Carblock grew up in the nation of Knoppock. Firmline grew up in the nation of Tatkin. Bioperatology grew up in the nation of Tatkin. Bioperatology won the Modiparity award. Halfbill was awarded to Firmline. Halfbill was awarded to Carblock. Bioperatology was one of the producers of the movie Pestok. Bioperatology produced the movie Vitrilateral with others. Firmline produced the movie Pastillobox with others. Firmline produced the movie Clenestration with others. Carblock was one of the producers of the movie Pastillobox. Carblock produced the movie Vitrilateral with others. Carblock produced the movie Clenestration with others. Firmline was one of the producers of the movie Pestok.
Q: Which movies has Bioperatology directed?
Answer: ["Pestok", "Vitrilateral"]

Q: Which movies has Carblock directed?
Answer: ["Clenestration"]

movie: Nohit ; director: Mimicocycle. movie: Noenometer ; director: Mimicocycle. movie: Tayenne ; directed by: Zayage. movie: Pneumodendron ; director: Sclerocybin. movie: Tayenne ; awarded: Goosehead. movie: Nohit ; awarded: Handt. movie: Pneumodendron ; award: Handt. movie: Noenometer ; awarded: Brownbeard. movie: Nohit ; writer: Mimicocycle. movie: Noenometer ; written by: Sclerocybin. movie: Tayenne ; writer: Sclerocybin. movie: Pneumodendron ; written by: Zayage. movie: Tayenne ; writer: Zayage. movie: Pneumodendron ; written by: Mimicocycle. movie: Noenometer ; release year: 1991. movie: Tayenne ; year: 2013. movie: Nohit ; year: 2005. movie: Pneumodendron ; year: 2005. Mimicocycle was an actor in the movie Tayenne. Zayage acted in the movie Pneumodendron. Zayage was an actor in the movie Nohit. Sclerocybin was an actor in the movie Nohit. Sclerocybin was an actor in the movie Tayenne. Mimicocycle was an actor in the movie Noenometer. Zayage was born in 1935. Sclerocybin was born in 1935. Mimicocycle was born in 1930. Mimicocycle is from the country of Calderita. Sclerocybin grew up in the nation of Calderita. Zayage is from the country of Obility. Quinion was awarded to Zayage. Fannyxist was awarded to Sclerocybin. Fannyxist was awarded to Mimicocycle. Mimicocycle produced the movie Nohit with others. Zayage was one of the producers of the movie Nohit. Sclerocybin was one of the producers of the movie Tayenne. Sclerocybin produced the movie Pneumodendron with others. Zayage produced the movie Pneumodendron with others. Mimicocycle was one of the producers of the movie Tayenne. Sclerocybin was one of the producers of the movie Noenometer. Zayage produced the movie Noenometer with others
Q: What movies has Sclerocybin written?
Answer: ["Noenometer", "Tayenne"]

Q: What movies has Zayage written?
Answer: ["Pneumodendron", "Tayenne"]

Input: 
{passage}
Q: {input}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''

aw_qa_template = '''
movie: Premercy ; directed by: Muntaril. movie: Skirtsicine ; director: Teeplemole. movie: Featsaw ; directed by: Monsterscar. movie: Zalate ; director: Monsterscar. movie: Zalate ; awarded: Hallowcock. movie: Featsaw ; awarded: Zorgion. movie: Premercy ; award: Chowwurst. movie: Skirtsicine ; award: Hallowcock. award: Goatfly ; winner: Teeplemole. person: Monsterscar ; award: Glodome. person: Muntaril ; award: Goatfly. movie: Featsaw ; release year: 1973. movie: Zalate ; release year: 1964. movie: Skirtsicine ; release year: 1973. movie: Premercy ; year: 1961. Teeplemole was an actor in the movie Skirtsicine. Muntaril was an actor in the movie Skirtsicine. Monsterscar was an actor in the movie Premercy. Muntaril was an actor in the movie Featsaw. Teeplemole was an actor in the movie Zalate. Muntaril was born in the year 1910. Teeplemole was born in 1910. Monsterscar was born in 1942. Teeplemole is from the country of Piperfish. Monsterscar is from the country of Piperfish. Muntaril is from the country of Clony. Muntaril produced the movie Skirtsicine with others. Monsterscar was one of the producers of the movie Featsaw. Monsterscar produced the movie Premercy with others. Monsterscar produced the movie Zalate with others. Teeplemole was one of the producers of the movie Featsaw. Teeplemole produced the movie Zalate with others. Muntaril produced the movie Premercy with others. Monsterscar wrote for the movie Premercy. Muntaril was one of the writers for the movie Zalate. Muntaril wrote for the movie Featsaw. Teeplemole wrote for the movie Featsaw. Monsterscar was one of the writers for the movie Zalate. Teeplemole was one of the writers for the movie Skirtsicine.
Q: Which awards were given to Zalate?
Answer: ["Hallowcock"]

Q: Which awards were given to Premercy?
Answer: ["Chowwurst"]

movie: Misgendery ; directed by: Wetherality. movie: Dewbar ; director: Gigabut. movie: Caudacite ; director: Lougerière. movie: Tayenne ; directed by: Lougerière. movie: Misgendery ; awarded: Microsouenesis. movie: Dewbar ; awarded: Erowid. movie: Tayenne ; awarded: Cockspit. movie: Caudacite ; award: Erowid. award: Aniconder ; winner: Wetherality. award: Aniconder ; winner: Lougerière. person: Gigabut ; award: Trifogation. movie: Dewbar ; release year: 1991. movie: Tayenne ; year: 2013. movie: Caudacite ; release year: 2008. movie: Misgendery ; year: 1991. Wetherality was an actor in the movie Dewbar. Gigabut was an actor in the movie Tayenne. Lougerière was an actor in the movie Tayenne. Lougerière acted in the movie Caudacite. Lougerière acted in the movie Misgendery. Gigabut was an actor in the movie Caudacite. Wetherality was an actor in the movie Misgendery. Wetherality was born in the year 1917. Lougerière was born in 1926. Gigabut was born in the year 1917. Gigabut grew up in the nation of Triclops. Lougerière is from the country of Tatkin. Wetherality grew up in the nation of Tatkin. Lougerière produced the movie Dewbar with others. Gigabut produced the movie Tayenne with others. Gigabut produced the movie Dewbar with others. Lougerière was one of the producers of the movie Misgendery. Wetherality was one of the producers of the movie Caudacite. Gigabut was one of the producers of the movie Caudacite. Wetherality produced the movie Misgendery with others. Wetherality produced the movie Tayenne with others. Wetherality wrote for the movie Tayenne. Gigabut wrote for the movie Misgendery. Lougerière was one of the writers for the movie Caudacite. Wetherality wrote for the movie Misgendery. Gigabut wrote for the movie Tayenne. Gigabut wrote for the movie Dewbar. Lougerière wrote for the movie Dewbar. Wetherality wrote for the movie Caudacite.
Q: Which movies were given the Erowid award?
Answer: ["Dewbar", "Caudacite"]

Q: Which awards were given to Wetherality?
Answer: ["Aniconder"]

movie: Pastillobox ; directed by: Firmline. movie: Clenestration ; directed by: Carblock. movie: Pestok ; directed by: Bioperatology. movie: Vitrilateral ; director: Bioperatology. movie: Vitrilateral ; award: Antipositive. movie: Clenestration ; awarded: Handt. movie: Pastillobox ; awarded: Handt. movie: Pestok ; awarded: Gutney. movie: Pestok ; writer: Firmline. movie: Clenestration ; written by: Carblock. movie: Pastillobox ; written by: Bioperatology. movie: Pestok ; writer: Bioperatology. movie: Clenestration ; written by: Firmline. movie: Vitrilateral ; writer: Bioperatology. movie: Pastillobox ; writer: Carblock. movie: Vitrilateral ; written by: Carblock. movie: Pestok ; release year: 1986. movie: Clenestration ; year: 1986. movie: Vitrilateral ; year: 1999. movie: Pastillobox ; release year: 1984. Carblock was an actor in the movie Pastillobox. Firmline was an actor in the movie Vitrilateral. Bioperatology was an actor in the movie Clenestration. Firmline acted in the movie Pastillobox. Carblock was an actor in the movie Clenestration. Bioperatology was an actor in the movie Pestok. Firmline was born in the year 1904. Bioperatology was born in the year 1935. Carblock was born in 1935. Carblock grew up in the nation of Knoppock. Firmline grew up in the nation of Tatkin. Bioperatology grew up in the nation of Tatkin. Bioperatology won the Modiparity award. Halfbill was awarded to Firmline. Halfbill was awarded to Carblock. Bioperatology was one of the producers of the movie Pestok. Bioperatology produced the movie Vitrilateral with others. Firmline produced the movie Pastillobox with others. Firmline produced the movie Clenestration with others. Carblock was one of the producers of the movie Pastillobox. Carblock produced the movie Vitrilateral with others. Carblock produced the movie Clenestration with others. Firmline was one of the producers of the movie Pestok.
Q: Who has been awarded the Modiparity award?
Answer: ["Bioperatology"]

Q: Which awards were given to Vitrilateral?
Answer: ["Antipositive"]

movie: Nohit ; director: Mimicocycle. movie: Noenometer ; director: Mimicocycle. movie: Tayenne ; directed by: Zayage. movie: Pneumodendron ; director: Sclerocybin. movie: Tayenne ; awarded: Goosehead. movie: Nohit ; awarded: Handt. movie: Pneumodendron ; award: Handt. movie: Noenometer ; awarded: Brownbeard. movie: Nohit ; writer: Mimicocycle. movie: Noenometer ; written by: Sclerocybin. movie: Tayenne ; writer: Sclerocybin. movie: Pneumodendron ; written by: Zayage. movie: Tayenne ; writer: Zayage. movie: Pneumodendron ; written by: Mimicocycle. movie: Noenometer ; release year: 1991. movie: Tayenne ; year: 2013. movie: Nohit ; year: 2005. movie: Pneumodendron ; year: 2005. Mimicocycle was an actor in the movie Tayenne. Zayage acted in the movie Pneumodendron. Zayage was an actor in the movie Nohit. Sclerocybin was an actor in the movie Nohit. Sclerocybin was an actor in the movie Tayenne. Mimicocycle was an actor in the movie Noenometer. Zayage was born in 1935. Sclerocybin was born in 1935. Mimicocycle was born in 1930. Mimicocycle is from the country of Calderita. Sclerocybin grew up in the nation of Calderita. Zayage is from the country of Obility. Quinion was awarded to Zayage. Fannyxist was awarded to Sclerocybin. Fannyxist was awarded to Mimicocycle. Mimicocycle produced the movie Nohit with others. Zayage was one of the producers of the movie Nohit. Sclerocybin was one of the producers of the movie Tayenne. Sclerocybin produced the movie Pneumodendron with others. Zayage produced the movie Pneumodendron with others. Mimicocycle was one of the producers of the movie Tayenne. Sclerocybin was one of the producers of the movie Noenometer. Zayage produced the movie Noenometer with others
Q: Which awards were given to Tayenne?
Answer: ["Goosehead"]

Q: Which awards were given to Noenometer?
Answer: ["Brownbeard"]

Input: 
{passage}
Q: {input}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''

simp_qa_template = '''
movie: Premercy ; directed by: Muntaril. movie: Skirtsicine ; director: Teeplemole. movie: Featsaw ; directed by: Monsterscar. movie: Zalate ; director: Monsterscar. movie: Zalate ; awarded: Hallowcock. movie: Featsaw ; awarded: Zorgion. movie: Premercy ; award: Chowwurst. movie: Skirtsicine ; award: Hallowcock. award: Goatfly ; winner: Teeplemole. person: Monsterscar ; award: Glodome. person: Muntaril ; award: Goatfly. movie: Featsaw ; release year: 1973. movie: Zalate ; release year: 1964. movie: Skirtsicine ; release year: 1973. movie: Premercy ; year: 1961. Teeplemole was an actor in the movie Skirtsicine. Muntaril was an actor in the movie Skirtsicine. Monsterscar was an actor in the movie Premercy. Muntaril was an actor in the movie Featsaw. Teeplemole was an actor in the movie Zalate. Muntaril was born in the year 1910. Teeplemole was born in 1910. Monsterscar was born in 1942. Teeplemole is from the country of Piperfish. Monsterscar is from the country of Piperfish. Muntaril is from the country of Clony. Muntaril produced the movie Skirtsicine with others. Monsterscar was one of the producers of the movie Featsaw. Monsterscar produced the movie Premercy with others. Monsterscar produced the movie Zalate with others. Teeplemole was one of the producers of the movie Featsaw. Teeplemole produced the movie Zalate with others. Muntaril produced the movie Premercy with others. Monsterscar wrote for the movie Premercy. Muntaril was one of the writers for the movie Zalate. Muntaril wrote for the movie Featsaw. Teeplemole wrote for the movie Featsaw. Monsterscar was one of the writers for the movie Zalate. Teeplemole was one of the writers for the movie Skirtsicine.
Q: Who were born in the year 1910?
Answer: ["Teeplemole", "Muntaril"]

Q: Who is from the country Piperfish?
Answer: ["Teeplemole", "Monsterscar"]

movie: Nilitude ; director: Monsterscar. movie: Dewbar ; directed by: Metatoun. movie: Warpstone ; directed by: Gastrat. movie: Partnershipmaker ; director: Metatoun. movie: Dewbar ; award: Tachychronograph. movie: Partnershipmaker ; awarded: Tachychronograph. movie: Nilitude ; award: Paleodactyl. movie: Warpstone ; award: Sabonade. person: Gastrat ; award: Trifogation. award: Polyquadrase ; winner: Monsterscar. award: Trifogation ; winner: Metatoun. movie: Warpstone ; release year: 1956. movie: Dewbar ; release year: 1984. movie: Nilitude ; year: 1984. movie: Partnershipmaker ; year: 1962. Gastrat was an actor in the movie Partnershipmaker. Metatoun was an actor in the movie Partnershipmaker. Metatoun was an actor in the movie Nilitude. Gastrat acted in the movie Nilitude. Monsterscar was an actor in the movie Dewbar. Gastrat acted in the movie Warpstone. Metatoun acted in the movie Warpstone. Metatoun was born in 1939. Gastrat was born in the year 1933. Monsterscar was born in 1933. Metatoun grew up in the nation of Moulole. Gastrat is from the country of Stridery. Monsterscar grew up in the nation of Moulole. Monsterscar produced the movie Nilitude with others. Monsterscar was one of the producers of the movie Warpstone. Metatoun was one of the producers of the movie Warpstone. Gastrat was one of the producers of the movie Nilitude. Metatoun produced the movie Partnershipmaker with others. Metatoun produced the movie Dewbar with others. Monsterscar was one of the producers of the movie Partnershipmaker. Gastrat produced the movie Dewbar with others. Metatoun wrote for the movie Partnershipmaker. Gastrat wrote for the movie Warpstone. Gastrat was one of the writers for the movie Dewbar. Monsterscar was one of the writers for the movie Nilitude. Metatoun wrote for the movie Warpstone.
Q: Who is from the country Stridery?
Answer: ["Gastrat"]

Q: Who were born in the year 1939?
Answer: ["Metatoun"]

movie: Coacheship ; director: Metatoun. movie: Assamplifier ; director: Kapod. movie: Misapportionment ; director: Sapien. movie: Quinsid ; director: Kapod. movie: Assamplifier ; award: Zorgion. movie: Quinsid ; awarded: Airpipe. movie: Coacheship ; award: Electrodesal. movie: Misapportionment ; award: Airpipe. movie: Coacheship ; written by: Metatoun. movie: Misapportionment ; written by: Kapod. movie: Coacheship ; written by: Kapod. movie: Quinsid ; writer: Sapien. movie: Misapportionment ; written by: Metatoun. movie: Assamplifier ; written by: Kapod. movie: Assamplifier ; written by: Sapien. movie: Assamplifier ; release year: 2000. movie: Coacheship ; year: 2001. movie: Quinsid ; year: 2005. movie: Misapportionment ; year: 2005. Sapien was an actor in the movie Misapportionment. Sapien acted in the movie Assamplifier. Kapod acted in the movie Quinsid. Sapien acted in the movie Coacheship. Metatoun was an actor in the movie Quinsid. Kapod acted in the movie Misapportionment. Metatoun acted in the movie Coacheship. Kapod acted in the movie Assamplifier. Sapien was born in the year 1910. Metatoun was born in 1928. Kapod was born in the year 1910. Metatoun is from the country of Legault. Kapod grew up in the nation of Tatkin. Sapien is from the country of Legault. Malwarp was awarded to Sapien. Metatoun won the Monkeynote award. Kapod won the Monkeynote award. Kapod was one of the producers of the movie Quinsid. Metatoun was one of the producers of the movie Misapportionment. Metatoun was one of the producers of the movie Quinsid. Sapien was one of the producers of the movie Assamplifier. Sapien produced the movie Coacheship with others. Metatoun was one of the producers of the movie Assamplifier. Kapod was one of the producers of the movie Misapportionment. Kapod was one of the producers of the movie Coacheship.
Q: Who is from the country Legault?
Answer: ["Metatoun", "Sapien"]

Q: Who were born in the year 1910?
Answer: ["Kapod", "Sapien"]

movie: Nohit ; director: Mimicocycle. movie: Noenometer ; director: Mimicocycle. movie: Tayenne ; directed by: Zayage. movie: Pneumodendron ; director: Sclerocybin. movie: Tayenne ; awarded: Goosehead. movie: Nohit ; awarded: Handt. movie: Pneumodendron ; award: Handt. movie: Noenometer ; awarded: Brownbeard. movie: Nohit ; writer: Mimicocycle. movie: Noenometer ; written by: Sclerocybin. movie: Tayenne ; writer: Sclerocybin. movie: Pneumodendron ; written by: Zayage. movie: Tayenne ; writer: Zayage. movie: Pneumodendron ; written by: Mimicocycle. movie: Noenometer ; release year: 1991. movie: Tayenne ; year: 2013. movie: Nohit ; year: 2005. movie: Pneumodendron ; year: 2005. Mimicocycle was an actor in the movie Tayenne. Zayage acted in the movie Pneumodendron. Zayage was an actor in the movie Nohit. Sclerocybin was an actor in the movie Nohit. Sclerocybin was an actor in the movie Tayenne. Mimicocycle was an actor in the movie Noenometer. Zayage was born in 1935. Sclerocybin was born in 1935. Mimicocycle was born in 1930. Mimicocycle is from the country of Calderita. Sclerocybin grew up in the nation of Calderita. Zayage is from the country of Obility. Quinion was awarded to Zayage. Fannyxist was awarded to Sclerocybin. Fannyxist was awarded to Mimicocycle. Mimicocycle produced the movie Nohit with others. Zayage was one of the producers of the movie Nohit. Sclerocybin was one of the producers of the movie Tayenne. Sclerocybin produced the movie Pneumodendron with others. Zayage produced the movie Pneumodendron with others. Mimicocycle was one of the producers of the movie Tayenne. Sclerocybin was one of the producers of the movie Noenometer. Zayage produced the movie Noenometer with others
Q: Who were born in the year 1935?
Answer: ["Sclerocybin", "Zayage"]

Q: Who is from the country Obility?
Answer: ["Zayage"]

Input: 
{passage}
Q: {input}

Output (your answer MUST be in the same format "Answer: <your answer here>", you MUST add "Answer: " before your answer):
Answer: <your answer here>
'''