# coding: utf-8
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if os.path.dirname(__file__) != '':
    os.chdir(os.path.dirname(__file__))

from python_dependencies.problem_manager import ProblemManager, generate_pdf


manager = ProblemManager()
manager.load_directory("../problems/")
manager.partition_into_books()

preamble = r'''\documentclass[11pt]{article}
\usepackage{../problem-collection}

\begin{document}
\selectlanguage{english}
'''

title_page = r'''
\begin{titlepage}
	\centering
	\vspace{10cm}
	{\sffamily\Huge \mbox{200 ESTONIAN PHYSICS OLYMPIAD}\\ PROBLEMS FROM YEARS\\ 2005 -- 2011\par}
	\vspace{1cm}
	{\Large With hints and solutions\par}
	\vfill
	{\Large Compiled by Taavet Kalda\par}
	\vspace{1cm}
	{\Large Translated by ...}

	\vfill

	% Bottom of the page
\end{titlepage}
'''

table_of_contents = r'''
\tableofcontents
\newpage
'''

introduction = r'''
{\setlength{\parindent}{24pt}
\section{Introduction}

This book contains 200 high school physics problems from the regional rounds, national rounds, and the open competitions of the Estonian physics olympiads.

Each problem comes with a short hint for students who are stuck on problems but do not want to look at the solutions just yet. The topics have been sorted based on their topics and the level of difficulty. The difficulty is marked with up to five stars. To make the searching of problems easier, a prefix is attached before the problem numbers, \enquote{P} for problem statements, \enquote{H} for hints and \enquote{S} for solutions. For example, the statement of problem 133 is denoted with P133. Furthermore, the name of the author and the round are written next to the title of the problem alongside with a short abbreviation of the form P 1, G 1 etc, where the letters correspond to middle school and high school respectively. G 9 would for example stand for the ninth problem in the high school division.
}
\newpage
\setlength{\parindent}{0pt}
'''

statements = manager.collection_two.get_eng_statements()
hints = manager.collection_two.get_eng_hints()
solutions = manager.collection_two.get_eng_solutions()

footer = r'''
\end{document}'''

contents = preamble + title_page  + table_of_contents + introduction + statements + "\\normalsize" + hints + solutions + footer

file_name = 'eng-second-collection-web'

generate_pdf(file_name, contents, True)  # Set the boolean to false if you want the .tex to be compiled once


print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_one.problems):}")
