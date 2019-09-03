import os
import codecs
import subprocess
from functools import cmp_to_key

from python_dependencies.utils import ProblemText

# Store info about a problem, needs a file attached following the usual naming convention
# Can be called to return the contents of the file and can be sorted in a nice way (see Collection)
class Problem:
    def __init__(self, file_name, directory = "/"):
        self.directory = directory
        self.file_name = file_name
        args = file_name.strip(".tex").split("-")
        self.round_abbr = args[1]

        contents = self.getContent()
        self.problem_text = ProblemText(contents)
        self.name = str(self.problem_text.getArgument(0))
        self.author = str(self.problem_text.getArgument(1))
        self.round = str(self.problem_text.getArgument(2))
        self.year = int(self.problem_text.getArgument(3))
        self.number = int(self.problem_text.getArgument(4)[2:])
        self.difficulty = int(self.problem_text.getArgument(5))
        self.topic = self.problem_text.getTopic().replace("-", " ")

    # TEMPORARY, USED FOR CHOOSING TOPICS FOR PROBLEMS WITH UNDETERMINED TOPICS
    def updateTopic(self, idx):
        contents = self.getContent()
        loc = contents.index("Teema: ") + len("Teema: ")
        loc0 = loc
        while (contents[loc] != "\n"):
            loc += 1

        teemad = ["Dünaamika", "Elektriahelad", "Elektrostaatika", "Gaasid", "Geomeetriline-optika", "Kinemaatika", "Magnetism", "Staatika", "Taevamehaanika", "Termodünaamika", "Varia", "Vedelike-mehaanika"]
        if self.topic == "Töötlemata":
            print("Options:")
            for i in range(len(teemad)):
                print(f"\t{i}: {teemad[i]}")
            str = input(f"Topic of P{idx} {self.file_name}: ")
            if (str.isdigit() and int(str) < len(teemad)):
                str = teemad[int(str)]
            print(f"Chosen topic was {str}")
            print("=============================")
            contents = contents[0:loc0] + str + contents[loc:-1] + contents[len(contents) - 1]
            with codecs.open(self.directory + self.file_name, "w", "utf8") as f:
                f.write(contents)

    def getContent(self,):
        with codecs.open(self.directory + self.file_name, "r", "utf8") as f:
            return f.read().replace("\r\n", "\n").replace("\r", "\n")

    # Removes all other \if ... \fi except the one being considered
    # Only serves to make .tex shorter, shouldn't make compilation faster...
    def getTidyContent(self, type):
        contents = ProblemText(self.problem_text.getContents())

        # Replace name with the english variant if language is english
        if type == "EngStatement" or type == "EngSolution":
            round_to_eng = {"lahg":r"open competition",
							"v3g":r"national round",
							"v2g":r"regional round"}
            # Update the name of the problem to be in English
            contents.updateArgument(contents.getEngName(), 0)
            # Update the topic of the problem to be in English
            contents.updateArgument(round_to_eng[self.round_abbr], 2)

        topic = f"% Teema: {self.topic}\n"
        if type != "Statement":
            topic += "\n"

        contents.updateArgument(f'\n{topic}{contents.getIf(type)}\n', 6)
        return contents.contents


# Custom comparator used for sorting Problems.
# TODO: Make this more python-y? Currently uses python 2.x structure.
dict_ = {"lahg":0, "v2g":1, "v3g":2}
def customProblemSort(x, y):
    if x.topic > y.topic:
        return 1
    elif x.topic == y.topic:
        if x.difficulty > y.difficulty:
            return 1
        elif x.difficulty == y.difficulty:
            if x.year > y.year:
                return 1
            elif x.year == y.year:
                if dict_[x.round_abbr] > dict_[y.round_abbr]:
                    return 1
                elif dict_[x.round_abbr] == dict_[y.round_abbr]:
                    if x.number > y.number:
                        return 1
                    elif x.number == y.number:
                        return 0
    return -1


