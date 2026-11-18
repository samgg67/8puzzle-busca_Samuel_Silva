from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        if not initial.is_solvable:
            return SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        frontier = [initial]
        best_depth = {initial.tiles: 0}
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            node = frontier.pop()

            if best_depth.get(node.tiles, node.cost) < node.cost:
                continue

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            if node.cost >= self.depth_limit:
                continue

            nodes_expanded += 1
            for child in reversed(node.neighbors()):
                nodes_generated += 1
                previous = best_depth.get(child.tiles)
                if previous is not None and previous <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                frontier.append(child)

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )