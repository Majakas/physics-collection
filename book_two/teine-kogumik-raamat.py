# coding: utf-8
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if os.path.dirname(__file__) != '':
    os.chdir(os.path.dirname(__file__))

from python_dependencies.problem_manager import ProblemManager, generatePdf
from python_dependencies.utils import readConfig


manager = ProblemManager()
manager.loadDirectory("../problems/")
manager.partitionIntoBooks()
config = readConfig("teine-kogumik-config.txt")

preamble = r'''\documentclass[11pt, twoside]{article}
\usepackage[paperwidth=165mm,paperheight=235mm, textwidth=360pt, textheight=541.40024pt, inner = 25mm, outer = 15mm]{geometry}

\usepackage[width=181mm, height=251mm, cam, center]{crop}
\def\longer{22.7621}
\def\shorter{14.2263}
\newcommand*\cropa{%
	\begin{picture}(0,0)
		\thinlines\unitlength1pt
		\put(-\longer,0){\line(1,0){\shorter}}
		\put(0, \longer){\line(0,-1){\shorter}}
	\end{picture}%
}
\newcommand*\cropb{%
	\begin{picture}(0,0)
		\thinlines\unitlength1pt
		\put(\longer,0){\line(-1,0){\shorter}}
		\put(0,\longer){\line(0,-1){\shorter}}
	\end{picture}%
}
\newcommand*\cropc{%
	\begin{picture}(0,0)
		\thinlines\unitlength1pt
		\put(-\longer,0){\line(1,0){\shorter}}
		\put(0,-\longer){\line(0,1){\shorter}}
	\end{picture}%
}
\newcommand*\cropd{%
	\begin{picture}(0,0)
		\thinlines\unitlength1pt
		\put(\longer,0){\line(-1,0){\shorter}}
		\put(0,-\longer){\line(0,1){\shorter}}
	\end{picture}%
}
\cropdef[]\cropa\cropb\cropc\cropd{cam_new}
\crop[cam_new]

\usepackage[cmyk]{xcolor} % PDF needs to be in CMYK colour space for printing
\usepackage{../problem-collection-book}

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

Kogumiku koostamist toetasid: Eesti Matemaatika Seltsi fond ``Benoit Mandelbroti Jälgedes'', Robert Kitt ja Tallinna Tehnikaülikool.
\vspace{0.5\baselineskip}


Korrektor ???

Kaanekujundaja Rael Kalda

Saatesõna Robert Kitt ja Jaan Kalda
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

Tegu on teise kogumikuga Eesti füüsikaolümpiaadi ülesannete kogude seerias, kus esimene kattis 200 ülesannet ajavahemikust 2012---2018.

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
Andreas Valdmann -- Tartu Ülikool\\
Andres Põldaru -- Tartu Ülikool\\
Ants Remm -- Tartu Ülikool ja ETH Zürich \\
Ardi Loot -- Tartu Ülikool\\
Eero Vaher -- Tartu Ülikool ja Leideni Ülikool\\
Erkki Tempel -- Eesti Füüsika Selts ja Pärnu Sütevaka Humanitaargümnaasium\\
Hans Daniel Kaimre -- Tartu Ülikool\\
Jaan Kalda -- Tallinna Tehnikaülikool\\
Jaan Toots -- Cambridge'i Ülikool ja Oxfordi Ülikool\\
Jonatan Kalmus -- Tallinna Tehnikaülikool\\
Joonas Kalda -- Cambridge'i Ülikool\\
Kaur Aare Saar -- Cambridge'i Ülikool ja Oxfordi Ülikool\\
Koit Timpmann -- Tartu Ülikool\\
Kristian Kuppart -- Tartu Ülikool\\
Madis Ollikainen -- Tartu Ülikool ja ETH Zürich \\
Mihkel Heidelberg -- Tartu Ülikool ja Tallinna Tehnikaülikool\\
Mihkel Kree -- Marseille' Ülikool ja Tartu Ülikool\\
Mihkel Pajusalu -- Tartu Ülikool ja Massachusettsi Tehnoloogiainstituut\\
Mihkel Rähn -- Tartu Ülikool\\
Moorits Mihkel Muru -- Tartu Ülikool\\
Rasmus Kisel -- Cambridge'i Ülikool\\
Roland Matt -- Tartu Ülikool ja ETH Zürich \\
Sandra Schumann -- Harvardi Ülikool ja Tartu Ülikool\\
Siim Ainsaar -- Tartu Ülikool ja Tallinna Tehnikaülikool\\
Stanislav Zavjalov -- Oxfordi Ülikool\\
Taavet Kalda -- Oxfordi Ülikool\\
Taavi Pungas -- Cambridge'i Ülikool ja Tartu Ülikool\\
Taivo Pungas -- ETH Zürich \\
Tanel Kiis -- Tartu Ülikool\\
Valter Kiisk -- Tartu Ülikool\\
Oleg Košik -- Tartu Ülikool\\
'''

footer = r'''
\end{document}'''

contents = preamble + title_page + copyright_page + table_of_contents + introduction + statements + "\\normalsize" + hints + solutions + authors + footer

file_name = 'teine-kogumik-raamat'

generatePdf(file_name, contents, True)


print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_two.problems):}")
