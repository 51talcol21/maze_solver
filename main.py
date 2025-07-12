import numpy as np
import time
import tracemalloc
import re
from collections import deque
import copy
import heapq
import sys

BOARD_DIRECTIONS = {
    'UP':    (-1, 0),
    'DOWN':  (1, 0),
    'LEFT':  (0, -1),
    'RIGHT': (0, 1),
}

class Maze(object):
    def __init__(self, board: list[list[int]], board_dimensions: tuple[int, int], 
        start_position: tuple[int,int],
        goal_position: tuple[int, int]):
        """
        Initializes maze object

        Parameters:
            board: Board for the maze, 2d list.
            board_dimensions: Dimensions of the board in tuple worm (3,2) is a 3 by 2 board.
            cost: Current path cost.
            parent: Parent Maze move. I.E. if this board represents a move down from the parent board, we store the parent.
            action: Movement (up, down, left, right).
        """
        self.board = board
        self.start_position = start_position
        self.goal_position = goal_position
        self.board_dimensions = board_dimensions

        # Ensure board meets dimensions
        if (np.shape(board) != board_dimensions):
            raise Exception("Board does not meet the dimensions.")
        if (not self.check_for_exits()):
            raise Exception("Board is not escapable.")

    def check_for_exits(self, tile_escape: int = 0) -> bool:
        """
        Checks to make sure at least two exits/entrances exists.
        Does not check for path.

        Parameters:
            tile_escape: The tile that represents exits/entrances (0)

        Returns:
            boolean: If two or more exits exist
        """
        exit_counter: int = 0
        for each_row in self.board:
            for each_tile in each_row:
                if each_tile == tile_escape:
                    exit_counter += 1
        return exit_counter >= 2

    def is_valid_tile(self, possible_position: tuple[int,int]):
        return (0 <= possible_position[0] < self.board_dimensions[0] and
                0 <= possible_position[1] < self.board_dimensions[1] and
                self.board[possible_position[0]][possible_position[1]] != 9
            )

class AStarSolver:
    def __init__(self, board: Maze):
        self.board = board
        self.start_position = board.start_position
        self.goal_position = board.goal_position

    def heuristic(self, start_pos, end_pos):
        """
        Calculates the Manhattan distance for our heuristic. 
        Manhattan distance just being the direct distance between cartesian coordinates, rather than "as the crow flies"/Euclidean
        
        Parameters:
            start_pos: Start position
            end_pos: End position
        """
        return abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])

    def solve(self):
        """
        Dijkstra's Algorith with the above manhattan heuristic.

        Returns:
            If path is found:
                path: Path to get there
                moves: Each move down (I.E. UP DOWN LEFT RIGHT RIGHT RIGHT)
                nodes_explored: Number of nodes explored
        """
        start = self.start_position
        goal = self.goal_position

        open_set = []
        heapq.heappush(open_set, (0 + self.heuristic(start, goal), 0, start, [start], []))
        visited = {}
        nodes_explored = 0

        while open_set:
            f, g, pos, path, moves = heapq.heappop(open_set)

            nodes_explored += 1

            if pos == goal:
                return path, moves, nodes_explored

            if pos in visited and visited[pos] <= g:
                continue
            visited[pos] = g

            for direction, (dr, dc) in BOARD_DIRECTIONS.items():
                nr, nc = pos[0] + dr, pos[1] + dc
                neighbor = (nr, nc)

                if not self.board.is_valid_tile(neighbor):
                    continue

                new_g = g + 1
                h = self.heuristic(neighbor, goal)
                heapq.heappush(open_set, (new_g + h, new_g, neighbor, path + [neighbor], moves + [direction]))

        return None, None


def display_board(board: Maze, current_position: tuple[int,int]):
    """
    Displays the board with letters for readability.
    Parameters:
        Board: The board to be passed.
        current_position: Where our 'player' currently is.
    """
    display_board = copy.copy(board)
    display_board.board[display_board.start_position[0]][display_board.start_position[1]] = "S"
    display_board.board[display_board.goal_position[0]][display_board.goal_position[1]] = "E"
    display_board.board[current_position[0]][current_position[1]] = "X"
    for each_row_index, each_row in enumerate(display_board.board):
        for each_tile_index, each_tile in enumerate(each_row):
            if each_tile == 1:
                display_board.board[each_row_index][each_tile_index] = "P"
            if each_tile == 9:
                display_board.board[each_row_index][each_tile_index] = "W"
        print(each_row)

