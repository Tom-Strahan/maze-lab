from collections import deque
from dataclasses import dataclass

from maze_lab.grid import Grid, Pos


@dataclass(frozen=True, slots=True)
class BfsResult:
    start: Pos
    goal: Pos
    found: bool
    visited_order: list[Pos]
    came_from: dict[Pos, Pos | None]
    path: list[Pos]


def _reconstruct_path(came_from: dict[Pos, Pos | None], goal: Pos, start: Pos) -> list[Pos]:
    if goal not in came_from:
        return []

    path: list[Pos] = []
    current: Pos | None = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path if path and path[0] == start else []


def bfs(g: Grid, *, start: Pos, goal: Pos) -> BfsResult:
    if not g.in_bounds(start) or not g.in_bounds(goal):
        raise ValueError(f"start {start} and goal {goal} must be in bounds")

    visited_order: list[Pos] = []
    came_from: dict[Pos, Pos | None] = {start: None}

    if start == goal:
        return BfsResult(
            start=start,
            goal=goal,
            found=True,
            visited_order=[start],
            came_from=came_from,
            path=[start],
        )
    q: deque[Pos] = deque([start])

    while q:
        p = q.popleft()
        visited_order.append(p)

        if p == goal:
            break

        for nxt in g.iter_neighbours(p):
            if nxt not in came_from:
                came_from[nxt] = p
                q.append(nxt)

    path = _reconstruct_path(came_from, goal, start)
    found = len(path) > 0 and path[-1] == goal

    return BfsResult(
        start=start,
        goal=goal,
        found=found,
        visited_order=visited_order,
        came_from=came_from,
        path=path,
    )
