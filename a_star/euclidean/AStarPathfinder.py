from collections import defaultdict
from queue import PriorityQueue
from time import sleep

import pygame

import maze_creator.picasso as picasso
import maze_creator.settings as settings
from maze_creator.Creator import Creator
from maze_creator.SquareState import SquareState


class AStarPathfinder:
    @staticmethod
    def find_path():
        def _get_valid_neighbours(_r: int, _c: int):
            """
            Find valid neighbours for a square:
            valid means it's not a wall, has not been visited
            :param _r: row
            :param _c: column
            :return: valid neighbours
            :rtype: list()
            """

            up_neighbour = (_r, _c + 1)
            down_neighbour = (_r, _c - 1)
            left_neighbour = (_r - 1, _c)
            right_neighbour = (_r + 1, _c)

            neighbours = [up_neighbour, down_neighbour, left_neighbour, right_neighbour]
            v_neighbours = list()

            for neighbour in neighbours:
                _r, _c = neighbour
                if _r in range(settings.ROWS) and _c in range(settings.ROWS):
                    if grid[_r][_c].state not in [SquareState.VISITED, SquareState.WALL, SquareState.START]:
                        v_neighbours.append(neighbour)

            return v_neighbours

        def _get_heuristic(p1: tuple, p2: tuple):
            """
            Get approximate distance to p2 using Euclidean distance
            :param p1: position 1
            :param p2: end position
            :return: approximate distance
            :rtype: int
            """
            return sum((p - q) ** 2 for p, q in zip(p1, p2)) ** .5

        def _reconstruct_path(_r, _c):
            rr, cc = _r, _c
            moves = list()

            while True:
                try:
                    rr, cc = came_from[rr][cc].get_pos()
                    moves.append((rr, cc))
                except:
                    moves.reverse()
                    return moves

        window = pygame.display.set_mode((800, 800))
        grid = Creator.get_grid()
        if not grid:
            return

        pq = PriorityQueue()

        end_pos = None
        start_pos = None
        start_row, start_col = None, None

        for row in grid:
            for square in row:
                if square.state == SquareState.START:
                    start_pos = square.row, square.col
                    start_row, start_col = start_pos
                elif square.state == SquareState.END:
                    end_pos = square.row, square.col
        print()
        print(f'Starting position: {start_pos}')
        print(f'Ending position: {end_pos}')
        print()

        came_from = defaultdict(dict)

        g_score = defaultdict(dict)
        f_score = defaultdict(dict)

        for rq in grid:
            for cq in rq:
                r, c = cq.get_pos()
                g_score[r][c] = float("inf")
                f_score[r][c] = float("inf")

        g_score[start_row][start_col] = 0
        f_score[start_row][start_col] = _get_heuristic(start_pos, end_pos)

        pq.put((f_score[start_row][start_col], grid[start_row][start_col]))

        finished = False
        while not finished:
            current = pq.get()
            current_square = current[1]
            current_row, current_col = current_square.get_pos()

            for n in _get_valid_neighbours(*current_square.get_pos()):
                n_row, n_col = n
                te_g_score = g_score[current_row][current_col] + 1

                grid[n_row][n_col].change_state(SquareState.PATH)
                if (n_row, n_col) == end_pos:
                    finished = True

                    grid[n_row][n_col].change_state(SquareState.PATH)
                    display_path = True

                    final_moves = _reconstruct_path(current_row, current_col)
                    final_moves.append((current_row, current_col))
                    final_moves.append((n_row, n_col))

                    print(f'Path found, took {len(final_moves)} moves')
                    print(f'Moves: {final_moves}')
                    print()

                    for r, c in final_moves:
                        grid[r][c].change_state(SquareState.PATH)
                        picasso.draw(window, grid)
                        sleep(0.1)

                    while display_path:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                if event.type == pygame.QUIT or (
                                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                    display_path = False
                                    break

                if te_g_score < g_score[n_row][n_col]:
                    came_from[n_row][n_col] = current_square
                    g_score[n_row][n_col] = te_g_score
                    f_score[n_row][n_col] = g_score[n_row][n_col] + _get_heuristic((n_row, n_col), end_pos)

                if (f_score[n_row][n_col], grid[n_row][n_col]) not in pq.queue:
                    pq.put((f_score[n_row][n_col], grid[n_row][n_col]))

                grid[n_row][n_col].change_state(SquareState.VISITED)
            picasso.draw(window, grid)
        pygame.quit()


if __name__ == '__main__':
    AStarPathfinder.find_path()
