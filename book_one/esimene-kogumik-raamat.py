# coding: utf-8
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.dirname(__file__))

from python_dependencies.problem_manager import ProblemManager, generatePdf
from python_dependencies.utils import readConfig


manager = ProblemManager()
manager.loadDirectory("../problems/")
manager.partitionIntoBooks()

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
	{\sffamily\Huge \mbox{200 EESTI FÜÜSIKAOLÜMPIAADI}\\ ÜLESANNET AASTATEST\\ 2012 -- 2018\par}
	\vspace{1cm}
	{\Large koos vihjete ja lahendustega\par}
	\vfill
	{\Large Koostas Taavet Kalda}

	\vfill

	% Bottom of the page
	{\large 2018}
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


Korrektor Lauri Vanamölder

Kaanekujundaja Rael Kalda

Saatesõna Robert Kitt ja Jaan Kalda
\vspace{0.5\baselineskip}

Kirjastanud Tallinna Tehnikaülikooli eelõppeosakond
\vspace{0.5\baselineskip}

ISBN 978-9949-83-342-9
\newpage
'''

table_of_contents = r'''
\tableofcontents
\newpage
'''

words_of_thanks = r'''
{\sloppy
\setlength{\parindent}{24pt}
\section*{Saateks}
\subsection*{Hea füüsikahuviline!}

Sa hoiad käes Eesti füüsikaolümpiaadide ülesannete kogu. Juba pelgalt asjaolu, et Sa sellise kogumiku oled avanud ja neid ridu loed, teeb Sind eriliseks. Sul on huvi looduse ja meid ümbritseva keskkonna vastu ning Sa tahad ennast proovile panna ülesandeid lahendades. Ei ole mingit vahet, kas näed end tulevikus teadlase, ettevõtja või avaliku elu tegelasena. Võime lahendada probleeme elust enesest tuleb igal elualal kasuks. Füüsikas on veel see eelis, et eksisteerivad superuniversaalsed tõed – loodusseadused, mis kehtivad igal ajal ja igal hetkel.

Olümpiaadiülesannete kogu on nagu kestvusala spordis. Tulemuse saavutamiseks tuleb pikalt pingutada. Mõni ülesanne jääb kummitama mitmeks päevaks, enne kui leiad idee lahenduseks. Ilmselt on mõned ülesanded ka üle jõu käivad. Kuid kõige parem tunne on siis, kui pikalt mõeldud lahenduskäik annab tulemuse ning ülesanne saab lahendatud ilma vastust piilumata. Sama on ka spordis: kui distantsi lõikad, ei ole finišijoont ületades see päris õige tunne. Seega on käesolev kogu peamiselt akadeemiline meelelahutus, mille preemiaks võib olla hea koht olümpiaadil või vähemasti füüsikatunnis.

Nagu öeldud, annavad füüsikaolümpiaadid ja füüsika laiemalt väga hea platvormi kõikideks elujuhtumiteks, kus on vaja lahendada mõnd keerulist probleemi.
Just füüsikute võime eristada olulist ebaolulisest ning lahendusvõrrandi koostamisel kasutada ainult sisuliselt olulisi mõjureid teeb füüsika teiste teaduste hulgas eriliseks. Samas tuleb seda pragmaatilist maailmavaadet pidevalt õlitada uute teadmiste ja kogemustega ning õppida ka ammu lahendatud ülesannetest.

Soovin, et käesolev ülesannete kogu oleks Sulle piisavalt kerge, et leida rõõmu õigetest lahendustest, ning piisavalt raske mõistmaks, et elus ei tule midagi lihtsalt.


\vspace{0.5\baselineskip}\noindent
Robert Kitt\\
Loodusteaduste doktor, TTÜ tehniline füüsika 2005. a\\
Eesti võistkonna liige rahvusvahelistel füüsikaolümpiaadidel 1994. ja 1995.~a

\newpage
\subsection*{Olümpiaadiülesanded kui meelelahutus}
{\setstretch{0.98}
Füüsikaolümpiaadid on olnud üle poole sajandi üheks olulisemaks faktoriks noortes füüsikahuvi äratamisel.
Erinevalt koolitunnis pakutavatest ülesannetest nõuavad olümpiaadiülesanded leidlikkust ja sarnaselt
mõttemängudele pakuvad lahendamisrõõmu. Kooliülesanded on reaalaladel võimekate laste jaoks liiga lihtsad, mistõttu
võib füüsika tunduda igav. Selliste õpilaste ande tõhusaks arendamiseks on vaja
midagi keerulisemat --- midagi sellist, nagu pakutakse olümpiaadidel.

Eesti füüsikaolümpiaadid (EFO) on tänu oma püsivalt nooruslikule žüriile suutnud pakkuda füüsikasõpradele puremiseks
uudseid ning intrigeerivaid pähkleid.
Žürii nooruslikkust on aidanud hoida see, et endised olümpiaadivõitjad, sõltumata sellest, mis riigis ja mis ülikoolis nad edasi õppima asuvad, liituvad harilikult žüriiga.
Värske veri tähendab värskeid ideid ja vaheldusrikkaid ülesandeid.
Ülikooliõpingute lõppemise järel kipub noorte žüriiliikmete aktiivsus vähenema, sest tulevad töökohustused,
aga selleks ajaks on žüriiga liitunud juba mitmed nooremad üliõpilased.

Läbi aastakümnete on kogunenud aukartustäratav hulk ülesandeid ---
suurepärane materjal füüsikahuvilisel noorel oma ande arendamiseks.
Need on leitavad küll internetilehtedelt, kuid ülesannete
kirjastamine on jäänud unarusse. Internetis leiduvate
ülesandevaramute häda on selles, et ülesanded on
sorteerimata ning õpilasel, kes otsib mingil teemal
teatud raskusastmega ülesannet, võib selle leidmisega olla tükk tegu.
Halvematel juhtudel võib õpilane sattuda vigase ülesande peale:
selliseid on küll väga vähe (käesoleva kogumiku statistika põhjal \textit{ca} 2\%),
aga õpilasele võib niisugune ülesanne mõjuda eksitavalt ja ebakindlust tekitavalt.

2017. aastaks oli eelmise EFO ülesannete kogumiku väljaandmisest möödunud enam kui kaks aastakümmet.
Osaliselt täidab tekkinud lünka Mihkel Kree ja Kristian Kupparti toimetatud ning Eesti Energia toel Tartu Ülikooli
teaduskooli poolt äsja kirjastatud saja ülesandega vihik ``Elekter ja termodünaamika''. Ometigi on häid
ülesandeid kogunenud palju rohkem!

\subsubsection*{Tänuavaldused}
Käesoleva vihikuga on vahefinišisse jõudnud Robert Kiti, kunagise rahvusvahelise
füüsikaolümpiaadi Eesti võistkonna liikme ning
praeguse Swedbank Eesti peadirektori algatus EFO
ülesannetearhiivi süstematiseerimiseks ja kirjastamiseks.
Tänagem sel puhul kõiki asjaosalisi: projekti algatajat ja Eesti matemaatika- ning
füüsikaolümpiaadide edendamiseks mõeldud stipendiumifondi ``Benoit Mandelbroti Jälgedes'' asutajat Robert Kitti; EFO žürii liikmeid kollegiaalse ja entusiastliku töö eest ülesannete koostamisel,
autoriõiguste valdajaid --- ülesannete autoreid (vt nimekirja kogumiku lõpus) ja Tartu Ülikooli ---  ülesannete avaldamise loa eest;
Haridus- ja Teadusministeeriumi olümpiaadide järjepideva rahastamise eest; Tartu Ülikooli teaduskooli
olümpiaadide organiseerimise eest; Tallinna Tehnikaülikooli eelõpet
kogumiku kiire kirjastamise eest.

\subsubsection*{Füüsika kui elukutse --- edasiõppimise võimalused}
Käesoleva kogumiku eesmärgiks on tõsta lugeja huvi füüsika vastu --- näidata, et füüsika tegeleb põnevate ning
eluliste probleemidega. Füüsika ei õpeta mitte ainult Newtoni seadusi, Maxwelli võrrandeid jms, vaid eelkõige
õpetab mõtlemisviisi ja strateegiaid, kuidas läheneda elulistele probleemidele: võimet koostada keeruliste nähtuste
lihtsaid mudeleid, eraldades olulise ebaolulisest. Sestap ei maksa imestada, et
füüsika erialal ülikooli lõpetanud on tööturul kõrgelt hinnatud.
Füüsikaharidusega inimesed suudavad oma oskusi rakendada kõikjal, mh uudsete tehnoloogiate
arendamisel, andmekaeves, investeerimisfirmades, panganduses jne.

Neil, kellel füüsikaolümpiaadi ülesannete lahendamine edeneb hästi, tasub tõsiselt kaaluda haridustee jätkamist
füüsikaga seotud erialadel ülikoolis. Eestis on selleks mitmeid võimalusi, eeskätt tuleb mainida
{Tallinna Tehnikaülikooli rakendusfüüsika õppekava ning Tartu Ülikooli füüsika, keemia ja materjaliteaduse õppekava}.
Füüsikaga on tihedalt seotud ka peaaegu kõik
Tallinna Tehnikaülikooli inseneri ja loodusteaduskonna õppekavad (nt elektroenergeetika ja mehhatroonika, maapõueressursid,
materjalitehnoloogia, ehituse ja biomeditsiiniga seotud õppekavad jne) ning  Tartu Ülikooli õppekavad
``Geoloogia ja keskkonnatehnoloogia'' ning ``Loodusteadused ja tehnoloogia'' (viimane on inglise keeles).
Tasub samuti teada, et nii  Tartu Ülikool kui Tallinna Tehnikaülikool võtavad olümpiaadidel edukalt
osalenud õpilasi vastu nn eritingimustel, st õppurid ei pea täitma lävendinõudeid.
Tartu Ülikooli puhul peab õpilane tulema üleriigilisel olümpiaadil 5 parema hulka 11.\ või 12.\ klassi arvestuses või
10 parema hulka üldpingereas, Tallinna Tehnikaülikoolis piisab reaalainete olümpiaadidel lõppvooru pääsemisest.

\subsubsection*{Füüsikale keskenduvad õppekavad Eesti ülikoolides}
Et lihtsustada õpilastel õppekava valikut, peatume lähemalt kahe vahetult füüsika nime pealkirjas sisaldava õppekava võrdlusel.

Nii Tallinna Tehnikaülikooli rakendusfüüsika õppekava rakendusfüüsika peaerialal kui ka Tartu Ülikooli füüsika, keemia ja materjaliteaduse õppekava füüsika
peaerialal on võimalik saada laiapõhjaline ja süsteemne füüsikaharidus, mis katab
enam-vähem võrdse arvu loengutundidega sellised baasteemad nagu termodünaamika, elektrodünaamika, optika,
kvantmehaanika ja erirelatiivsusteooria. Siiski on nende õppekavade vahel märkimisväärseid erinevusi.

Tartu Ülikooli õppekavas antakse värskele sisseastujale, kes ei suuda kohe teha kindlat valikut füüsika, keemia
ja materjaliteaduse vahel, võimalus lükata otsuse tegemine aasta võrra edasi: esimese aasta jooksul antakse talle
kiire ülevaade kõigist kolmest teadusharust ning seejärel saab ta teha teadliku valiku.
Tallinna Tehnikaülikoolis on samuti võimalik lükata valiku tegemine aasta võrra edasi, aga valida saab ühest küljest
rakendusfüüsika ning teisest küljest okeanograafia ja meteoroloogia vahel.

Tartu Ülikooli õppekavas on füüsika kogutundide arv suurem, seda ühest
küljest oluliselt suurema hulga füüsika praktikumide
ning teisest küljest selliste täiendavate füüsikapeatükkide tõttu nagu
``Spektroskoopia'', ``Globaalfüüsika''
ja ``Tuumafüüsika eksperimentaalmeetodid'', aga ka ülevaatekursus
``Füüsikaline maailmapilt'' ning meetodikeskne
õppeaine ``Loodusteadusliku meetodi seminar''.

Tallinna Tehnikaülikoolis seevastu on  suurendatud tähelepanu all
mehaanika (nt eraldi kursus on elastsusteooriast),
sest mehaanikal on oluline roll peaaegu kõigis tehnikateaduste
harudes; tänapäevafüüsika teemasid esindab kursus ``Sissejuhatus
osakestefüüsikasse ja kosmoloogiasse''. Rohkem on ka informaatikat ning
matemaatikat, muu hulgas pannakse rõhku statistilistele meetoditele ja
suurandmete analüüsile. Suurandmetega tuleb tänapäeval tegemist teha
paljude
rakendusfüüsika elukutsete puhul, nt okeanograafias ja majandusfüüsikas,
aga ka füüsikas endas, nt osakestefüüsikas.
Tallinna Tehnikaülikooli õppekavas on suurem osakaal valikainetel, nt
võib valida järgmisi kursusi:
``Astrofüüsika ja kosmonautika'', ``Majandusfüüsika alused'', ``Hüdro-
ja aeromehaanika'', ``Eksperimenditehnika'' ja
``Füüsikalised uurimismeetodid''.

Praktikavõimalusi on nii Tartus kui Tallinnas võrdselt palju.
Tartu füüsikaõppuritel on võimalik teha lõputöö ja saada teadustöö kogemus füüsika instituudis, kus
uurimisteemade valik on lai.
Tallinnas saab füüsikakeskset praktikat ning lõputööd teha nii Keemilise ja Bioloogilise Füüsika Instituudis kui ka
Tallinna Tehnikaülikooli küberneetika instituudis, võimalike uurimisteemade osaline loetelu on leitav lehelt
\url{www.taltech.ee/fyysika-teemad}.

Nimetatud õppekavade kohta on võimalik täiendavalt lugeda lehtedelt
\url{www.taltech.ee/fyysika} ja
\url{www.ut.ee/et/ut-oppekavad/fuusika-keemia-materjaliteadus}.

\vspace{0.5\baselineskip}\noindent
Jaan Kalda\\
Tallinna Tehnikaülikooli küberneetika instituut, professor\\
võistkonna mentor rahvusvahelistel füüsikaolümpiaadidel aastast 1994}
\fussy
'''

introduction = r'''
{\setlength{\parindent}{24pt}
\section{Sissejuhatus}

Siia on koondatud 200 gümnaasiumi ülesannet Eesti füüsikaolümpiaadi piirkonnavoorudest, lõppvoorudest ja lahtistest võistlustest. Igale ülesandele on juurde kirjutatud paarilauseline vihje. Juhul kui õpilane jääb ülesannet lahendades toppama, on tal võimalik vihjet lugeda ning teisele katsele minna.

Ülesanded on jaotatud teemade kaupa ning teemasiseselt raskuse järgi. Raskustaset tähistatakse kuni viie tärniga. Ülesannete lihtsamaks otsimiseks on ülesannete numbrite ette pandud \enquote{Ü}, vihjete ette \enquote{V} ja lahenduste ette \enquote{L}. Näiteks ülesande 133 teksti number on kujul Ü133. Iga ülesande juures on kirjas ka selle autor ning olümpiaadi vooru lühinimetus, lisaks lühendid P 1, G 1 jne, kus tähed tähistavad põhikooli- ja gümnaasiumiastet. Näiteks G 9 viitab gümnaasiumiastme 9. ülesandele.

Kogumiku koostamise käigus eemaldati erinevatel põhjustel 4 ülesannet, mis asendati 2011. aasta füüsika lahtise võistluse ülesannetega.}
\newpage
\setlength{\parindent}{0pt}
'''

statements = manager.collection_one.getEstStatements()
hints = manager.collection_one.getEstHints()
solutions = manager.collection_one.getEstSolutions()

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

contents = preamble + title_page + copyright_page + words_of_thanks + table_of_contents + introduction + statements + "\\normalsize" + hints + solutions + authors + footer

file_name = 'esimene-kogumik-raamat'

generatePdf(file_name, contents, True)


print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_one.problems):}")
