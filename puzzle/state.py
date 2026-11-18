from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVES = (
    ("UP", -1, 0),
    ("DOWN", 1, 0),
    ("LEFT", 0, -1),
    ("RIGHT", 0, 1),
)


class State:
    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def is_solvable(self) -> bool:
        tiles = [t for t in self.tiles if t != 0]
        inversions = sum(
            1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j]
        )
        return inversions % 2 == 0

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        children: List["State"] = []
        blank = self.blank_index
        row, col = divmod(blank, 3)

        for action, d_row, d_col in MOVES:
            new_row, new_col = row + d_row, col + d_col
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                target = new_row * 3 + new_col
                tiles = list(self.tiles)
                tiles[blank], tiles[target] = tiles[target], tiles[blank]
                children.append(State(tuple(tiles), parent=self, action=action, cost=self.cost + 1))

        return children

    def path(self) -> List["State"]:
        states: List["State"] = []
        node: Optional["State"] = self
        while node is not None:
            states.append(node)
            node = node.parent
        states.reverse()
        return states

    def actions(self) -> List[str]:
        return [state.action for state in self.path()[1:]]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")