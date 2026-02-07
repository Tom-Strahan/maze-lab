import random
from collections import deque

from maze_lab.generate.dfs_backtracker import generate_dfs_backtracker
from maze_lab.grid import Grid, Pos


def bfs_reachable_count(g: Grid, start: Pos) -> int:
    seen = {start}
    q: deque[Pos] = deque([start])

    while q:
        p = q.popleft()

        for nxt in g.iter_neighbours(p):
            if nxt not in seen:
                q.append(nxt)
                seen.add(nxt)

    return len(seen)


def test_dfs_backtracker_generates_perfect_maze_edges() -> None:
    g = Grid(5, 6)
    generate_dfs_backtracker(g, start=Pos(0, 0), rng=random.Random(123))
    assert g.count_open_edges() == len(g) - 1


def test_dfs_backtracker_generates_conencted_maze() -> None:
    g = Grid(10, 10)
    generate_dfs_backtracker(g, start=Pos(4, 8), rng=random.Random(123))
    assert bfs_reachable_count(g, Pos(4, 8)) == len(g)
