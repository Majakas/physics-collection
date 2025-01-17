# coding: utf-8
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if os.path.dirname(__file__) != '':
    os.chdir(os.path.dirname(__file__))

from python_dependencies.problem_manager import ProblemManager, generate_pdf
from python_dependencies.utils import read_config, results_tabulator, table_title_converter

if not __name__ == "__main__":
    sys.exit()

manager = ProblemManager()
manager.load_directory("../problems/")
manager.partition_into_books()
config = read_config("teine-kogumik-config.txt")

print(f"Number of problems in the manager: {len(manager.problems):}")
print(f"Number of problems in the collection: {len(manager.collection_two.problems):}")

prev_prob_num = 0
prev_prob = None

manager.collection_one.problem_sort_by_year()
for i, prob in enumerate(manager.collection_one.problems):
    while prob.number != prev_prob_num + 1:
        print(f"Problem number {prev_prob_num + 1} is missing")
        print(prob.year, prob.round)
        prev_prob_num = (prev_prob_num + 1) % 10
    prev_prob_num = prob.number % 10
