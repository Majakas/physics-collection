import os
import codecs
import subprocess
from functools import cmp_to_key

from python_dependencies.utils import ProblemText, round_to_abbreviation, letter_to_agegroup

cnt = 0

# Store info about a problem, needs a file attached following the usual naming convention
# Can be called to return the contents of the file and can be sorted in a nice way (see Collection)
class Problem:
    def __init__(self, file_name, directory="/"):
        self.directory = directory
        self.file_name = file_name
        # 0 = title, 1 = author, 2 = round, 3 = year, 4 = number, 5 = difficulty, 6 = topic
        contents = self.get_content()
        self.problem_text = ProblemText(contents)

        self.name = str(self.problem_text.get_metadata(0))
        self.author = str(self.problem_text.get_metadata(1))
        self.round = str(self.problem_text.get_metadata(2))
        self.round_abbr = round_to_abbreviation[self.round]
        self.year = int(self.problem_text.get_metadata(3))
        self.number = int(self.problem_text.get_metadata(4)[2:])
        self.difficulty = self.problem_text.get_metadata(5)
        if self.difficulty != "":
            self.difficulty = int(self.difficulty)
        else:
            self.difficulty = 0
        self.topic = str(self.problem_text.get_metadata(6))

    def get_content(self, ):
        with codecs.open(self.directory + self.file_name, "r", "utf8") as f:
            return f.read().replace("\r\n", "\n").replace("\r", "\n")

    def get_tidy_content(self, type_, prepend_appends=None):
        global cnt
        
        temp_contents = ProblemText(self.problem_text.get_contents())
        if prepend_appends is not None:
            for instruction in prepend_appends:
                idx, start, end = instruction
                old_arg = temp_contents.get_metadata(idx)
                temp_contents.update_metadata(start + old_arg + end, idx)
        
        temp_contents.update_all_text(f'{temp_contents.get_subsequent_text_with_wrappers(type_)}')
        return temp_contents.contents


# Custom comparator used for sorting Problems.
# TODO: Make this more python-y? Currently uses python 2.x structure.
dict_ = {"lahg": 0, "v2g": 1, "v3g": 2, "lahp": 3, "v2p": 4, "v3p": 5}


