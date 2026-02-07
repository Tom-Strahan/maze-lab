import random

from maze_lab.generate.dfs_backtracker import generate_dfs_backtracker
from maze_lab.grid import Grid, Pos
from maze_lab.solve.bfs import bfs


def test_start_equals_goal() -> None:
    g = Grid(3, 3)
    res = bfs(g, start=Pos(2, 2), goal=Pos(2, 2))
    assert res.found
    assert res.path == [Pos(2, 2)]


def test_bfs_finds_path_in_maze() -> None:
    g = Grid(10, 10)
    generate_dfs_backtracker(g, start=Pos(0, 0), rng=random.Random(123))
    res = bfs(g, start=Pos(0, 0), goal=Pos(9, 9))
    assert res.found
    assert res.path[0] == Pos(0, 0)
    assert res.path[-1] == Pos(9, 9)

    for a, b in zip(res.path, res.path[1:], strict=False):
        assert b in set(g.iter_neighbours(a))


def test_bfs_returns_not_found_when_no_path() -> None:
    g = Grid(4, 4)  # Default grid is all walls, no path
    res = bfs(g, start=Pos(0, 0), goal=Pos(3, 3))
    assert not res.found
    assert res.path == []
