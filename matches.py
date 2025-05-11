from typing import List

from poule import Poule

def create_matches(names, n_poules) -> List[Poule]:
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
