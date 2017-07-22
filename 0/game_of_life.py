#!/usr/bin/env python3

from pprint import pprint
from random import random
from time import sleep


def main():
    width = 10
    height = 10
    cells = [[(1 if random() < .5 else 0) for col in range(width)] for row in range(height)]
    while True:
        cells = iterate(cells)
        pprint(cells)
        print()
        sleep(.2)


def iterate(cells):
    cells = enlarge(cells)
    width = len(cells[0])
    height = len(cells)
    new_cells = [[0] * width for row in range(height)]
    for row in range(height):
        for col in range(width):
            n = count_alive_neighbors(cells, row, col)
            new_cells[row][col] = apply_rules(cells[row][col], n)
    new_cells = shrink(new_cells)
    return new_cells


def enlarge(cells):
    width = len(cells[0])
    height = len(cells)
    new_width = width + 2
    new_cells = [
        [0] * new_width,
    ]
    new_cells.extend([0] + cells[row] + [0] for row in range(height))
    new_cells += [
        [0] * new_width,
    ]
    return new_cells


def shrink(cells):
    width = len(cells[0])
    height = len(cells)
    alive_rows = set()
    alive_cols = set()
    for row in range(height):
        for col in range(width):
            if cells[row][col]:
                alive_rows.add(row)
                alive_cols.add(col)
    if not alive_rows:
        return []
    min_row = min(alive_rows)
    max_row = max(alive_rows)
    min_col = min(alive_cols)
    max_col = max(alive_cols)
    return [
        [
            cells[row + min_row][col + min_col]
            for col in range(1 + max_col - min_col)
        ]
        for row in range(1 + max_row - min_row)
    ]


def test_shrink():
    cells = [
        [0, 1, 1],
        [0, 1, 0],
        [1, 0, 0],
    ]
    pprint(cells)
    pprint(shrink(cells))
    assert shrink(cells) == cells


test_shrink()





def count_alive_neighbors(cells, row, col):
    width = len(cells[0])
    height = len(cells)
    n = 0
    offsets = [-1, 0, 1]
    for row_offset in offsets:
        for col_offset in offsets:
            #print(row_offset, col_offset)
            if row_offset == 0 and col_offset == 0:
                continue
            if row_offset < 0 and row == 0:
                continue
            if row_offset > 0 and row == height - 1:
                continue
            if col_offset < 0 and col == 0:
                continue
            if col_offset > 0 and col == width - 1:
                continue
            #print('->', row + row_offset, col + col_offset)
            n += cells[row + row_offset][col + col_offset]
    return  n


def test_count_alive_neighbors():
    cells = [
        [0, 1, 1],
        [0, 1, 0],
        [1, 0, 0],
    ]
    assert count_alive_neighbors(cells, 1, 1) == 3
    assert count_alive_neighbors(cells, 0, 0) == 2
    assert count_alive_neighbors(cells, 2, 2) == 1


test_count_alive_neighbors()


def apply_rules(prev_value, alive_neighbors):
    # 1
    if prev_value and alive_neighbors < 2:
        return 0
    # 2
    if prev_value and alive_neighbors in [2, 3]:
        return 1
    # 3
    if prev_value and alive_neighbors > 3:
        return 0
    # 4
    if not prev_value and alive_neighbors == 3:
        return 1
    return prev_value


if __name__ == '__main__':
    main()
