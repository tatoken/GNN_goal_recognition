from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class MapFirstType:
    map_data: List[List[int]]
    source_destinations: List[Tuple[int, int]]
    percentage_obstacles: float
    id: int
    map_id: int
    size: int