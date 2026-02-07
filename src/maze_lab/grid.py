from collections.abc import Iterator
from dataclasses import dataclass
from enum import IntEnum


@dataclass(frozen=True, slots=True)
class Pos:
    x: int
    y: int


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

    @property
    def dx(self) -> int:
        return {Direction.N: 0, Direction.E: 1, Direction.S: 0, Direction.W: -1}[self]

    @property
    def dy(self) -> int:
        return {Direction.N: -1, Direction.E: 0, Direction.S: 1, Direction.W: 0}[self]

    @property
    def bit(self) -> int:
        return 1 << int(self)

    @property
    def opposite(self) -> "Direction":
        return {
            Direction.N: Direction.S,
            Direction.E: Direction.W,
            Direction.S: Direction.N,
            Direction.W: Direction.E,
        }[self]


ALL_DIRECTIONS = (Direction.N, Direction.E, Direction.S, Direction.W)
ALL_WALLS_MASK = sum(d.bit for d in ALL_DIRECTIONS)


class Grid:
    """
    A Rectangular Grid. Each cell stores walls as a 4 bit mask (N/E/S/W) where 1 means that a wall
    is present.
    """

    __slots__ = ("width", "height", "_walls")

    width: int
    height: int
    _walls: list[int]

    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("grid width and height must be greater than 0")
        self.width = width
        self.height = height
        self._walls = [ALL_WALLS_MASK] * width * height

    def __len__(self) -> int:
        return self.width * self.height

    def in_bounds(self, p: Pos) -> bool:
        return 0 <= p.x < self.width and 0 <= p.y < self.height

    def index(self, p: Pos) -> int:
        if not self.in_bounds(p):
            raise IndexError(f"{p} is out of bounds!")
        return p.y * self.width + p.x

    def wall_mask(self, p: Pos) -> int:
        return self._walls[self.index(p)]

    def has_wall(self, p: Pos, d: Direction) -> bool:
        return (self.wall_mask(p) & d.bit) != 0

    def neighbour_pos(self, p: Pos, d: Direction) -> Pos:
        return Pos(p.x + d.dx, p.y + d.dy)

    def iter_adjacent_in_bounds(self, p: Pos) -> Iterator[tuple[Direction, Pos]]:
        for d in ALL_DIRECTIONS:
            pos = Pos(p.x + d.dx, p.y + d.dy)
            if self.in_bounds(pos):
                yield d, pos

    def iter_neighbours(self, p: Pos) -> Iterator[Pos]:
        for d, pos in self.iter_adjacent_in_bounds(p):
            if not self.has_wall(p, d):
                yield pos

    def carve(self, p: Pos, d: Direction) -> Pos:
        pos = self.neighbour_pos(p, d)
        if not self.in_bounds(p) or not self.in_bounds(pos):
            raise ValueError("Cannot carve out of bounds")
        p_ind = self.index(p)
        pos_ind = self.index(pos)
        self._walls[p_ind] &= ~d.bit
        self._walls[pos_ind] &= ~d.opposite.bit
        return pos

    def passages_from(self, p: Pos) -> list[Direction]:
        mask = self.wall_mask(p)
        return [d for d in ALL_DIRECTIONS if mask & d.bit == 0]

    def count_open_edges(self) -> int:
        edges = 0
        for y in range(self.height):
            for x in range(self.width):
                p = Pos(x, y)
                if x + 1 < self.width and not self.has_wall(p, Direction.E):
                    edges += 1
                if y + 1 < self.height and not self.has_wall(p, Direction.S):
                    edges += 1
        return edges
