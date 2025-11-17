from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Map_path_solution_output:
    V: List[List[Tuple[int, int, int]]]
    E: List[Tuple[int, int]]
    Y: List[List[int]]
    O: List[List[int]] #order of nodes in V paths
    Optimality: List[float]
    AvgLength: float
    ObstaclePerc: float
