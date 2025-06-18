
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

QC: {input}

Output:
QS: <QS-1>
QS: <QS-2>
.....
QS: <QS-N>    
'''