def custom_problem_sort(x, y):
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

    def add_problem(self, problem):
        self.problems.append(problem)

    def problem_sort(self):
        self.problems.sort(key=cmp_to_key(custom_problem_sort))

    def get_est_statements(self, config=None):
        if config is None:
            config = {}
        ret = r'''
        \section{Ülesanded}
        \toggleStatement
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
                ret += "\n\\graphicspath{{" + str(problem.directory) + "}}\n"
                included_graphics_paths[problem.directory] = True

            if "P" + str(i + 1) + "_author" in config:
                arg1 = (1, "" + config["P" + str(i + 1) + "_author"], "")
                ret += f'\n% Ü{str(i + 1)}\n{problem.get_tidy_content("prob", (arg1,))}\n'
            else:
                ret += f'\n% Ü{str(i + 1)}\n{problem.get_tidy_content("prob")}\n'
            if "P" + str(i + 1) in config:
                ret += config["P" + str(i + 1)] + "\n"
            ret += "\\bigskip\n"
        ret += "\\newpage"
        return ret

    def get_est_hints(self, config=None):
        if config is None:
            config = {}
        ret = r'''\section{Vihjed}
        \toggleHint
        '''
        for i, problem in enumerate(self.problems):
            ret += f'\n% V{str(i + 1)}\n{problem.get_tidy_content("hint")}\n'
            if "H" + str(i + 1) in config:
                ret += config["H" + str(i + 1)] + "\n"
            ret += "\\bigskip\n"
        ret += "\\newpage"
        return ret

    def get_est_solutions(self, config=None):
        if config is None:
            config = {}
        ret = r'''\section{Lahendused}
        \toggleSolution
        '''
        for i, problem in enumerate(self.problems):
            ret += f'\n% L{str(i + 1)}\n{problem.get_tidy_content("solu")}\n'
            if "S" + str(i + 1) in config:
                ret += config["S" + str(i + 1)] + "\n"
            ret += "\\bigskip\n"
        ret += "\\newpage"
        return ret

    def get_eng_statements(self):
        ret = r'''
        \section{Problems}
        \toggleStatement
        '''
        covered_topics = {}
        included_graphics_paths = {}
        not_first = False

        topic_to_eng = {"Dünaamika": "Dynamics",
                        "Elektriahelad": "Electric circuits",
                        "Elektrostaatika": "Electrostatics",
                        "Gaasid": "Gases",
                        "Geomeetriline optika": "Geometrical optics",
                        "Kinemaatika": "Kinematics",
                        "Laineoptika": "Wave optics",
                        "Magnetism": "Magnetism",
                        "Staatika": "Statics",
                        "Taevamehaanika": "Stellar mechanics",
                        "Termodünaamika": "Thermodynamics",
                        "Varia": "Miscellaneous",
                        "Vedelike mehaanika": "Liquid mechanics"}

        for i, problem in enumerate(self.problems):
            if problem.topic not in covered_topics:
                if not_first:
                    ret += "\\newpage"
                else:
                    not_first = True
                covered_topics[problem.topic] = True
                ret += "\\subsection{\\protect\\StrSubstitute{" + topic_to_eng[problem.topic] + "}{-}{ }}\n"
            if problem.directory not in included_graphics_paths:
                ret += "\n\\graphicspath{{" + str(problem.directory) + "}}\n"
                included_graphics_paths[problem.directory] = True
            ret += f'\n% P{str(i + 1)}\n{problem.get_tidy_content("probeng")}\n'
            ret += "\\bigskip\n"
        ret += "\\newpage"
        return ret

    def get_eng_hints(self):
        ret = r'''\section{Hints}
        \toggleHint
        '''
        for i, problem in enumerate(self.problems):
            ret += f'\n% H{str(i + 1)}\n{problem.get_tidy_content("hinteng")}\n'
            ret += "\\bigskip\n"
        ret += "\\newpage"
        return ret

    def get_eng_solutions(self):
        ret = r'''\section{Solutions}
        \toggleSolution
        '''
        for i, problem in enumerate(self.problems):
            ret += f'\n% S{str(i + 1)}\n{problem.get_tidy_content("solueng")}\n'
            ret += "\\bigskip\n"
        ret += "\\newpage"
        return ret


# Manages all the problems that are fed into it. Furthermore handles collection
# initialisation and storing
class ProblemManager:
    def __init__(self):
        self.problems = []
        self.collection_one = Collection((2012, 2018))
        self.collection_two = Collection((2005, 2011))
        self.collection_three = Collection((1900, 2004))
        self.collection_all = Collection((1900, 2099))
        self.collection_one_younger = Collection((2012, 2018))

    def load_directory(self, directory="/", strict=True):
        for file_name in os.listdir(directory):
            if is_valid_filename(file_name, strict):
                self.problems.append(Problem(file_name, directory))

    def partition_into_books(self):
        for problem in self.problems:
            if problem.age_group == "high school":
                self.collection_all.add_problem(problem)

                if 2011 <= problem.year <= 2018:
                    if not (problem.year == 2011 and not (problem.round_abbr == "lahg" and problem.number <= 5)):
                        if not (problem.year == 2018 and problem.round_abbr == "lahg"):
                            self.collection_one.add_problem(problem)

                if 2005 <= problem.year <= 2011:
                    if problem.year == 2011 and (problem.round_abbr == "lahg" and problem.number <= 5):
                        continue
                    self.collection_two.add_problem(problem)

            elif problem.age_group == "middle school":
                self.collection_one_younger.add_problem(problem)

            if problem.year <= 2004:
                self.collection_three.add_problem(problem)

        self.collection_one.problem_sort()
        self.collection_two.problem_sort()
        self.collection_three.problem_sort()
        self.collection_all.problem_sort()
        self.collection_one_younger.problem_sort()

# Determines whether the string follows the standard file naming convention of year-round-number.tex
def is_valid_filename(x, strict=True):
    if strict:
        args = x.strip(".tex").split("-")
        if len(args) == 3 and args[0].isdigit() and args[1] in ["v2g", "lahg", "v3g"] and args[2].isdigit():
            if 1 <= int(args[2]) <= 10:
                return True
        return False
    else:
        return x.endswith(".tex")


# Generates a pdf with LaTeX with argument contents as the contents of the .tex file to
# be compiled. If repeat is enabled, the code is compiled twice for cross-references.
# Also cleans up reduntant files
def generate_pdf(file_name, contents, repeat=False):
    with codecs.open(file_name + '.tex', 'w', 'utf-8') as f:
        f.write(contents)

    for i in range(1 + int(repeat)):
        commandLine = subprocess.Popen(['xelatex', file_name + '.tex'])
        commandLine.communicate()  # Feedback from the console

    if os.path.isfile(file_name + '.aux'):
        os.remove(file_name + '.aux')
    if os.path.isfile(file_name + '.log'):
        os.remove(file_name + '.log')
    if os.path.isfile(file_name + '.toc'):
        os.remove(file_name + '.toc')
    if os.path.isfile(file_name + '.out'):
        os.remove(file_name + '.out')
