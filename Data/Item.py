from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Item:
    V: List[Tuple[int, int, int]]
    E: List[Tuple[int, int]]
    Y: List[int]
