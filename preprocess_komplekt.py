import os
import codecs
from shutil import copyfile
from python_dependencies.utils import ProblemText, tidy
from python_dependencies.problem_manager import Problem, Collection, ProblemManager
from glob import glob
from pathlib import Path
import re
import numpy as np


def extract_command(contents, command, raise_error=True):
    # Extracts the contents of a command from the contents and returns the contents without the command and command argument
    # E.g. command = \yl
    # Also asserts that this command appears only once
    if contents.count(command) != 1:
        if raise_error:
            error_msg = f'Expected 1 occurence of {command}, got {contents.count(command)}'
            raise ValueError(error_msg)
        return contents, ''
    s = command.replace('\\', '\\\\') + r'\{(.+?)\}'
    command_arg = re.search(s, contents).group(1)
    #title = re.search(r'\\yl\{(.+?)\}', prob_content).group(1)
    it = contents.find(command + r'{')

    def scuffed_lstrip(s):
        # strip but with strings not only chars. Only allow one new line to be stripped
        banned_strs = ['\n', ' ', '\r', '\t', '\\\\']
        i = 0
        newline_cnt = 0
        while i < len(s):
            if not any([s[i:].startswith(banned_str) for banned_str in banned_strs]):
                break
            if s[i] == '\n':
                newline_cnt += 1
                if newline_cnt > 1:
                    break
            i += 1
        return s[i:]

    contents = contents[:it] + scuffed_lstrip(contents[it + contents[it:].find('}') + 1:])
    if contents.count(command) != 0:
        if raise_error:
            error_msg = f'Expected 0 occurences of {command}, got {contents.count(command)}'
            raise ValueError(error_msg)
    return contents, command_arg


def process_prob(fname_probs, dir_dest):
    with codecs.open(fname_probs, "r", "utf8") as f:
        contents = f.read()

    # Remove all occurences of \newpage and \pagebreak
    contents = contents.replace('\\newpage', '')
    contents = contents.replace('\\pagebreak', '')

    # There are 10 problems in each file. The titles are defined by latex command \yl{...}
    # Regex for extracting positions where we have \yl{...}
    it_probs = [m.start() for m in re.finditer(r'\\yl\{', contents)]
    assert len(it_probs) == 10, f'Expected 10 problems, got {len(it_probs)} for {dir_name}'
    
    # Parse each problem
    for i in range(10):
        it_start = it_probs[i]
        
        # There are sometimes wrapfigures which preced the problem, count them in too
        it = contents[:it_start].rfind(r'\end{wrapfigure}')
        if it != -1:
            s = contents[it + len(r'\end{wrapfigure}'):it_start].strip()
            if s == '':
                it_probs[i] = contents[:it_start].rfind(r'\begin{wrapfigure}')


    for i in range(10):
        it_start, it_end = it_probs[i], it_probs[i+1] if i < 9 else contents.rfind(r'\end{document}')
        prob_content = contents[it_start:it_end]
        
        # Extract problem title with regex
        prob_content, title = extract_command(prob_content, r'\yl')
        title = title.strip().lower().capitalize()

        # Extract problem difficulty
        prob_content, difficulty = extract_command(prob_content, r'\punktid')
        # Extract problem author
        prob_content, author = extract_command(prob_content, r'\autor', raise_error=False)
        if author == 'Oleg Ko\\v sik':
            author = 'Oleg Košik'
        if author == 'VALTER KIISK':
            author = 'Valter Kiisk'
        all_authors.append(author)


        # File name
        fname = f'{year}-{round}-{i + 1:02d}.tex'
        #print(f'{fname}: {title}, {author}, {difficulty}p')

        # Adapt every figure to follow the correct format
        # First figure out the figures that the .tex references
        # 1. \includegraphics[...][<figure_name>]
        its = [m.start() for m in re.finditer(r'\\includegraphics', prob_content)]
        n_figs = len(its)
        if n_figs > 0:
            new_prob_content = prob_content[:its[0]] # Replace the figure names in problem content
            for j, it in enumerate(its):
                s = prob_content[it:]

                figure_name = s[s.find(r'{') + 1:s.find(r'}')]
                figure_name = Path(figure_name).stem
                figure_fname = glob(os.path.join(dir_name, figure_name + '.*'))
                if len(figure_fname) == 0:
                    print(f'  Figure {figure_name} not found in {dir_name}!')
                if len(figure_fname) > 1:
                    print(f'  Multiple figures found for {figure_name} in {dir_name}!')
                
                suffix = '' if n_figs == 1 else f'{j + 1}'
                figure_target_name = f'{year}-{round}-{i + 1:02d}-yl{suffix}' + Path(figure_fname[0]).suffix
                new_prob_content += s[:s.find(r'{') + 1] + figure_target_name
                if j < n_figs - 1:
                    new_prob_content += s[s.find(r'}'):its[j + 1]]
                else:
                    new_prob_content += s[s.find(r'}'):]

                figure_target_fname = os.path.join(dir_dest, figure_target_name)
                print(f'  Copying {figure_fname[0]} to {figure_target_fname}')
                copyfile(figure_fname[0], figure_target_fname)
            prob_content = new_prob_content

        # Construct the formated problem content
        formatted_content = f'\\setAuthor{{{author}}}\n'
        formatted_content += f'\\setRound{{{round_longform}}}\n'
        formatted_content += f'\\setYear{{{year}}}\n'
        formatted_content += f'\\setNumber{{G {i + 1}}}\n'
        formatted_content += f'\\setDifficulty{{{i + 1}}}\n'
        formatted_content += f'\\setTopic{{TODO}}\n'
        formatted_content += f'\n\\prob{{{title}}}\n'
        formatted_content += prob_content
        formatted_content += '\n\\hint\n\n\\solu\n'
        formatted_content += '\\probend'

        # Save the contents to a new file
        with codecs.open(os.path.join(dir_dest, fname), "w", "utf8") as f:
            f.write(formatted_content)


