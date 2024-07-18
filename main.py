import random
from typing import List, Tuple
import pandas as pd


class Poule:
    def __init__(self, persons: List[str], index: int = -1):
        self._persons = persons
        self._index = index

    def get_persons(self):
        return self._persons

    def get_matches(self) -> List[Tuple[str, str]]:
        r = []
        for a, person1 in enumerate(self._persons):
            for b in range(a + 1, len(self._persons)):
                r.append((person1, self._persons[b]))
        return r


def create_matches(names, n_poules):
    n_persons_per_poule = len(names) // n_poules
    n_persons_left = len(names) % n_poules
    poules = []
    for p in range(n_poules):
        if p < n_persons_left:
            poules.append(Poule(names[p * n_persons_per_poule: (p + 1) * n_persons_per_poule] + [names[-(p + 1)]], index=p))
        else:
            poules.append(Poule(names[p * n_persons_per_poule: (p + 1) * n_persons_per_poule], index=p))

    for poule in poules:
        print(f"poule {poule._index} ("
              f"n_matches: {len(poule.get_matches())}, "
              f"n_persons: {len(poule.get_persons())}) "
              f"{poule.get_matches()}")
    return poules


def create_columns(poules):
    n_columns = 3
    columns = [[] for _ in range(n_columns * 5)]
    max_rows = -1
    for p in range(len(poules)):
        col = p % n_columns
        row = p // n_columns
        m = poules[p].get_matches()
        id = f"{poules[p]._index + 1}"
        columns[col * 5].extend([id] + [n[0] for n in m] + [""])
        columns[(col * 5) + 1].extend([""] + [n[1] for n in m] + [""])
        columns[(col * 5) + 2].extend([""] + ["<winner>" for n in m] + [""])
        columns[(col * 5) + 3].extend([""] + ["<score>" for n in m] + [""])
        columns[(col * 5) + 4].extend([""] + ["" for n in m] + [""])
        if len(columns[col * 5]) > max_rows:
            max_rows = len(columns[col * 5])

    # Add padding
    columns = [c + ([""] * (max(max_rows - len(c), 0) + 1)) for c in columns]
    return columns


# names = [f"name_{i}" for i in range(23)]
names = [str(s).strip() for s in open("c:/projects/names.txt").readlines()]
random.shuffle(names)

n_first_poules = 5
n_second_poules = 2

first_poules = create_matches(names=names, n_poules=n_first_poules)
first_columns = create_columns(first_poules)

if n_second_poules > 0:
    winners = [f"Win of {i+1}" for i in range(len(first_poules))]
    second_poules = create_matches(names=winners, n_poules=n_second_poules)

    second_columns = create_columns(second_poules)
    columns = [f + s for f, s in zip(first_columns, second_columns)]
else:
    columns = first_columns

d = {i:c for i,c in enumerate(columns)}
df = pd.DataFrame.from_dict(d)
df.to_csv("c:/projects/schema.csv", index=False, header=False)