# Stores problems to form a collection. Is able to sort the problems in different ways
# Default is to first sort by topic, then difficulty, then year, then round, then # of the problem.
# Is able to return LaTeX friendly statements/hints/solutions for all problems in the collections
# in different languages.
class Collection:
    def __init__(self, years):
        self.problems = []
        self.years = years

    def addProblem(self, problem):
        self.problems.append(problem)

    def problemSort(self):
        self.problems.sort(key=cmp_to_key(customProblemSort))

    def getEstStatements(self, config = {}):
        ret = r'''
        \section{Ülesanded}
        \ToggleStatement
        '''
        covered_topics = {}
        included_graphics_paths = {}
        not_first = False

        for i, problem in enumerate(self.problems):
            if problem.topic not in covered_topics:
                if not_first:
                    ret += "\\newpage"
                else:
                    not_first = True
                covered_topics[problem.topic] = True
                ret += "\\subsection{\\protect\\StrSubstitute{" + problem.topic + "}{-}{ }}\n"
            if problem.directory not in included_graphics_paths:
                ret +=  "\n\\graphicspath{{" + str(problem.directory) + "}}\n"
                included_graphics_paths[problem.directory] = True
            ret += f'\n% Ü{str(i + 1)}\n{problem.getTidyContent("Statement")}\n'
            if "P" + str(i + 1) in config:
                ret += config["P" + str(i + 1)] + "\n"
        ret += "\\newpage"
        return ret

    def getEstHints(self, config = {}):
        ret = r'''\section{Vihjed}
        \ToggleHint
        '''
        for i, problem in enumerate(self.problems):
            ret += f'\n% V{str(i + 1)}\n{problem.getTidyContent("Hint")}\n'
            if "H" + str(i + 1) in config:
                ret += config["H" + str(i + 1)] + "\n"
        ret += "\\newpage"
        return ret

    def getEstSolutions(self, config = {}):
        ret = r'''\section{Lahendused}
        \ToggleSolution
        '''
        for i, problem in enumerate(self.problems):
            ret += f'\n% L{str(i + 1)}\n{problem.getTidyContent("Solution")}\n'
            if "S" + str(i + 1) in config:
                ret += config["S" + str(i + 1)] + "\n"
        ret += "\\newpage"
        return ret

    def getEngStatements(self):
        ret = r'''
        \section{Problems}
        \ToggleEngStatement
        '''
        covered_topics = {}
        included_graphics_paths = {}
        not_first = False

        topic_to_eng = {"Dünaamika":"Dynamics",
                        "Elektriahelad":"Electric circuits",
                        "Elektrostaatika":"Electrostaticss",
                        "Gaasid":"Gases",
                        "Geomeetriline optika":"Geometrical optics",
                        "Kinemaatika":"Kinematics",
                        "Magnetism":"Magnetism",
                        "Staatika":"Statics",
                        "Taevamehaanika":"Stellar mechanics",
                        "Termodünaamika":"Thermodynamics",
                        "Varia":"Miscellaneous",
                        "Vedelike mehaanika":"Liquid mechanics"}

        for i, problem in enumerate(self.problems):
            if problem.topic not in covered_topics:
                if not_first:
                    ret += "\\newpage"
                else:
                    not_first = True
                covered_topics[problem.topic] = True
                ret += "\\subsection{\\protect\\StrSubstitute{" + topic_to_eng[problem.topic] + "}{-}{ }}\n"
            if problem.directory not in included_graphics_paths:
                ret +=  "\n\\graphicspath{{" + str(problem.directory) + "}}\n"
                included_graphics_paths[problem.directory] = True
            ret += f'\n% P{str(i + 1)}\n{problem.getTidyContent("EngStatement")}\n'
        ret += "\\newpage"
        return ret

    def getEngHints(self):
        ret = r'''\section{Hints}
        \ToggleEngHint
        '''
        for i, problem in enumerate(self.problems):
            ret += f'\n% H{str(i + 1)}\n{problem.getTidyContent("EngHint")}\n'
        ret += "\\newpage"
        return ret

    def getEngSolutions(self):
        ret = r'''\section{Solutions}
        \ToggleEngSolution
        '''
        for i, problem in enumerate(self.problems):
            ret += f'\n% S{str(i + 1)}\n{problem.getTidyContent("EngSolution")}\n'
        ret += "\\newpage"
        return ret


# Manages all the problems that are fed into it. Furthermore handles collection
# initialisation and storing
class ProblemManager:
    def __init__(self):
        self.problems = []
        self.collection_one = Collection((2012, 2018))
        self.collection_two = Collection((2005, 2011))
        self.collection_all = Collection((1900, 2099))

    def loadDirectory(self, directory = "/"):
        for file_name in os.listdir(directory):
            if isValidFileName(file_name):
                self.problems.append(Problem(file_name, directory))

    def partitionIntoBooks(self):
        for problem in self.problems:
            self.collection_all.addProblem(problem)

            if 2011 <= problem.year <= 2018:
                if not (problem.year == 2011 and not (problem.round_abbr == "lahg" and problem.number <= 4)):
                    if not (problem.year == 2018 and problem.round_abbr == "lahg"):
                        self.collection_one.addProblem(problem)

            if 2005 <= problem.year <= 2011:
                if problem.year == 2011 and (problem.round_abbr == "lahg" and problem.number <= 4):
                    continue
                self.collection_two.addProblem(problem)

        self.collection_one.problemSort()
        self.collection_two.problemSort()
        self.collection_all.problemSort()


# Determines whether the string follows the standard file naming convention of year-round-number.tex
def isValidFileName(str):
    args =  str.strip(".tex").split("-")
    if len(args) == 3 and args[0].isdigit() and args[1] in ["v2g", "lahg", "v3g"] and args[2].isdigit():
        if 1 <= int(args[2]) <= 10:
            return True
    return False


# Generates a pdf with LaTeX with argument contents as the contents of the .tex file to
# be compiled. If repeat is enabled, the code is compiled twice for cross-references.
# Also cleans up reduntant files
def generatePdf(file_name, contents, repeat = False):
    with codecs.open(file_name + '.tex', 'w', 'utf-8') as f:
         f.write(contents)

    for i in range(1 + int(repeat)):
        commandLine = subprocess.Popen(['xelatex', file_name + '.tex'])
        commandLine.communicate() # Feedback from the console

    os.remove(file_name + '.aux')
    os.remove(file_name + '.log')
    os.remove(file_name + '.toc')
    os.remove(file_name + '.out')
