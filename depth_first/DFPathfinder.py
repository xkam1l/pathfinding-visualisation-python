from queue import LifoQueue

import pygame

import maze_creator.picasso as picasso
import maze_creator.settings as settings
from maze_creator.Creator import Creator
from maze_creator.SquareState import SquareState


class DFPathfinder:
    @staticmethod
    def find_path():
        def _get_valid_neighbours(r: int, c: int):
            """
            Find valid neighbours for a square:
            valid means it's not a wall, has not been visited
            :param r: row
            :param c: column
            :return: valid neighbours
            :rtype: list()
            """

            up_neighbour = (r, c + 1)
            down_neighbour = (r, c - 1)
            left_neighbour = (r - 1, c)
            right_neighbour = (r + 1, c)

            neighbours = [up_neighbour, down_neighbour, left_neighbour, right_neighbour]
            v_neighbours = list()

            for neighbour in neighbours:
                r, c = neighbour
                if r in range(settings.ROWS) and c in range(settings.ROWS):
                    if grid[r][c].state not in [SquareState.VISITED, SquareState.WALL, SquareState.START]:
                        v_neighbours.append(neighbour)

            return v_neighbours

        window = pygame.display.set_mode((800, 800))
        grid = Creator.get_grid()

        finished = False

        start_pos = None
        end_pos = None

        for row in grid:
            for square in row:
                if square.state == SquareState.START:
                    start_pos = square.row, square.col
                elif square.state == SquareState.END:
                    end_pos = square.row, square.col

        print()
        print(f'Starting position: {start_pos}')
        print(f'Ending position: {end_pos}')

        q = LifoQueue()
        q.put([start_pos])

        while not finished:
            moves_so_far = q.get()

            rx, cy = moves_so_far[len(moves_so_far) - 1]
            valid_neighbours = _get_valid_neighbours(rx, cy)

            for vn in valid_neighbours:
                moves_so_far_copy = moves_so_far.copy()
                rvn, cvn = vn
                moves_so_far_copy.append(vn)
                q.put(moves_so_far_copy)
                if (rvn, cvn) == end_pos:
                    final_moves = moves_so_far_copy
                    print()
                    print(f'Path found, took {len(final_moves)} moves')
                    print(f'Moves: {final_moves}')
                    print()
                    finished = True

                    [grid[r][c].change_state(SquareState.PATH) for r, c in final_moves]
                    picasso.draw(window, grid)

                    display_path = True
                    while display_path:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or (
                                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                display_path = False
                    break

                grid[rvn][cvn].change_state(SquareState.VISITED)
            picasso.draw(window, grid)
        pygame.quit()


if __name__ == '__main__':
    DFPathfinder.find_path()
