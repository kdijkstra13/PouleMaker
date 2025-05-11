from typing import List, Tuple

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
