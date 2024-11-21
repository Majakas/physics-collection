import codecs
import os
import regex as re


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
        self.metadata = []  # 0 = title, 1 = author, 2 = round, 3 = year, 4 = number, 5 = difficulty, 6 = topic
        self.default_metadata = ["", "Tundmatu autor", "", "", "", "?", ""]
        self.metadata_identifiers = ['\\prob', '\\setAuthor', '\\setRound', '\\setYear', '\\setNumber', '\\setDifficulty', '\\setTopic']
        self.text = [] # 0 = prob est, 1 = hint est, 2 = sol est, 3 = prob eng, 4 = hint eng, 5 = sol eng 
        self.text_identifiers = ['\\prob', '\\hint', '\\solu', '\\probeng', '\\hinteng', '\\solueng', '\\probend']

        for identifier in self.metadata_identifiers:
            self.metadata.append(self.parse_curly_contents(identifier))

        for identifier in self.text_identifiers:
            self.text.append(self.get_subsequent_text(identifier))

    def get_curly_idxs(self, identifier):
        idx = re.search(identifier.replace('\\','\\\\') + r'[{]', self.contents)
        if idx is None:
            # no argument found. Take default value
            return -1, -1
        idx = idx.start() + len(identifier)

        while self.contents[idx] != '{':
            if self.contents[idx] == '\n':
                # no argument found. Take default value
                return -1, -1
            idx += 1
        idx += 1
        start = idx
        while self.contents[idx] != '}':
            idx += 1
        return start, idx

    def parse_curly_contents(self, identifier):
        start, end = self.get_curly_idxs(identifier)
        if start == -1:
            if identifier not in self.metadata_identifiers:
                return ""
            else:
                return self.default_metadata[self.metadata_identifiers.index(identifier)]

        return self.contents[start:end]

    # Checks whether str is the same idx-th argument
    def argument_equality(self, str_, idx):
        if not 0 <= idx < len(self.arguments):
            raise ValueError('idx out of bounds of the arguments list!')
        if str_ == self.arguments[idx]:
            return True
        else:
            return False

    def update_metadata(self, str_, idx):
        if not 0 <= idx < len(self.metadata):
            raise ValueError('idx out of bounds of the list of arguments!')
        start, end = self.get_curly_idxs(self.metadata_identifiers[idx])

        self.metadata[idx] = str_
        self.contents = self.contents[:start] + self.metadata[idx] + self.contents[end:]

    def update_text_segment(self, new_text, identifier):
        start, end = self.get_subsequent_text_idx(identifier)

        self.contents = self.contents[:start] + new_text + self.contents[end:]

    def update_all_text(self, new_text):
        start = self.contents.find(self.text_identifiers[0])
        end = self.contents.find(self.text_identifiers[-1]) + len(self.text_identifiers[-1])
        if start == -1 or end == len(self.text_identifiers) - 1:
            return
        
        self.contents = self.contents[:start] + new_text + self.contents[end:]

    def get_subsequent_text_idx(self, identifier):
        idx = re.search(identifier.replace('\\','\\\\') + r'[{\s\d]', self.contents)
        if idx is None:
            # no argument found. Take default value
            return -1, -1

        idx = idx.start() + len(identifier)
        while self.contents[idx] != '\n':
            idx += 1
        start = idx + 1

        while True:
            for end_identifier in self.text_identifiers:
                if self.contents.startswith(end_identifier, idx):
                    return start, idx
            idx += 1
            if idx == len(self.contents):
                return -1, -1

    def get_subsequent_text(self, identifier):
        start, end = self.get_subsequent_text_idx(identifier)
        if start == -1:
            return ""
        else:
            return self.contents[start:end].strip()

    def get_subsequent_text_with_wrappers(self, identifier):
        start, end = self.get_subsequent_text_idx(identifier)
        if start == -1:
            return ""
        
        problem_name = self.get_metadata(0)
        if 'eng' in identifier:
            problem_name = self.parse_curly_contents('probeng')
        
        if identifier == '\\prob':
            return f'\\prob{{{problem_name}}}\n{self.contents[start:end].strip()}\n\\probend'
        return f'\\prob{{{problem_name}}}\n{identifier}\n{self.contents[start:end].strip()}\n\\probend'

    def get_metadata(self, idx):
        if not 0 <= idx < len(self.metadata):
            raise ValueError('index out of range of the list of arguments that should be accessible')
        return self.metadata[idx]

    def get_contents(self):
        return self.contents


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
