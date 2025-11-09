import random
import json
from collections import deque
import os

def is_connected(grid):
    size = len(grid)
    free_cells = [(r, c) for r in range(size) for c in range(size) if grid[r][c] == 0]

    if not free_cells:
        return False

    visited = set()
    stack = [free_cells[0]]
    visited.add(free_cells[0])

    while stack:
        r, c = stack.pop()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append((nr, nc))

    return len(visited) == len(free_cells)


def generate_connected_map(map_id: int, size: int = 4, percentage_obstacles: float = 0.3, n_instances: int = 10):
    total_cells = size * size
    n_obstacles = int(total_cells * percentage_obstacles)

    # Start con mappa vuota
    grid = [[0 for _ in range(size)] for _ in range(size)]
    all_positions = [(r, c) for r in range(size) for c in range(size)]

    # Piazza ostacoli garantendo connettività
    placed = 0
    attempts = 0
    while placed < n_obstacles and attempts < total_cells * 5:
        r, c = random.choice(all_positions)
        if grid[r][c] == 1:
            attempts += 1
            continue
        grid[r][c] = 1
        if is_connected(grid):
            placed += 1
        else:
            grid[r][c] = 0
        attempts += 1

    # Celle libere lineari
    free_cells = [r * size + c for r in range(size) for c in range(size) if grid[r][c] == 0]

    # Genera istanze source-destination
    instances = []
    for inst_id in range(n_instances):
        if len(free_cells) < 2:
            break
        src, dst = random.sample(free_cells, 2)
        instances.append({
            "id": map_id * 10000 + inst_id,
            "source_destination": [src, dst]
        })

    result = {
        "map_id": map_id,
        "size": size,
        "percentage_obstacles": f"{percentage_obstacles:.2f}",
        "map": grid,
        "instances": instances
    }
    return result


if __name__ == "__main__":
    random.seed(42)
    output_dir = "datasetMapsNew/maps_dataset_8"
    os.makedirs(output_dir, exist_ok=True)

    for file_id in range(1, 101):  # 100 file
        perc = random.uniform(0, 0.7)
        data = generate_connected_map(
            map_id=file_id,
            size=8,
            percentage_obstacles=perc,
            n_instances=10
        )
        file_path = os.path.join(output_dir, f"maps_dataset_8_{file_id}.json")
        with open(file_path, "w") as f:
            json.dump([data], f, indent=2)

    print("✅ Generati 100 file JSON nella cartella 'maps_output'")
