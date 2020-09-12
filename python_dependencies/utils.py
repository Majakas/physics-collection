import codecs
import os


# Load the configuration file for a collection. Appends specified text after problems
# E.g config = {"H12":"\newpage"} adds \newpage after the 12th hint.
def read_config(file_name):
    config = {}
    if os.path.isfile(file_name):
        with codecs.open(file_name, "r", "utf8") as f:
            contents = f.readlines()
        for line in contents:
            if line.find(":") != -1:
                config[line[:line.find(":")]] = line[line.find(":") + 1:]
    return config


def tidy(x):
    return x.replace("\r\n", "\n").replace("\r", "\n")


def round_to_abbreviation(round_, agegroup):
    converter_round = {"piirkonnavoor": "v2", "lahtine": "lah", "lõppvoor": "v3", "regional round": "v2",
                        "open competition": "lah", "national round": "v3"}
    converter_agegroup = {"middle school": "p", "high school": "g"}

    if (round_ not in converter_round) or (agegroup not in converter_agegroup):
        print("round or agegroup don't follow the correct format!")
    return converter_round[round_] + converter_agegroup[agegroup]


def letter_to_agegroup(x):
    if x == "G":
        return "high school"
    elif x == "P":
        return "middle school"
    else:
        raise ValueError


# Class for handling the contents of the problem file. Only manipulates text.
class ProblemText:
    def __init__(self, contents):
        contents = tidy(contents)
        self.contents = contents
        self.arguments = []
        i = 0
        while i < len(contents):
            if contents[i] == "{":
                arg = ""
                i += 1
                depth = 1
                while True:
                    if contents[i] == "{" and contents[i - 1] != "\\":
                        depth += 1
                    elif contents[i] == "}" and contents[i - 1] != "\\":
                        depth -= 1
                    if depth == 0:
                        break
                    arg += contents[i]
                    i += 1
                self.arguments.append(arg)
            i += 1
        if len(self.arguments) != 7:
            raise ValueError('Too many or too few arguments found in ProblemText')

    # Returns the indeces of the open and closed curly of the number-th argument
    def find_argument_curlies(self, idx):
        depth = 0
        cnt = 0
        start = -1

        if not 0 <= idx < len(self.arguments):
            raise ValueError('idx out of bounds')
        for i in range(len(self.contents)):
            if self.contents[i - 1] != '\\':
                if self.contents[i] == '{':
                    depth += 1
                elif self.contents[i] == '}':
                    depth -= 1

                if depth == 1 and self.contents[i] == '{':
                    if cnt == idx and start == -1:
                        start = i

                if depth == 0 and self.contents[i] == '}':
                    if cnt == idx:
                        return start, i
                    cnt += 1
        raise ValueError('Something went wrong with the curlies')

    # Checks whether str is the same idx-th argument
    def argument_equality(self, str_, idx):
        if not 0 <= idx < len(self.arguments):
            raise ValueError('idx out of bounds of the arguments list!')
        if str_ == self.arguments[idx]:
            return True
        else:
            return False

    def update_argument(self, str_, idx):
        if not 0 <= idx < len(self.arguments):
            raise ValueError('idx out of bounds of the list of arguments!')
        start, end = self.find_argument_curlies(idx)

        self.arguments[idx] = str_
        self.contents = self.contents[:start + 1] + self.arguments[idx] + self.contents[end:]

    def update_if(self, str_, if_type):
        identifier = f'\\if{if_type}\n'
        idx = self.contents.index(identifier)
        if idx == -1:
            raise ValueError('if type doesn\' exist')

        start = idx
        while not self.contents.startswith("\\fi\n", idx):
            idx += 1
        idx += len("\\fi")

        self.contents = self.contents[:start] + str_ + self.contents[idx:]

    def update_topic(self, new_topic):
        identifier = '% Teema: '
        idx = self.contents.index(identifier) + len(identifier)
        start = idx

        while self.contents[idx] != '\n':
            idx += 1

        self.contents = self.contents[:start] + new_topic + self.contents[idx:]

    def get_argument(self, idx):
        if not 0 <= idx <= 6:
            raise ValueError('index out of range of the list of arguments that should be accessible')
        return self.arguments[idx]

    def get_contents(self):
        return self.contents

    def get_eng_name(self):
        identifier = '% Problem name: '
        try:
            idx = self.contents.index(identifier) + len(identifier)

            name = ''
            while self.contents[idx] != '\n':
                name += self.contents[idx]
                idx += 1
        except ValueError:
            name = ''
        return name

    def get_topic(self):
        identifier = '% Teema: '
        idx = self.contents.index(identifier) + len(identifier)

        topic = ''
        while self.contents[idx] != '\n':
            topic += self.contents[idx]
            idx += 1
        return topic

    def get_if(self, if_type):
        try:
            identifier = f'\\if{if_type}\n'
            idx = self.contents.index(identifier)
            if idx == -1:
                raise ValueError('if type doesn\' exist')

            ret = ""
            while not self.contents.startswith("\\fi\n", idx):
                ret += self.contents[idx]
                idx += 1
            ret += "\\fi"
        except ValueError:
            ret = f'\\if{if_type}\n\\fi'

        return ret


def results_tabulator(args, file_name):
    latex = r'''\begin{table}[H]
    \begin{center}
    \pgfplotstabletypeset[
        col sep=comma,
        string type,
        every head row/.style={%
            before row={
                \rowcolor[rgb]{0.9,0.9,0.9}
                \multicolumn{6}{c}{\textbf{''' + args[0] + r'''}} \\
                \rowcolor[rgb]{0.9,0.9,0.9}
                \multicolumn{6}{c}{\textbf{''' + args[1] + r'''}} \\
                \rowcolor[rgb]{0.9,0.9,0.9}
                \multicolumn{6}{c}{\textbf{''' + args[2] + r'''}} \\
                \rowcolor[rgb]{0.9,0.9,0.9}
            },
            after row={}
        },
        columns={KOHT, NIMI, KLASS, JUHENDAJA, PSUM, RANK},
        columns/KOHT/.style={
            column name=Koht,
        },
        columns/NIMI/.style={
            column name=Nimi,
            column type={l}
        },
        columns/JUHENDAJA/.style={
            column name=Füüsikaõpetaja,
            column type={l}
        },
        columns/KLASS/.style={
            column name=Klass,
        },
        columns/PSUM/.style={
            column name=Kokku,
            column type={S},
        },
        columns/RANK/.style={
            column name=Järk,
        },
        ]{''' + file_name + r'''}
    \end{center}
    \end{table}
    '''
    return latex


def table_title_converter(title, date):
    title = title.split("-")
    conv = {"lahg": ["Füüsika lahtine võistlus", "Vanem rühm"], "v3g": ["Füüsika lõppvoor", "Gümnaasium"]}
    if title[0] not in conv:
        raise ValueError("title doesn't follow the correct format")
    return [conv[title[0]][0], date, conv[title[0]][1]]