def process_sols(fname_sols, dir_dest):
    with codecs.open(fname_sols, "r", "utf8") as f:
        contents = f.read()


    # Remove all occurences of \newpage and \pagebreak
    contents = contents.replace('\\newpage', '')
    contents = contents.replace('\\pagebreak', '')

    # There are 10 problems in each file. The titles are defined by latex command \yl{...}
    # Regex for extracting positions where we have \yl{...}
    it_probs = [m.start() for m in re.finditer(r'\\yl\{', contents)]
    assert len(it_probs) == 10, f'Expected 10 problems, got {len(it_probs)} for {dir_name}'
    
    # Parse each problem
    for i in range(10):
        it_start = it_probs[i]
        
        # There are sometimes wrapfigures which preced the problem, count them in too
        it = contents[:it_start].rfind(r'\end{wrapfigure}')
        if it != -1:
            s = contents[it + len(r'\end{wrapfigure}'):it_start].strip()
            if s == '':
                it_probs[i] = contents[:it_start].rfind(r'\begin{wrapfigure}')

    for i in range(10):
        it_start, it_end = it_probs[i], it_probs[i+1] if i < 9 else contents.rfind(r'\end{document}')
        prob_content = contents[it_start:it_end]
        
        # Remove title, score and author from the problem content
        prob_content, _ = extract_command(prob_content, r'\yl')
        prob_content, _ = extract_command(prob_content, r'\punktid', raise_error=False)
        prob_content, _ = extract_command(prob_content, r'\autor', raise_error=False)

        # File name
        fname = f'{year}-{round}-{i + 1:02d}.tex'
        # Adapt every figure to follow the correct format
        # First figure out the figures that the .tex references
        # 1. \includegraphics[...][<figure_name>]
        its = [m.start() for m in re.finditer(r'\\includegraphics', prob_content)]
        n_figs = len(its)
        if n_figs > 0:
            new_prob_content = prob_content[:its[0]] # Replace the figure names in problem content
            for j, it in enumerate(its):
                s = prob_content[it:]

                figure_name = s[s.find(r'{') + 1:s.find(r'}')]
                figure_name = Path(figure_name).stem
                figure_fname = glob(os.path.join(dir_name, figure_name + '.*'))
                if len(figure_fname) == 0:
                    print(f'  Figure {figure_name} not found in {dir_name}!')
                if len(figure_fname) > 1:
                    print(f'  Multiple figures found for {figure_name} in {dir_name}!')
                
                suffix = '' if n_figs == 1 else f'{j + 1}'
                figure_target_name = f'{year}-{round}-{i + 1:02d}-yl{suffix}' + Path(figure_fname[0]).suffix
                new_prob_content += s[:s.find(r'{') + 1] + figure_target_name
                if j < n_figs - 1:
                    new_prob_content += s[s.find(r'}'):its[j + 1] - its[j]]
                else:
                    new_prob_content += s[s.find(r'}'):]

                figure_target_fname = os.path.join(dir_dest, figure_target_name)
                print(f'  Copying {figure_fname[0]} to {figure_target_fname}')
                copyfile(figure_fname[0], figure_target_fname)
            prob_content = new_prob_content
        
        # Load in previous problem content
        prob = Problem(fname, dir_dest).problem_text
        prob.update_text_segment(prob_content.strip() + '\n', r'\solu')
        #print(prob.get_contents())
        with codecs.open(os.path.join(dir_dest, fname), "w", "utf8") as f:
            f.write(prob.get_contents())
        print(f'  Updated solutions for {fname}')


if __name__ == '__main__':
    dir_orig = 'probs_raw_b3/'
    dir_dest = 'probs_b3/'

    dir_names = glob(dir_orig + '*')
    all_authors = []

    for dir_name in dir_names:
        # The directory name is in format 2018_lahg, first 4 chars are the year, last are the round
        # Get the last directory
        year = dir_name.split(os.sep)[-1].split('_')[0]
        round = dir_name.split(os.sep)[-1].split('_')[1]
        round_longform = {'lahg': 'lahtine', 'v2g': 'piirkonnavoor', 'v3g': 'lõppvoor'}[round]

        print(f'Processing {dir_name}')
        fname_probs = os.path.join(dir_name, 'Problems.tex')
        fname_sols = os.path.join(dir_name, 'Solutions.tex')
        assert os.path.exists(fname_probs), f'File {fname_probs} does not exist'
        assert os.path.exists(fname_sols), f'File {fname_sols} does not exist'
        process_prob(fname_probs, dir_dest)

        process_sols(fname_sols, dir_dest)
