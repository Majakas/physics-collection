import os
import codecs
from shutil import copyfile
from python_dependencies.utils import ProblemText, tidy
from python_dependencies.problem_manager import Problem, Collection, ProblemManager

def stripBeginning(str):
    return str.split("/")[-1]


def isValidFileName(str):
    str = str.split("/")[-1]
    args =  str.strip(".tex").split("-")
    if len(args) == 3 and args[0].isdigit() and args[1] in ["v2g", "lahg", "v3g"] and args[2].isdigit():
        if 1 <= int(args[2]) <= 10:
            return True
    return False


def transcribe(directory, topic_name=""):
    covered = {}
    names = []
    if directory == "":
        all_files = os.listdir()
    else:
        all_files = os.listdir(directory)
    for file_name in all_files:
        if isValidFileName(file_name):
            prob = Problem(file_name, directory)
            #print(prob.author)
            if prob.author not in covered:
                covered[prob.author] = prob.author
                names.append(prob.author)

            contents = ""
            # os.rename(directory + file_name, directory + file_name[0:-7] + ".tex")
            with codecs.open(directory + file_name, "r", "utf8") as f:
                contents = f.read()
                i = 0
                while i < len(contents):
                    if contents[i] == '′':
                        contents = contents[:i] + '\'' + contents[i + 1:]
                    i += 1

            #with codecs.open(directory + file_name, "w", "utf8") as f:
                #f.write(contents)
                #contents = f.readlines()
                #contents.insert(7, ("% Teema: " + topic_name).strip("/") + "\n")
                #contents = "".join(contents)
                #with codecs.open("200-test/" + file_name, "w", "utf8") as out:
                #    out.write(contents)
        #else:
        #    copyfile(directory + file_name, "200-test/" + file_name)
    names.sort()
    with codecs.open("autorid.txt", "w", "utf8") as f:
        for name in names:
            print(name)
            f.write(name + "\n")


def locate(file_name, destination_file):
    if isValidFileName(file_name):
        with codecs.open(file_name, "r", "utf8") as f:
            contents = f.readlines()
            start = contents.index("\\ifStatement\r\n")
            end = start + 1
            while (contents[end] != "\\fi\r\n"):
                end += 1

            #for i in range(start + 1, end):
            #    print(contents[i], end="")

            for i in range(end - 1, start, -1):
                if contents[i] != '\r\n' and contents[i] != "\\newpage\r\n":
                    break
                elif contents[i] == "\\newpage\r\n":
                    with codecs.open(destination_file, "a", "utf8") as g:
                        g.write(stripBeginning(file_name) + "\r\n")

teemad = ["Dünaamika", "Elektriahelad", "Elektrostaatika", "Gaasid", "Geomeetriline-optika", "Kinemaatika", "Magnetism", "Staatika", "Taevamehaanika", "Termodünaamika", "Varia", "Vedelike-mehaanika"]
def determineTopics(directory = ""):
    if directory == "":
        all_files = os.listdir()
    else:
        all_files = os.listdir(directory)
    for file_name in all_files:
        if isValidFileName(file_name):
            with codecs.open(directory + file_name, "r", "utf8") as f:
                contents = f.read()
                loc = contents.index("Teema: ") + len("Teema: ")
                topic = ""
                while (contents[loc] != "\n"):
                    topic += contents[loc]
                    loc += 1
                if topic == "Töötlemata":
                    print("Options:")
                    for i in range(len(teemad)):
                        print(f"\t{i}: {teemad[i]}")
                    str = input(f"Topic of {file_name}: ")
                    if (str.isdigit() and int(str) < len(teemad)):
                        str = teemad[int(str)]
                    print(f"Chosen topic was {str}")
                    print("=============================")

# dir_eng to dir_est
def superimpose(dir_eng, dir_est):
    eng_files = os.listdir(dir_eng)
    for file_name in eng_files:
        if isValidFileName(file_name):
            with codecs.open(dir_eng + file_name, "r", "utf8") as f:
                eng = ProblemText(f.read())
                with codecs.open(dir_est + file_name, "r", "utf8") as g:
                    est = tidy(g.read())

            statement = eng.get_if("EngStatement")
            hint = eng.get_if("EngHint")
            sol = eng.get_if("EngSolution")

            i = len(est) - 1
            while i >= 0:
                if est.startswith("\\fi\n", i):
                    i += len("\\fi\n")
                    est = est[:i] + "\n\n" + statement + "\n\n\n" + hint + "\n\n\n" + sol + "\n" + est[i:]
                    break
                i -= 1
            print(dir_est + file_name)
            with codecs.open(dir_est + file_name, "w", "utf8") as f:
                f.write(est.replace("\n", "\r\n"))


def authorer(collection):
    covered = {}
    names = []

    cnt = 0
    for prob in collection.problems:
        #print(prob.author)
        if prob.author not in covered:
            covered[prob.author] = prob.author
            names.append(prob.author)
        cnt += 1

    names.sort()
    with codecs.open("autorid.txt", "w", "utf8") as f:
        for name in names:
            print(name)
            f.write(name)
            f.write('\r\n')
    print(cnt)

#determineTopics("problems/")

'''
directory = "200-test/"
cnt = 0
for file_name in os.listdir(directory):
    if isValidFileName(file_name):
        cnt += 1
        locate(directory + file_name, "config.txt")
print(cnt)
'''
manager = ProblemManager()
manager.load_directory('problems/')
manager.partition_into_books()

collection = manager.collection_one
authorer(collection)

#transcribe("problems/")
#transcribe("", "Töötlemata")
#superimpose("rael/rael/", "problems - Copy (2)/")
teemad = ["Dünaamika", "Elektriahelad", "Elektrostaatika", "Gaasid", "Geomeetriline-optika", "Kinemaatika", "Magnetism", "Staatika", "Taevamehaanika", "Termodünaamika", "Varia", "Vedelike-mehaanika"]

#for directory in teemad:
#    transcribe(directory + "/", directory)
