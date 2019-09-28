# coding: utf-8
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.dirname(__file__))

from python_dependencies.problem_manager import ProblemManager, generatePdf
from python_dependencies.utils import readConfig


manager = ProblemManager()
manager.loadDirectory("../problems/")
manager.partitionIntoBooks()
config = readConfig("teine-kogumik-config.txt")

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
	{\sffamily\Huge \mbox{200 EESTI FÜÜSIKAOLÜMPIAADI}\\ ÜLESANNET AASTATEST\\ 2005 -- 2011\par}
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

Siia on koondatud 200 gümnaasiumi ülesannet Eesti füüsikaolümpiaadi piirkonnavoorudest, lõppvoorudest ja lahtistest võistlustest. Igale ülesandele on juurde kirjutatud paarilauseline vihje. Juhul kui õpilane jääb ülesannet lahendades toppama, on tal võimalik vihjet lugeda ning teisele katsele minna.

Tegu on teise kogumikuga Eesti füüsikaolümpiaadi ülesannete kogude seeriast, kus esimene kattis 200 ülesannet ajavahemikust 2012---2018.

Ülesanded on jaotatud teemade kaupa ning teemasiseselt raskuse järgi. Raskustaset tähistatakse kuni viie tärniga. Ülesannete lihtsamaks otsimiseks on ülesannete numbrite ette pandud \enquote{Ü}, vihjete ette \enquote{V} ja lahenduste ette \enquote{L}. Näiteks ülesande 133 teksti number on kujul Ü133. Iga ülesande juures on kirjas ka selle autor ning olümpiaadi vooru lühinimetus, lisaks lühendid P 1, G 1 jne, kus tähed tähistavad põhikooli- ja gümnaasiumiastet. Näiteks G 9 viitab gümnaasiumiastme 9. ülesandele.

Kogumiku koostamise käigus eemaldati erinevatel põhjustel 3 ülesannet.
\newpage
\setlength{\parindent}{0pt}
'''

statements = manager.collection_two.getEstStatements(config)
hints = manager.collection_two.getEstHints(config)
solutions = manager.collection_two.getEstSolutions(config)

authors = r'''
\section{Autorite loetelu}

Aigar Vaigu -- Aalto Ülikool ja VTT Technical Research Centre of Finland\\
Aleksei Vlassov -- Tartu Ülikool\\
Andre Sääsk --\\
Andreas Valdmann -- Tartu Ülikool\\
Andres Laan -- Cambridge'i Ülikool\\
Eero Uustalu -- Tallinna Tehnikaülikool\\
Jaak Kikas -- Tartu Ülikool\\
Jaan Kalda -- Tallinna Tehnikaülikool\\
Jaan Susi -- Tartu Ülikool\\
Koit Timpmann -- Tartu Ülikool\\
Kristian Kuppart -- Tartu Ülikool\\
Mihkel Heidelberg -- Tartu Ülikool ja Tallinna Tehnikaülikool\\
Mihkel Kree -- Marseille' Ülikool ja Tartu Ülikool\\
Mihkel Pajusalu -- Tartu Ülikool ja Massachusettsi Tehnoloogiainstituut\\
Mihkel Rähn -- Tartu Ülikool\\
Oleg Košik -- Tartu Ülikool\\
Ott Krikmann -- Eesti Maaülikool\\
Riho Taba -- Bristoli Ülikool ja Imperial College\\
Roland Matt -- Tartu Ülikool ja ETH Zürich \\
Siim Ainsaar -- Tartu Ülikool ja Tallinna Tehnikaülikool\\
Stanislav Zavjalov -- Oxfordi Ülikool\\
Taavi Pungas -- Cambridge'i Ülikool ja Tartu Ülikool\\
Urmo Visk - Tartu Ülikool\\
Valter Kiisk -- Tartu Ülikool\\
'''

footer = r'''
\end{document}'''

contents = preamble + title_page + table_of_contents + introduction + statements + "\\normalsize" + hints + solutions + authors + footer

file_name = 'teine-kogumik-veeb'

generatePdf(file_name, contents, True)


print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_two.problems):}")
