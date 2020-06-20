import matplotlib.pyplot as plt

from python_dependencies.problem_manager import ProblemManager, generate_pdf, Problem
from python_dependencies.utils import ProblemText

manager = ProblemManager()
manager.load_directory('problems/')
manager.partition_into_books()

collection = manager.collection_two

round_counter = {}
years = {}
lahg = {}
v2g = {}
v3g = {}
cnt = 0
for i in range(2005, 2012):
    lahg[i] = 0
    v2g[i] = 0
    v3g[i] = 0
for prob in collection.problems:
    if prob.round not in round_counter:
        round_counter[prob.round] = 0
    if prob.year not in years:
        years[prob.year] = 0
    if prob.author == 'Tundmatu autor':
        cnt += 1
        round_counter[prob.round] += 1
        years[prob.year] += 1

        if prob.round == 'lahtine':
            lahg[prob.year] += 1
        elif prob.round == 'piirkonnavoor':
            v2g[prob.year] += 1
        else:
            v3g[prob.year] += 1

for i, j in round_counter.items():
    print(i, j)

print("")
ans = []
for i, j in years.items():
    ans.append((i, j))
    print(i, j)

print(cnt)

v2gu, v3gu, lahgu = [], [], []
for i, j in v2g.items():
    v2gu.append((i, j))
for i, j in v3g.items():
    v3gu.append((i, j))
for i, j in lahg.items():
    lahgu.append((i, j))
v2gu = sorted(v2gu)
v3gu = sorted(v3gu)
lahgu = sorted(lahgu)

ans = sorted(ans)
plt.plot([i[0] for i in v2gu], [i[1] for i in v2gu], label='piirkonnavoor')
plt.plot([i[0] for i in v3gu], [i[1] for i in v3gu], label='lõppvoor')
plt.plot([i[0] for i in lahgu], [i[1] for i in lahgu], label='lahtine')
plt.title('Tundmatute autorite sagedus aastate kaupa')
plt.legend()
plt.grid(True)
plt.show()
