from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class MapSecondType:
    map_V: List[List[int]]
    source_destination: List[int, int]
    percentage_obstacles: float
    id: int
    map_id: int
    size: int