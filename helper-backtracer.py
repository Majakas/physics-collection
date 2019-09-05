# Goes through a book's latex file and checks whether anything has been updated in there
# compared to the original .tex version and if there has been, the original source file
# for the problem will be updated correspondingly.
import argparse
import codecs

from python_dependencies.problem_manager import ProblemManager, generatePdf, Problem, round_to_abbreviation

parser = argparse.ArgumentParser(description='Backpropagate the updates made into the book .tex file to the problem source files.')
parser.add_argument(
    '--source',
    type=str,
    default = "",
    help='Specify the location of the book .tex file.')
args = parser.parse_args()


def tidy(str):
    return str.replace("\r\n", "\n").replace("\r", "\n")

manager = ProblemManager()
manager.loadDirectory("problems/")
manager.partitionIntoBooks()

source = args.source
problem_folder = "problems/"
contents = ""
with codecs.open(source, "r", "utf8") as f:
    contents = tidy(f.read())

i = 0
cnt = 0

topics = {}
is_english = False
args_dict = [{} for i in range(6)]
while i < len(contents):
    if contents.startswith(r"\ylDisplay{", i):
        cnt += 1
        args = []
        while len(args) < 7:
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
                args.append(arg)
            i += 1
        file_name = f'{args[3]}-{round_to_abbreviation[args[2]]}-{int(args[4][2:]):02}.tex'

        new_text, new_type, new_topic = "", "", ""

        new_text = args[6]
        for j in range(len(new_text)):
            if new_text.startswith("\\if", j):
                new_text = new_text[j:].strip()

        iftype = new_text.split("\n")[0]
        if iftype.find("Eng") != -1:
            is_english = True
        new_type = iftype[3:]

        idx = args[6].find("% Teema:") + len("% Teema:")
        while args[6][idx] != "\n":
            new_topic += args[6][idx]
            idx += 1
        new_topic = new_topic.strip().replace("-", " ")

        #print(file_name)
        problem = Problem(file_name, problem_folder)

        old_text = problem.problem_text.getIf(new_type)

        #print(actual_contents == pr)
        if old_text != new_text:
            print(f"{iftype[3:]} of problem {file_name} needs to be updated:\n\tP{(cnt-1)%200+1}: {args[0]}\n\told length: {len(old_text)}, new length: {len(new_text)}")

            problem.problem_text.updateIf(new_text, new_type)
            print(repr(old_text))
            print(repr(new_text))
            input("\tProceed?")
            with codecs.open(problem_folder + file_name, "w", "utf8") as f:
                f.write(problem.problem_text.getContents().replace("\n", "\r\n"))
            print("Success")


        if file_name not in topics:
            topics[file_name] = {}
        if new_topic not in topics[file_name]:
            topics[file_name][new_topic] = 0
        topics[file_name][new_topic] += 1

        for j in range(6):
            if j != 2 and not (j == 0 and is_english):
                if file_name not in args_dict[j]:
                    args_dict[j][file_name] = {}
                if args[j] not in args_dict[j][file_name]:
                    args_dict[j][file_name][args[j]] = 0
                args_dict[j][file_name][args[j]] += 1
        #print(i)
    i += 1

for file_name, dict in topics.items():
    min_freq = 1000
    min_topic = ""
    for topic, freq in dict.items():
        if freq < min_freq:
            min_freq = freq
            min_topic = topic

    if min_freq < 3:
        new_topic = min_topic
        problem = Problem(file_name, problem_folder)

        if new_topic == problem.topic:
            continue

        print(f"Updating the topic of problem {file_name}:\n\told topic: {problem.topic}, new topic: {new_topic}")
        new_text = problem.getContent()
        id = "% Teema: "
        new_text = new_text[:new_text.find(id) + len(id)] + new_topic.replace(" ", "-") + new_text[new_text.find(id) + len(id) + len(problem.topic):]

        input("\tProceed?")
        with codecs.open(problem_folder + file_name, "w", "utf8") as f:
            new_text = new_text.replace("\n", "\r\n")
            f.write(new_text)
            print("Success")

for i in range(6):
    if i != 2 and not (i == 0 and is_english):
        for file_name, dict in args_dict[i].items():
            min_freq = 1000
            min_arg = ""
            for arg, freq in dict.items():
                if freq < min_freq:
                    min_freq = freq
                    min_arg = arg

            if min_freq < 3:
                new_arg = min_arg
                problem = Problem(file_name, problem_folder)

                if new_arg == problem.problem_text.getArgument(i):
                    continue

                descriptions = ["problem name", "author", "round", "year", "problem number", "difficulty"]

                print(f"Updating the {descriptions[i]} of problem {file_name}:\n\told {descriptions[i]}: {problem.problem_text.getArgument(i)}, new {descriptions[i]}: {new_arg}")
                print(repr(problem.problem_text.getArgument(i)))
                problem.problem_text.updateArgument(new_arg, i)
                print(repr(new_arg))

                input("\tProceed?")
                with codecs.open(problem_folder + file_name, "w", "utf8") as f:
                    f.write(problem.problem_text.getContents().replace("\n", "\r\n"))
                    print("Success")

print(f'Number of passes: {cnt}')
