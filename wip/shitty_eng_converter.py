import codecs
import glob
import os
import shutil

from python_dependencies.problem_manager import ProblemManager, generate_pdf, Problem

idx = 0
def getInside(str, target, start, end = ""):
    global idx
    if end == "":
        end = start
    if str.startswith(start, idx):
        idx_start = idx
        #print(str[idx], idx, end="\n")
        idx += 1
        #print(str[idx], idx, end="\n")
        cnt = 0
        while not str.startswith(end, idx):
            cnt += 1
            if cnt > 2000:
                print(f"ran into an endless loop while detecting {start} + {end} with index {idx}")
                #print(str)
                input()
            idx += 1

        idx += len(end)
        #print(idx_start, idx, end="\n")
        target.append(str[idx_start:idx])
        return True
    return False


def check(est, equations):
    types = "equation", "align", "align*", "equation*"
    for t in types:
        if getInside(est, equations, "\\begin{" + t + "}", "\\end{" + t + "}"):
            return True
    if (getInside(est, equations, "$$") or getInside(est, equations, "$") or
       getInside(est, equations, "\\[", "\\]") or getInside(est, equations, "\\(", "\\)")):
        return True
    return False

def checkfigs(est, figs):
    types = "wrapfigure", "wrapfigure*", "figure", "figure*", "center", "tikzpicture", "tikzpicture*"
    for t in types:
        if getInside(est, figs, "\\begin{" + t + "}", "\\end{" + t + "}"):
            return True

    return False

def createEng(problem, rael, type, cnt = 0, name = ""):
    rael = rael.replace("%", r"\%").strip() # Because % is commment in latex

    new_dir = "rael/"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    for file in glob.glob(problem.directory + problem.file_name[0:-4] + "*"):
        if not os.path.exists(new_dir + file.split("\\")[1]):
            shutil.copy(file, new_dir)

    contents = ""
    with codecs.open(new_dir + problem.file_name, "r", "utf8") as f:
        contents = f.read()
        contents = contents.replace("\r\n", "\n")

    engish = type[0:3] + "Eng" + type[3:]
    if contents.find(engish) != -1:
        return 5

    print(f"Attempting {engish[3:]} of P{cnt}, file name: {problem.file_name}")


    global idx
    all_content = problem.get_content()
    all_content = all_content.replace("\r\n", "\n")
    idx = all_content.index(type)
    start_idx = idx
    while all_content.startswith("\\fi\n", idx) == False:
        idx += 1
    est = all_content[start_idx:idx]

    equations = []
    figs = []

    #print(problem.file_name)
    #print(rael)
    idx = 0
    while idx < len(est):
        while check(est, equations):
            pass
        while checkfigs(est, figs):
            pass
        idx += 1
    print(equations)
    eqns_new = []
    for eqn in equations:
        if eqn.startswith("$\\SI") or eqn.startswith("$\\num") or eqn.startswith("$\\si{"):
            pass
        else:
            eqns_new.append(eqn)
    equations = eqns_new
    del eqns_new
    print(equations)

    # If possible, replace figs with the eng counterpart
    figs_new = []
    for fig in figs:
        if fig.find("\\begin{tikzpicture}") != -1 or fig.find("\\begin{circuitikz}") != -1:
            figs_new.append(fig)
            continue
        if fig.find("\\includegraphics") == -1:
            print("Figure not included correctly!")
            pass
        else:
            temp = "\\includegraphics"
            path = ""
            i = fig.index(temp)
            i += len(temp)
            if fig[i] == "[":
                while fig[i] != "]":
                    i += 1
                i += 1
            start_idx = i + 1
            if fig[i] == "{":
                i += 1
                while fig[i] != "}":
                    path += fig[i]
                    i += 1

            if path.endswith(".pdf") or path.endswith(".eps") or path.endswith(".png") or path.endswith(".jpg"):
                path = path[0:-4]
            if glob.glob(problem.directory + path + "_ing.*"):
                path += "_ing"

            fig = fig[0:start_idx] + path + fig[i:]
            figs_new.append(fig)
    figs = figs_new
    del figs_new

    print(f"\tNumber of equations: {len(equations)}")
    print(f"\tNumber of figures: {len(figs)}")

    i_eqn = 0
    i_figs = 0
    i = 0
    while i < len(rael):
        uno = "VALEM"
        if rael.startswith(uno, i):
            if i_eqn == len(equations):
                print(problem.file_name, "Liiga palju VALEM-eid!")
                return False
            rael = rael[0:i] + equations[i_eqn] + rael[i + len(uno):]
            i_eqn += 1
        doi = "JOONIS"
        if rael.startswith(doi, i):
            if i_figs == len(figs):
                print(problem.file_name, "Liiga palju JOONIS-eid!")
                return False
            rael = rael[0:i] + figs[i_figs] + rael[i + len(doi):]
            i_figs += 1
        trei = "NONE"
        if rael.startswith(trei, i):
            if i_eqn == len(equations):
                print(problem.file_name, "Liiga palju VALEM-eid!")
                return False
            i_eqn += 1
        i += 1
    if i_figs != len(figs):
        print(problem.file_name, "Liiga vähe JOONIS-eid!")
        return False
    if i_eqn != len(equations):
        print(problem.file_name, "Liiga vähe VALEM-eid!")
        return False

    #print(rael)

    rael = rael.strip()

    if type == "\\ifStatement":
        i = contents.find("\\ifSolution")
        while not contents.startswith("\\fi\n", i):
            i += 1
        i += 4
        contents = contents[0:i] + "\n\n\\ifEngStatement\n% Problem name: " + name + "\n" + rael + "\n\\fi\n" + contents[i:]
    elif type == "\\ifHint":
        i = max(contents.find("\\ifSolution"), contents.find("\\ifEngStatement"))
        while not contents.startswith("\\fi\n", i):
            i += 1
        i += 4
        contents = contents[0:i] + "\n\n\\ifEngHint\n" + rael + "\n\\fi\n" + contents[i:]
    elif type == "\\ifSolution":
        i = max(contents.find("\\ifSolution"), contents.find("\\ifEngStatement"))
        i = max(i, contents.find("\\ifEngHint"))
        while not contents.startswith("\\fi\n", i):
            i += 1
        i += 4
        contents = contents[0:i] + "\n\n\\ifEngSolution\n" + rael + "\n\\fi\n" + contents[i:]

    with codecs.open(new_dir + problem.file_name, "w", "utf8") as f:
        contents = contents.replace("\n", "\r\n")
        f.write(contents)

    return True



