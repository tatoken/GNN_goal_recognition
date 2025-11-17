import random
import json
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


def generate_connected_map(map_id: int, size: int = 4, percentage_obstacles: float = 0.3):
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

    result = {
        "map_id": map_id,
        "size": size,
        "percentage_obstacles": f"{percentage_obstacles:.2f}",
        "map": grid
    }
    return result


def  generate_maps(size_of_maps,random_seed=1,maps_per_file=10,num_file=100,output_dir="maps_generated",obst_perc_min=0,obst_perc_max=0.5):
    random.seed(random_seed)
    os.makedirs(output_dir, exist_ok=True)

    global_map_id = 1

    for file_id in range(1, num_file + 1):
        maps_in_this_file = []

        for _ in range(maps_per_file):
            perc = random.uniform(obst_perc_min, obst_perc_max)
            
            data = generate_connected_map(
                map_id=global_map_id,
                size=size_of_maps,
                percentage_obstacles=perc
            )
            maps_in_this_file.append(data)
            global_map_id += 1

        file_path = os.path.join(
            output_dir, f"maps_dataset_{size_of_maps}_{file_id}.json"
        )

        with open(file_path, "w") as f:
            json.dump(maps_in_this_file, f, indent=2)

generate_maps(8)