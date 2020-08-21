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
manager.load_directory("Kogumik_new/", strict=False)
manager.partition_into_books()
#config = read_config("teine-kogumik-config.txt")
print(len(manager.collection_one_younger.problems))


preamble = r'''\documentclass[11pt]{article}
\usepackage[web]{../problem-collection}
\begin{document}
'''

title_page = r'''
\begin{titlepage}
    \centering
    \vspace{10cm}
    {\sffamily\Huge \mbox{180 EESTI FÜÜSIKAOLÜMPIAADI}\\ PÕHIKOOLI ÜLESANNET AASTATEST\\ 2006 -- 2020?\par}
    \vspace{1cm}
    {\Large koos vihjete ja lahendustega\par}
    \vfill
    {\Large Koostas Raimond Pääru}

    \vfill

    % Bottom of the page
    {\large 2019}
\end{titlepage}
'''

copyright_page = r'''
\raggedbottom % Because of twosided
\mbox{}\vfill

\textcopyright~Autoriõigused: ...

\vfill

Toimetas ja kontrollis Roland Erich Uriko

Kirjastanud Tallinna Tehnikaülikooli eelõppeosakond
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

Siia on koondatud 180 põhikooli ülesannet Eesti füüsikaolümpiaadi piirkonnavoorudest ja lõppvoorudest.
Igale ülesandele on juurde kirjutatud lühike vihje.
Juhul kui õpilane jääb ülesannet lahendades toppama, on tal võimalik vihjet lugeda ning teisele katsele minna.

Ülesanded on jaotatud teemade kaupa ning teemasiseselt raskuse järgi. Raskustaset tähistatakse kuni viie tärniga.
Ülesannete lihtsamaks otsimiseks on ülesannete numbrite ette pandud Ü vihjete ette V ja lahenduste ette L.
Näiteks ülesande 69 teksti number on kujul Ü69.
Iga ülesande juures on kirjas ka selle autor (kui see on teada) ning olümpiaadi vooru lühinimetus, lisaks lühendid P 1, G 1 jne, kus tähed tähistavad põhikooli- ja gümnaasiumiastet.
Näiteks P 9 viitab põhikooliastme 9. ülesandele.
\newpage
\setlength{\parindent}{0pt}
'''

statements = manager.collection_one_younger.get_est_statements()
hints = manager.collection_one_younger.get_est_hints()
solutions = manager.collection_one_younger.get_est_solutions()

authors = r'''
\section{Autorite loetelu}

...
'''

footer = r'''
\end{document}'''

contents = preamble + title_page + copyright_page + table_of_contents + introduction + statements + "\\normalsize" + hints + solutions + footer

file_name = 'esimene-kogumik-noorem-veeb'

generate_pdf(file_name, contents, True)

print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_two.problems):}")
