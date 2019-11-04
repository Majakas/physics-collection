import codecs
import os

# Load the configuration file for a collection. Appends specified text after problems
# E.g config = {"H12":"\newpage"} adds \newpage after the 12th hint.
def readConfig(file_name):
    config = {}
    if os.path.isfile(file_name):
        with codecs.open(file_name, "r", "utf8") as f:
            contents = f.readlines()
        for line in contents:
            if line.find(":") != -1:
                config[line[:line.find(":")]] = line[line.find(":") + 1:]
    return config


def tidy(str):
    return str.replace("\r\n", "\n").replace("\r", "\n")


round_to_abbreviation = {"piirkonnavoor":"v2g", "lahtine":"lahg", "lõppvoor":"v3g", "regional round":"v2g", "open competition":"lahg", "national round":"v3g"}


# Class for handling the contents of the problem file. Only manipulates text.
class ProblemText:
    def __init__(self, contents):
        contents = tidy(contents)
        self.contents = contents
        self.arguments = []
        ret = []
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
            raise valueError('Too many or too few arguments found in ProblemText')

    # Returns the indeces of the open and closed curly of the number-th argument
    def findArgumentCurlies(self, idx):
        depth = 0
        cnt = 0
        start = -1

        if not 0 <= idx < len(self.arguments):
            raise valueError('idx out of bounds')
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
    def argumentEquality(self, str, idx):
        if not 0 <= idx < len(self.arguments):
            raise ValueError('idx out of bounds of the arguments list!')
        if str == self.arguments[idx]:
            return True
        else:
            return False

    def updateArgument(self, str, idx):
        if not 0 <= idx < len(self.arguments):
            raise ValueError('idx out of bounds of the list of arguments!')
        start, end = self.findArgumentCurlies(idx)

        self.arguments[idx] = str
        self.contents = self.contents[:start + 1] + self.arguments[idx] + self.contents[end:]

    def updateIf(self, str, type):
        identifier = f'\\if{type}\n'
        idx = self.contents.index(identifier)
        if idx == -1:
            raise ValueError('if type doesn\' exist')

        start = idx
        while not self.contents.startswith("\\fi\n", idx):
            idx += 1
        idx += len("\\fi")

        self.contents = self.contents[:start] + str + self.contents[idx:]

    def updateTopic(self, new_topic):
        identifier = '% Teema: '
        idx = self.contents.index(identifier) + len(identifier)
        start = idx

        while self.contents[idx] != '\n':
            idx += 1

        self.contents = self.contents[:start] + new_topic + self.contents[idx:]

    def getArgument(self, idx):
        if not 0 <= idx < 6:
            raise ValueError('index out of range of the list of arguments that should be accessible')
        return self.arguments[idx]

    def getContents(self):
        return self.contents

    def getEngName(self):
        identifier = '% Problem name: '
        idx = self.contents.index(identifier) + len(identifier)

        name = ''
        while self.contents[idx] != '\n':
            name += self.contents[idx]
            idx += 1
        return name

    def getTopic(self):
        identifier = '% Teema: '
        idx = self.contents.index(identifier) + len(identifier)

        topic = ''
        while self.contents[idx] != '\n':
            topic += self.contents[idx]
            idx += 1
        return topic

    def getIf(self, type):
        identifier = f'\\if{type}\n'
        idx = self.contents.index(identifier)
        if idx == -1:
            raise ValueError('if type doesn\' exist')

        ret = ""
        while not self.contents.startswith("\\fi\n", idx):
            ret += self.contents[idx]
            idx += 1
        ret += "\\fi"

        return ret

def ResultsTabulator(args, file_name):
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

def TableTitleConverter(title, date):
    title = title.split("-")
    conv = {"lahg":["Füüsika lahtine võistlus", "Vanem rühm"], "v3g":["Füüsika lõppvoor", "Gümnaasium"]}
    if title[0] not in conv:
        raise ValueError("title doesn't follow the correct format")
    return [conv[title[0]][0], date, conv[title[0]][1]]