manager = ProblemManager()
manager.load_directory("problems/")
manager.partition_into_books()

rael = ""
with codecs.open("200yl_YES.txt", "r", "utf8") as f:
    rael = f.read()

rael_parsed = []
rael_names = []

cnt = 1
i, start_idx = 0, -1
while i != len(rael):
    if rael[i].isdigit():
        num = ""
        while rael[i].isdigit():
            num += rael[i]
            i += 1
        num = int(num)

        if num == cnt:
            if start_idx != -1:
                rael_parsed.append(rael[start_idx:i-len(str(num))])
            cnt += 1
            name = ""
            while rael[i] != '\n':
                name += rael[i]
                i += 1
            i += 1
            name = name.strip()
            rael_names.append(name)

            start_idx = i
    i += 1
rael_parsed.append(rael[start_idx:len(rael)])

cnt = 1
i, start_idx = 0, -1
with codecs.open("200vihjet.txt", "r", "utf8") as f:
    rael = f.read()
rael_hints = []
while i < len(rael):
    if rael[i].isdigit():
        num = ""
        while rael[i].isdigit():
            num += rael[i]
            i += 1
        num = int(num)

        if num == cnt:
            if start_idx != -1:
                rael_hints.append(rael[start_idx:i-len(str(num))])
            cnt += 1
            while rael[i] != '\n':
                i += 1
            i += 1

            start_idx = i
    i += 1
rael_hints.append(rael[start_idx:len(rael)])

cnt = 1
i, start_idx = 0, -1
with codecs.open("200lah4.txt", "r", "utf8") as f:
    rael = f.read()
rael_solutions = []
while i < len(rael):
    if rael[i].isdigit():
        num = ""
        while rael[i].isdigit():
            num += rael[i]
            i += 1
        num = int(num)

        if num == cnt:
            if start_idx != -1:
                rael_solutions.append(rael[start_idx:i-len(str(num))])
            cnt += 1
            while rael[i] != '\n':
                i += 1
            i += 1

            start_idx = i
    i += 1
rael_solutions.append(rael[start_idx:len(rael)])

#for i in range(len(rael_names)):
#    print(f"{i + 1} {rael_names[i]}:\n{rael_parsed[i]}")

i = 0
failed_statements = 0
for i in range(len(manager.collection_one.problems)):
    status = createEng(manager.collection_one.problems[i], rael_parsed[i], "\\ifStatement", i + 1, rael_names[i])
    if status == False:
        print("Attempt failed...\n")
        failed_statements += 1
    elif status == True:
        print("Attempt successful!\n")

failed_hints = 0
for i in range(len(manager.collection_one.problems)):
    status = createEng(manager.collection_one.problems[i], rael_hints[i], "\\ifHint", i + 1)
    if status == False:
        print("Attempt failed...\n")
        failed_hints += 1
    elif status == True:
        print("Attempt successful!\n")

failed_solutions = 0
for i in range(len(manager.collection_one.problems)):
    status = createEng(manager.collection_one.problems[i], rael_solutions[i], "\\ifSolution", i + 1)
    if status == False:
        print("Attempt failed...\n")
        failed_solutions += 1
    elif status == True:
        print("Attempt successful!\n")

print(f"Number of failed statements: {failed_statements}")
print(f"Number of failed hints: {failed_hints}")
print(f"Number of failed solutions: {failed_solutions}")
