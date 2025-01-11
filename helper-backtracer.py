import argparse
import codecs

from python_dependencies.problem_manager import ProblemManager, generate_pdf, Problem, round_to_abbreviation
import python_dependencies.utils as utils


def capture_argument(contents, command_name):
    """
    Capture the argument of a command, e.g. if command_name="\setAuthor" we get
    from the first occurence of \setAuthor{argument} -> argument
    """
    i = contents.find(command_name)
    if i == -1:
        return -1
    i_start = contents[i:].find("{")
    i_end = contents[i + i_start:].find("}")
    return contents[i + i_start + 1:i + i_start + i_end]


if __name__ == "__main__":
    """
    This helper script is used for more convenient editing of multiple problems at once.
    It reads the book .tex file and compares it to the original source files of the problems and proposes the updates to the source files.
    """
    parser = argparse.ArgumentParser(description='Backpropagate the updates made into the book .tex file to the problem source files.')
    parser.add_argument(
        '--source',
        type=str,
        default = "",
        help='Specify the location of the book .tex file.')
    parser.add_argument(
        '--problem-folder',
        type=str,
        default = "problems/",
        help='Specify the location of the problem source files.')
    problem_metadata = parser.parse_args()


    def tidy(str):
        return str.replace("\r\n", "\n").replace("\r", "\n")

    source = problem_metadata.source
    problem_folder = problem_metadata.problem_folder
    #python ..\helper-backtracer.py --source kolmas-kogumik-veeb.tex --problem-folder ../probs_b3/

    manager = ProblemManager()
    manager.load_directory(problem_folder)
    manager.partition_into_books()

    contents = ""
    with codecs.open(source, "r", "utf8") as f:
        contents = tidy(f.read())

    i_contents = 0
    problem_cnt = 0

    is_english = False
    # Dictionary that keeps track of the frequency of each argument in each problem.
    # We update the argument of the problem in its source file if the frequency of an argument in a problem is equal to 1!
    # This is so that we only have to edit an argument in the book .text only once (the old argument can appear twice in two out of problem texts, hints and solutions).
    problems_args_dict = [{} for i in range(7)]
    while i_contents < len(contents):
        if contents.startswith(r"\setAuthor{", i_contents):
            i_problem_end = i_contents + contents[i_contents:].find(r"\probend") + len(r"\probend")

            problem_content = utils.ProblemText(contents[i_contents:i_problem_end])
            i_contents = i_problem_end
            
            problem_cnt += 1

            problem_metadata = problem_content.metadata
            file_name = f'{problem_metadata[3]}-{round_to_abbreviation(problem_metadata[2])}-{int(problem_metadata[4][2:]):02}.tex'
            problem_from_file = Problem(file_name, problem_folder).problem_text
            for i in range(6):
                if len(problem_content.text[i]) > 0:
                    old_text = problem_from_file.text[i]
                    new_text = problem_content.text[i]
                    if old_text != new_text:
                        print(f"{problem_content.text_identifiers[i][1:]} of problem {file_name} needs to be updated:\n\tP{(problem_cnt-1)%200+1}: {problem_metadata[0]}\n\told length: {len(old_text)}, new length: {len(new_text)}")

                        print(repr(old_text))
                        print(repr(new_text))
                        input("\tProceed?")
                        problem_from_file.update_text_segment(new_text, problem_from_file.text_identifiers[i])
                        with codecs.open(problem_folder + file_name, "w", "utf8") as f:
                            f.write(problem_from_file.get_contents().replace("\n", "\r\n"))
                            print("Success")

            for j in range(7):
                if j != 2 and not (j == 0 and is_english):
                    if file_name not in problems_args_dict[j]:
                        problems_args_dict[j][file_name] = {}
                    if problem_metadata[j] not in problems_args_dict[j][file_name]:
                        problems_args_dict[j][file_name][problem_metadata[j]] = 0
                    problems_args_dict[j][file_name][problem_metadata[j]] += 1
        else:
            i_contents += 1

    # Update metadata
    for i in range(7):
        if i != 2 and not (i == 0 and is_english):
            for file_name, dict in problems_args_dict[i].items():
                min_freq = 1000
                min_metadata = ""
                for metadata, freq in dict.items():
                    if freq < min_freq:
                        min_freq = freq
                        min_metadata = metadata

                if min_freq < 3:
                    new_metadata = min_metadata
                    problem_from_file = Problem(file_name, problem_folder).problem_text

                    if new_metadata == problem_from_file.metadata[i]:
                        continue

                    descriptions = ["problem name", "author", "round", "year", "problem number", "difficulty", "topic"]

                    print(f"Updating the {descriptions[i]} of problem {file_name}:\n\told {descriptions[i]}: {problem_from_file.metadata[i]}, new {descriptions[i]}: {new_metadata}")
                    problem_from_file.update_metadata(new_metadata, i)

                    input("\tProceed?")
                    with codecs.open(problem_folder + file_name, "w", "utf8") as f:
                        f.write(problem_from_file.get_contents().replace("\n", "\r\n"))
                        print("Success")

    print(f'Number of passes: {problem_cnt}')
