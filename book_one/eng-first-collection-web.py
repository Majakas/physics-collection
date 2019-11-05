# coding: utf-8
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if os.path.dirname(__file__) != '':
    os.chdir(os.path.dirname(__file__))

from python_dependencies.problem_manager import ProblemManager, generatePdf


manager = ProblemManager()
manager.loadDirectory("../problems/")
manager.partitionIntoBooks()

preamble = r'''\documentclass[11pt]{article}
\usepackage{../problem-collection-web}
\usepackage[a4paper, textwidth=360pt, textheight=541.40024pt]{geometry}
\sisetup{decimalsymbol=fullstop}
\usepackage[english]{babel}

\begin{document}
'''

title_page = r'''
\begin{titlepage}
	\centering
	\vspace{10cm}
	{\sffamily\Huge \mbox{200 ESTONIAN PHYSICS OLYMPIAD}\\ PROBLEMS FROM YEARS\\ 2012 -- 2018\par}
	\vspace{1cm}
	{\Large With hints and solutions\par}
	\vfill
	{\Large Compiled by Taavet Kalda\par}
	\vspace{1cm}
	{\Large Translated by Rael Kalda}

	\vfill

	% Bottom of the page
	{\large 2018}
\end{titlepage}
'''

copyright_page = r'''
\addtocounter{page}{1}
\mbox{}\vfill

\textcopyright~Copyright: Estonian Mathematical Society, Tallinn University of Technology,
University of Tartu, authors of the problems and Taavet Kalda.
\vspace{0.5\baselineskip}

The compilation of the problem book was supported by: Estonian Mathematical Society's fund ``Benoit Mandelbroti Jälgedes'', Robert Kitt and Tallinn University of Technology.
\vspace{0.5\baselineskip}

Publisher Tallinn University of Technology's pre-study department
\newpage
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

During the assembly of the problem book, four problems were removed due to various reasons and they were replaced with problems from 2011's open physics competition.}
\newpage
\setlength{\parindent}{0pt}
'''

statements = manager.collection_one.getEngStatements()
hints = manager.collection_one.getEngHints()
solutions = manager.collection_one.getEngSolutions()

authors = r'''
\section{List of authors}

Aigar Vaigu - Aalto University and VTT Technical Research Centre of Finland\\
Andreas Valdmann - University of Tartu\\
Andres Põldaru - University of Tartu\\
Ants Remm - University of Tartu and ETH Zürich \\
Ardi Loot - University of Tartu\\
Eero Vaher - University of Tartu and Leideni University\\
Erkki Tempel - Estonian Physical Society and Pärnu Sütevaka Humanitaargümnaasium\\
Hans Daniel Kaimre - University of Tartu\\
Jaan Kalda - Tallinn University of Technology\\
Jaan Toots - University of Cambridge\\
Jonatan Kalmus - Tallinn University of Technology\\
Joonas Kalda - University of Cambridge\\
Kaur Aare Saar - University of Cambridge\\
Koit Timpmann - University of Tartu\\
Kristian Kuppart - University of Tartu\\
Madis Ollikainen - University of Tartu and ETH Zürich \\
Mihkel Heidelberg - University of Tartu and Tallinn University of Technology\\
Mihkel Kree - Marseille University and University of Tartu\\
Mihkel Pajusalu - University of Tartu and MIT\\
Mihkel Rähn - University of Tartu\\
Moorits Mihkel Muru - University of Tartu\\
Rasmus Kisel - University of Cambridge\\
Roland Matt - University of Tartu and ETH Zürich \\
Sandra Schumann - Harvardi University and University of Tartu\\
Siim Ainsaar  - University of Tartu and Tallinn University of Technology\\
Stanislav Zavjalov - University of Oxford\\
Taavet Kalda - University of Oxford\\
Taavi Pungas - University of Cambridge and University of Tartu\\
Taivo Pungas - ETH Zürich \\
Tanel Kiis - University of Tartu\\
Valter Kiisk - University of Tartu\\
Oleg Košik - University of Tartu\\
'''

footer = r'''
\end{document}'''

contents = preamble + title_page + copyright_page + table_of_contents + introduction + statements + "\\normalsize" + hints + solutions + authors + footer

file_name = 'eng-first-collection-web'

generatePdf(file_name, contents, True)


print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_one.problems):}")
