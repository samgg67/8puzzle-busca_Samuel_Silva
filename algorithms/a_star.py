import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

GOAL_POSITIONS = {tile: divmod(index, 3) for index, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):
    def heuristic(self, state: State) -> int:
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(index, 3)
            goal_row, goal_col = GOAL_POSITIONS[tile]
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        if not initial.is_solvable:
            return SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        tie = count()
        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_g = {initial.tiles: 0}
        explored = set()
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            _, _, node = heapq.heappop(frontier)

            if node.tiles in explored:
                continue

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            explored.add(node.tiles)
            nodes_expanded += 1

            for child in node.neighbors():
                nodes_generated += 1
                if child.tiles in explored:
                    continue
                if child.cost < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = child.cost
                    f = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (f, next(tie), child))

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )