# coding: utf-8
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.dirname(__file__))

from python_dependencies.problem_manager import ProblemManager, generatePdf


manager = ProblemManager()
manager.loadDirectory("../problems/")
manager.partitionIntoBooks()

preamble = r'''\documentclass[11pt]{article}
\usepackage{../problem-collection-web}
\usepackage[a4paper, textwidth=360pt, textheight=541.40024pt]{geometry}
\usepackage[estonian]{babel}

\begin{document}
'''

title_page = r'''
\begin{titlepage}
	\centering
	\vspace{10cm}
	{\sffamily\Huge \mbox{200 EESTI FÜÜSIKAOLÜMPIAADI}\\ ÜLESANNET AASTATEST\\ 2005 -- 2018\par}
	\vspace{1cm}
	{\Large koos vihjete ja lahendustega\par}
	\vfill
	{\Large Koostas Taavet Kalda}

	\vfill

	% Bottom of the page
	{\large 2019}
\end{titlepage}
'''

table_of_contents = r'''
\tableofcontents
\newpage
'''

introduction = r'''
{\setlength{\parindent}{24pt}
\section{Sissejuhatus}

Siia on koondatud 400 gümnaasiumi ülesannet Eesti füüsikaolümpiaadi piirkonnavoorudest, lõppvoorudest ja lahtistest võistlustest. Igale ülesandele on juurde kirjutatud paarilauseline vihje. Juhul kui õpilane jääb ülesannet lahendades toppama, on tal võimalik vihjet lugeda ning teisele katsele minna.

Ülesanded on jaotatud teemade kaupa ning teemasiseselt raskuse järgi. Raskustaset tähistatakse kuni viie tärniga. Ülesannete lihtsamaks otsimiseks on ülesannete numbrite ette pandud \enquote{Ü}, vihjete ette \enquote{V} ja lahenduste ette \enquote{L}. Näiteks ülesande 133 teksti number on kujul Ü133. Iga ülesande juures on kirjas ka selle autor ning olümpiaadi vooru lühinimetus, lisaks lühendid P 1, G 1 jne, kus tähed tähistavad põhikooli- ja gümnaasiumiastet. Näiteks G 9 viitab gümnaasiumiastme 9. ülesandele.
\newpage
\setlength{\parindent}{0pt}
'''

statements = manager.collection_all.getEstStatements()
hints = manager.collection_all.getEstHints()
solutions = manager.collection_all.getEstSolutions()


footer = r'''
\end{document}'''

contents = preamble + title_page + table_of_contents + introduction + statements + "\\normalsize" + hints + solutions + footer

file_name = 'terve-kogumik-veeb'

generatePdf(file_name, contents, True)


print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_all.problems):}")
