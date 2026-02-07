import pytest

from maze_lab.grid import Direction, Grid, Pos


def test_grid_initially_has_all_walls() -> None:
    g = Grid(3, 2)
    for y in range(g.height):
        for x in range(g.width):
            assert g.wall_mask(Pos(x, y)) == 0b1111  # 15 is 1111 (all walls)


def test_carve_removes_walls_both_sides() -> None:
    g = Grid(2, 1)
    p = Pos(0, 0)
    assert g.has_wall(p, Direction.E)

    q = g.carve(p, Direction.E)
    assert q == Pos(1, 0)
    assert not g.has_wall(p, Direction.E)
    assert not g.has_wall(q, Direction.W)


def test_iter_neighbours_respects_walls() -> None:
    g = Grid(2, 1)
    p = Pos(0, 0)

    assert list(g.iter_neighbours(p)) == []

    g.carve(p, Direction.E)
    assert list(g.iter_neighbours(p)) == [Pos(1, 0)]


def test_carve_out_of_bounds_raises() -> None:
    g = Grid(1, 1)
    with pytest.raises(ValueError):
        g.carve(Pos(0, 0), Direction.N)