def bfs(board: Maze):
    """
    Solve by doing Breadth First Search

    Parameters:
        board: Our board to solve

    returns:
        [path, moves, and number of nodes explored]
    """
    start = board.start_position
    goal = board.goal_position

    # Keep track of our visited paths so we don't backtrck
    visited = set()
    
    queue = deque()
    queue.append((start, [start], []))  # (position, path_so_far, moves_so_far)
    nodes_explored = 0
    visited.add(start)

    while queue:
        pos, path, moves = queue.popleft()
        nodes_explored += 1

        if pos == goal:
            return path, moves, nodes_explored

        for direction, (dr, dc) in BOARD_DIRECTIONS.items():
            new_r, new_c = pos[0] + dr, pos[1] + dc
            next_pos = (new_r, new_c)
            if board.is_valid_tile(next_pos) and next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos], moves + [direction]))

    return None, None

def dfs(board: Maze):
    """
    Solve by doing Depth First Search

    Parameters:
        board: well, the board

    returns:
        [path, moves, and number of nodes explored]
    """
    start = board.start_position
    goal = board.goal_position

    # Init our stack with start position, the path so far (just the start position), and directions (blank obviously)
    stack = [(start, [start], [])]
    nodes_explored = 0
    visited = set()

    while stack:
        pos, path, moves = stack.pop()
        nodes_explored += 1

        # Base Case, curr position is where we want to be, the goal.
        if pos == goal:
            return path, moves, nodes_explored

        if pos in visited:
            continue
        visited.add(pos)

        for direction, (dr, dc) in BOARD_DIRECTIONS.items():
            new_r, new_c = pos[0] + dr, pos[1] + dc
            next_pos = (new_r, new_c)

            if board.is_valid_tile(next_pos) and next_pos not in visited:
                stack.append((next_pos, path + [next_pos], moves + [direction]))

    return None  # No path found

def benchmark(solver_name, solver_func, *args, **kwargs):
    import time
    import tracemalloc

    tracemalloc.start()
    start_time = time.time()

    result = solver_func(*args, **kwargs)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        'name': solver_name,
        'time': end_time - start_time,
        'memory_kb': peak / 1024,
        'nodes_explored': result[2],
        'path': result[1] if result[1] else "No path found.",
        'path_length': len(result[1]) if result[1] else 0,
        'found_path': result[1] is not None,
    }

def text_file_to_2d_array(filename: str) -> list[list[int]]:
    """
    Opens our input file and converts it to a maze, also reads in start and end position.
    Expected format is like this: `
        start(0,0)
        end(0,6)
        0 9 9 9 9 9 0
        1 1 1 1 1 9 1
        1 9 9 9 1 9 1
        1 9 9 1 1 9 1
        1 1 1 1 1 1 1
    `

    Parameters:
        filename: File path to the file.

    Returns:
        list: A 2D array representing the data from the file.
    """
    data_2d_array = []
    try:
        with open(filename, 'r') as file:
            start_line = file.readline().strip()
            end_line = file.readline().strip()

            start_match = re.match(r'start\((\d+),\s*(\d+)\)', start_line)
            end_match = re.match(r'end\((\d+),\s*(\d+)\)', end_line)

            if not start_match or not end_match:
                raise ValueError("Start or end line is not in the expected format: start(x,y), end(x,y)")

            start_coord = (int(start_match.group(1)), int(start_match.group(2)))
            end_coord = (int(end_match.group(1)), int(end_match.group(2)))

            for line in file:
                elements = line.strip().split()

                row = [int(e) for e in elements]

                data_2d_array.append(row)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except ValueError:
        print("Error: Could not convert data to the expected type (e.g., integer).")
    return start_coord, end_coord, data_2d_array

def main():
    file_input = sys.argv[1]
    input_information = text_file_to_2d_array(file_input)

    start_pos   = input_information[0]
    end_pos     = input_information[1]
    board       = input_information[2]

    full_board = Maze(board, np.shape(board), start_pos, end_pos)
    solver = AStarSolver(full_board)

    with open('output.txt', 'w') as f:
        for solver_func, solver_name in [
            (lambda: bfs(full_board), "BFS"),
            (lambda: dfs(full_board), "DFS"),
            (lambda: solver.solve(), "A*"),
        ]:
            stats = benchmark(solver_name, solver_func)
            f.write(f"Solver: {stats['name']}\n")
            f.write(f"  Found path: {stats['found_path']}\n")
            f.write(f"  Path length: {stats['path_length']}\n")
            f.write(f"  Nodes explored: {stats['nodes_explored']}\n")
            f.write(f"  Time taken: {stats['time']:.6f} seconds\n")
            f.write(f"  Peak memory usage: {stats['memory_kb']:.2f} KB\n")
            f.write(f"  Path taken: {stats['path']}\n")
            f.write('\n')

if __name__ == '__main__':
    main()
