# coding: utf-8
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if os.path.dirname(__file__) != '':
    os.chdir(os.path.dirname(__file__))

from python_dependencies.problem_manager import ProblemManager, generate_pdf
from python_dependencies.utils import read_config, results_tabulator, table_title_converter

if not __name__ == "__main__":
    sys.exit()

manager = ProblemManager()
manager.load_directory("../probs_b3/")
manager.partition_into_books()
config = read_config("teine-kogumik-config.txt")

preamble = r'''\documentclass[10pt]{article}
\usepackage[web]{../problem-collection}
\newcommand{\pp}[1]{REMOVE}
\newcommand{\p}[1]{REMOVE}

\begin{document}
'''

title_page = r'''
\begin{titlepage}
    \centering
    \vspace{10cm}
    {\sffamily\Huge \mbox{200 EESTI FÜÜSIKAOLÜMPIAADI}\\ ÜLESANNET AASTATEST\\ 2018 -- 2025\par}
    \vspace{1cm}
    {\Large koos vihjete ja lahendustega\par}
    \vfill
    {\Large Koostas Taavet Kalda}

    \vfill

    % Bottom of the page
    {\large 2025}
\end{titlepage}
'''

copyright_page = r'''
\raggedbottom % Because of twosided
\mbox{}\vfill

\textcopyright~Autoriõigused: Eesti Matemaatika Selts, Tallinna Tehnikaülikool,
Tartu Ülikool, ülesannete autorid ja Taavet Kalda.
\vspace{0.5\baselineskip}

Kogumiku koostamist toetasid: Eesti Matemaatika Seltsi fond ``Benoit Mandelbroti Jälgedes'', Robert Kitt ja Tallinna Tehnikaülikool.
\vspace{0.5\baselineskip}

\newpage
'''

table_of_contents = r'''
\tableofcontents
\newpage
'''

introduction = r'''
{\setlength{\parindent}{24pt}
\section{Sissejuhatus}

Siia on koondatud 200 gümnaasiumi ülesannet Eesti füüsikaolümpiaadi piirkonnavoorudest, lõppvoorudest ja lahtistest võistlustest. Igale ülesandele on juurde kirjutatud paarilauseline vihje. Juhul kui õpilane jääb ülesannet lahendades toppama, on tal võimalik vihjet lugeda ning teisele katsele minna.

%Tegu on teise kogumikuga Eesti füüsikaolümpiaadi ülesannete kogude seeriast, kus esimene kattis 200 ülesannet ajavahemikust 2012---2018.

Ülesanded on jaotatud teemade kaupa ning teemasiseselt raskuse järgi. Raskustaset tähistatakse kuni viie tärniga. Ülesannete lihtsamaks otsimiseks on ülesannete numbrite ette pandud \enquote{Ü}, vihjete ette \enquote{V} ja lahenduste ette \enquote{L}. Näiteks ülesande 133 teksti number on kujul Ü133. Iga ülesande juures on kirjas ka selle autor ning olümpiaadi vooru lühinimetus, lisaks lühendid P 1, G 1 jne, kus tähed tähistavad põhikooli- ja gümnaasiumiastet. Näiteks G 9 viitab gümnaasiumiastme 9. ülesandele.

%Kogumiku koostamise käigus eemaldati erinevatel põhjustel 3 ülesannet.

Lisaks leiate kogumiku lõpust kogumiku poolt kaetud lahtiste ja lõppvoorude esimese ja teise järgu saanud õpilaste ning ülesannete autorite nimekirja.}
\newpage
\setlength{\parindent}{0pt}
'''

manager.collection_three.problem_sort_by_year()
i_start = 10
manager.collection_three.problems = manager.collection_three.problems[i_start:i_start+10]
statements = manager.collection_three.get_est_statements(config)
hints = manager.collection_three.get_est_hints(config)
solutions = manager.collection_three.get_est_solutions(config)

results = r'''
'''

authors = r'''
\section{Autorite loetelu}

TODO
'''

footer = r'''
\end{document}'''

contents = preamble + title_page + copyright_page + table_of_contents + introduction + statements + "\\normalsize" + hints + solutions + results + authors + footer

file_name = 'kolmas-kogumik-veeb'

print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_three.problems):}")

generate_pdf(file_name, contents, True)
