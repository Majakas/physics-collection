import codecs
import glob
import re
import os
import shutil
from pathlib import Path

from python_dependencies.problem_manager import ProblemManager, generate_pdf, is_valid_filename

actual_joonised = [x for x in glob.glob("Kogumik/*.png")]
joonised = [x[8:-4] for x in glob.glob("Kogumik/*.png")]


"""for file_name in glob.glob("Kogumik/*.tex"):
    text = ""
    with codecs.open(file_name, "r", "utf8") as f:
        for path in joonised:
            if path in joonised:
                file_name
                print(path + "h")

        #text = f.read().replace("\r\n", "\n").replace("\r", "\n")
        #idx = text.find("\\ifSolution")
        #while text[idx] != "\n":
        #    idx += 1
        #while text[idx - 1] == " ":
        #    text = text[:idx - 1] + text[idx:]

        #text = text.replace("\\fi \n", "\\fi\n")
        #text = text.replace("{Elektriõpetus", "{Elektriopetus")
        #text = text.replace("{Soojusõpetus", "{Soojusopetus")
        #text = text.replace("{Valgusõpetus", "{Valgusopetus")
        #text = text.replace("{Võnkumine", "{Vonkumine")
        #re.sub(r'\s+$', '', text, flags=re.M)
        

        #text = text[text.find("\n")+1:]
        #idx = text.find("% Voor")
        #while text[idx] != "{":
        #    idx -= 1
        #idx += 1
        #text = text[:idx] + text[idx].lower() + text[idx + 1:]

    #with codecs.open(file_name, "w", "utf8") as f:
    #    f.write(text)"""


#exit(0)
manager = ProblemManager()
manager.load_directory("Kogumik/", strict=False)

new_folder = "Kogumik_new/"

if not os.path.exists(new_folder):
    os.makedirs(new_folder)

mapp = {}
for joonis in joonised:
    mapp[joonis] = 0

cnt = 0
cnt1 = 0
nm = {}
for problem in manager.problems:
    text = ""
    new_file_name = f"{problem.year}-{problem.round_abbr}-{problem.number:0>2}.tex"
    with codecs.open("Kogumik/" + problem.file_name, "r", "utf8") as f:
        text = f.read().replace("\r\n", "\n").replace("\r", "\n")

        idx = text.find("% Teema: ") + len("% Teema: ")
        text = text[:idx] + text[idx].upper() + text[idx + 1:]
        lah_cnt = 0
        yl_cnt = 0
        for path in joonised:
            if path in text:
                if path[path.find("_") + 1] == "L":
                    lah_cnt += 1
                else:
                    yl_cnt += 1
        yl_cnt1 = 1
        lah_cnt1 = 1
        for path in joonised:
            if path in text:
                new_name = f"{problem.year}-{problem.round_abbr}-{problem.number:0>2}-"
                if path[path.find("_") + 1] == "L":
                    new_name += "lah"
                    if lah_cnt > 1:
                        new_name += str(lah_cnt1)
                        lah_cnt1 += 1
                else:
                    new_name += "yl"
                    if yl_cnt > 1:
                        new_name += str(yl_cnt1)
                        yl_cnt1 += 1
                #print(problem.file_name, path, new_name)
                text = text.replace(path, new_name)
                cnt1 += 1
                mapp[path] = 1
                shutil.copyfile("Kogumik/" + path + ".png", new_folder + new_name + ".png")
    cnt += 1
    if new_file_name not in nm:
        nm[new_file_name] = [problem.file_name]
    else:
        nm[new_file_name].append(problem.file_name)
    #print(cnt, new_file_name)
    with codecs.open(new_folder + new_file_name, "w", "utf8") as f:
        f.write(text)
    """
    #if int(problem.year) == 2015:
    t = problem.problem_text.get_argument(6)

    new_file_name = f"{problem.year}-{problem.round_abbr}-{problem.number:0>2}"""



    #print(new_file_name)
    """while t[0] == '\n':
        t = t[1:]
    while t[-1] == '\n':
        t = t[:-1]
    teema = ""
    i = 0
    while t[i] != '\n':
        i += 1
    teema = t[:i]
    teema = teema.replace("% Teema: ", "").replace("-", " ")
    print(repr(teema))
    t = t[i + 1:]
    t = replacer(t, "\\ifStatement", "\\statementEst")
    t = replacer(t, "\\ifHint", "\\hintEst")
    t = replacer(t, "\\ifSolution", "\\solutionEst")

    identifier = '% Problem name: '
    idx = t.find(identifier) + len(identifier)
    start = t.find(identifier)
    eng_name = ""
    if idx != len(identifier) - 1:
        eng_name = ''
        while t[idx] != '\n':
            eng_name += t[idx]
            idx += 1
        t = t[:start] + t[idx + 1:]

        idx = t.find("\\ifEngStatement")
        t = t[:idx] + "\\prob{" + eng_name + "}\n" + t[idx:]

        t = replacer(t, "\\ifEngStatement", "\\statementEng")
        t = replacer(t, "\\ifEngHint", "\\hintEng")
        t = replacer(t, "\\ifEngSolution", "\\solutionEng")

    t = t.strip()
    t += "\n\\probEnd"

    new_text = r"\setAuthor{" + problem.author + "}\n\\setRound{" + problem.round + "}\n\\setYear{" + str(problem.year) + "}\n\\setNumber{" + problem.problem_text.get_argument(4) +\
        "}\n\\setDifficulty{" + str(problem.difficulty) + "}\n\\setTopic{" + teema + "}\n\n\\prob{" + problem.name + "}\n" + t
    new_text = new_text.strip("\n")


    my_file = Path(problem.directory + problem.file_name)
    print(my_file.is_file())
    print(repr(problem.directory + problem.file_name))
    print(new_text)
    with codecs.open(new_folder + problem.file_name, "w", "utf8") as f:
        f.write(new_text)"""
print(cnt, cnt1, len(manager.problems), len(joonised))

for it in nm:
    print(it, nm[it])

for it in mapp:
    if mapp[it] == 0:
        print(it, mapp[it])