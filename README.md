# physics-collection

This repository is meant for problem book creation and management. All the problems are kept in separate files following a specific structure and can be then compiled into LaTeX files using python scripts found in the book directories. Currently, a web version and a book version can be generated. Both have separate LaTeX style files.

The repository was developed during the creation of the physics problem collection books from high school division of the Estonian physics olympiad, including the regional, national and open round. There are 2 books, each one containing 200 problems with 30 problems from each year (10 from each round). The books span year 2005 - 2011 and 2012 - 2018.
There's also a web book containing all the problems in the 'problems/' folder.

## Technical details

All the problems are in kept in separate files containing a LaTeX command which, as its arguments, stores the following:
- the problem name
- name of the author
- round of appearance
- year of appearance
- number of the problem in the round
- approximate difficulty out of 10 points
- the statements/hints/solutions separated by LaTeX \if statements. The topic of the problem is on the first line as a comment. Python uses it to sort the problems per topic. Furthermore, the English statement stores the name of the problem in english as the first line after \ifEngStatement.

The compilation of the book follows a class ProblemManager (found in python_dependencies/) that's fed the directories of the problem .tex files and which then handles the sorting of problems and distributing them between "collections" specified by the user. The "collections" are additional classes which store problems (class Problem) which support retrieving the LaTeX code for statements, hints, solutions in both Estonian and English in their tidied form.

When feeding the ProblemManager a folder of .tex files, the file name in fact does not matter as all the relevant info about the problems is kept inside the file.

The final compilation of the book happens in a python script of the same name (for convention) as the book and which uses ProblemManager to retrieve the problems source code in the correct and tidied order and the creates the .tex file for the book and compiles it into a .pdf. 


### helper-backtracer.py

This file allows one to edit the .tex files generated by the python scripts and then update the corresponding problem .tex files by running the script. When the script is run and it encounters modified text, it will ask for confirmation for the text to be updated in the source file. To cancel the update, you need to close the script. For now, updating the problem year, number and round are not recommended as this creates conflicts when opening the source file (the backtracer assumes a specific naming convention for the source files). Furthermore, when updating the problem statement in English, one needs to modify the name after the \ifEngStatement line not the first argument of the \ylDisplay command. 
To run the file, pass the location of the book .tex file as the source argument, e.g. 
```
"python helper-backtracer.py --source="book_one/esimene-kogumik-veeb.tex"
```
TODO: add different cancellation policy.

## License

The python scripts in the project are licensed under the GNU General Public License - see the [LICENSE-GNU.md](LICENSE-GNU.md) file for details

The contents of the problems, including the statements, hints, solutions in both Estonian and English are licensed under the Creative Commons Attribution-NonCommercial 4.0 International Public License - see the [LICENSE-CC.md](LICENSE-CC.md) file for details
