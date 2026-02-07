import random

from maze_lab.grid import Direction, Grid, Pos


def generate_dfs_backtracker(
    grid: Grid, *, start: Pos | None = None, rng: random.Random | None = None
) -> None:
    """
    Generates a maze using depth first search with backtracking. Mutates the grid by carving
    passages.

    Args:
        grid: Grid to carve into.
        start: Starting cell (must be in bounds).
        rng: Optional Random instance for deterministic generation.
    """
    if start is None:
        start = Pos(0, 0)
    if not grid.in_bounds(start):
        raise ValueError(f"start position: {start} is out of bounds")

    r = rng if rng is not None else random.Random()

    visited: set[Pos] = {start}
    stack: list[Pos] = [start]

    while stack:
        p = stack[-1]

        candidates: list[tuple[Direction, Pos]] = []
        for dir, pos in grid.iter_adjacent_in_bounds(p):
            if pos not in visited:
                candidates.append((dir, pos))

        if not candidates:
            stack.pop()
            continue

        dir, pos = r.choice(candidates)
        grid.carve(p, dir)
        visited.add(pos)
        stack.append(pos)
