from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Map_input:
    map_data: List[List[int]]
    percentage_obstacles: float
    id: int
    map_id: int
    size: int