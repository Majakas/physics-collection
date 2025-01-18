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
manager.load_directory("../problems/")
manager.partition_into_books()
config = read_config("teine_kogumik_config.txt")

preamble = r'''\documentclass[10pt]{article}
\usepackage[web]{../problem-collection}
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

copyright_page = r'''
\raggedbottom % Because of twosided
\mbox{}\vfill

\textcopyright~Autoriõigused: Eesti Matemaatika Selts, Tallinna Tehnikaülikool,
Tartu Ülikool, ülesannete autorid ja Taavet Kalda.
\vspace{0.5\baselineskip}

Kogumiku koostamist toetasid: Eesti Matemaatika Seltsi fond \enquote{Benoit Mandelbroti Jälgedes}, Robert Kitt ja Tallinna Tehnikaülikool.
\vspace{0.5\baselineskip}


Korrektorid Nata-Ly Pantšenko ja Erki Leht

Kaanekujundaja Rael Kalda
\vspace{0.5\baselineskip}

Kirjastanud Tallinna Tehnikaülikooli eelõppeosakond
\vspace{0.5\baselineskip}

ISBN ???
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

Tegu on teise kogumikuga Eesti füüsikaolümpiaadi ülesannete kogude seeriast, kus esimene kattis 200 ülesannet ajavahemikust 2012---2018.

Ülesanded on jaotatud teemade kaupa ning teemasiseselt raskuse järgi. Raskustaset tähistatakse kuni viie tärniga. Ülesannete lihtsamaks otsimiseks on ülesannete numbrite ette pandud \enquote{Ü}, vihjete ette \enquote{V} ja lahenduste ette \enquote{L}. Näiteks ülesande 133 teksti number on kujul Ü133. Iga ülesande juures on kirjas ka selle autor ning olümpiaadi vooru lühinimetus, lisaks lühendid P 1, G 1 jne, kus tähed tähistavad põhikooli- ja gümnaasiumiastet. Näiteks G 9 viitab gümnaasiumiastme 9. ülesandele.

Kogumiku koostamise käigus eemaldati erinevatel põhjustel 3 ülesannet.

Lisaks leiate kogumiku lõpust kogumiku poolt kaetud lahtiste ja lõppvoorude esimese ja teise järgu saanud õpilaste ning ülesannete autorite nimekirja.
\newpage
\setlength{\parindent}{0pt}
'''

statements = manager.collection_two.get_est_statements(config)
hints = manager.collection_two.get_est_hints(config)
solutions = manager.collection_two.get_est_solutions(config)

results_years = ["v3g-2005", "lahg-2005", "v3g-2006", "lahg-2006", "v3g-2007",
                 "lahg-2007", "v3g-2008", "lahg-2008", "v3g-2009", "lahg-2009",
                 "v3g-2010", "lahg-2010", "v3g-2011", "lahg-2011"]
dates = ["9. aprill 2005. a.", "26. november 2005. a.", "4. märts 2006. a.", "25. november 2006. a.",
         "17. märts 2007. a.", "24. november 2007. a.", "8. märts 2008. a.", "29. november 2008. a.",
         "7. märts 2009. a.", "28. november 2009. a.", "6. märts 2010. a.", "27. november 2010. a.",
         "9. aprill 2011. a.", "26. november 2011. a.", ]
results = r'''
\section{Õpilaste tulemused}
'''
for i in range(len(results_years)):
    results += results_tabulator(table_title_converter(results_years[i], dates[i]),
                                 "results/" + results_years[i] + ".csv")
results += r'''\newpage
'''

authors = r'''
\section{Autorite loetelu}

Aigar Vaigu -- Aalto Ülikool ja VTT Technical Research Centre of Finland\\
Aleksei Vlassov -- Tartu Ülikool\\
Andre Sääsk -- Tartu Ülikooli Narva kolledž\\
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

contents = preamble + title_page + copyright_page + table_of_contents + introduction + statements + "\\normalsize" + hints + solutions + results + authors + footer

file_name = 'teine_kogumik_veeb'

generate_pdf(file_name, contents, True)

print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_two.problems):}")
