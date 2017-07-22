from pytest import skip
from textwrap import dedent


def test_smoke():
    live_cells = {(1, 1)}
    assert (1, 1) in live_cells


def test_tick_zero():
    assert tick(set()) == set()


def test_tick_one():
    assert tick({(1, 1)}) == set()



def test_tick_stable_2x2():
    assert tick({(1, 1), (1, 2), (2, 1), (2, 2)}) == {(1, 1), (1, 2), (2, 1), (2, 2)}


def test_tick_stable_2x2_2():
    assert tick({(1, 1), (1, 2), (2, 1)}) == {(1, 1), (1, 2), (2, 1), (2, 2)}


def test_tick_run():
    cells = {(1, 1), (1, 2), (2, 1), (2, 3)}
    print(dump(cells))
    print()
    assert dump(cells) == dedent('''\
        XX
        X.
        .X''')

    cells = tick(cells)
    print(dump(cells))
    print()
    assert dump(cells) == dedent('''\
        XX
        X.''')

    cells = tick(cells)
    print(dump(cells))
    print()
    assert dump(cells) == dedent('''\
        XX
        XX''')

    cells = tick(cells)
    print(dump(cells))
    print()
    assert dump(cells) == dedent('''\
        XX
        XX''')


def tick(live_cells):
    return {
        (x, y)
        for x, y in expand(live_cells)
        if evaluate_rules(((x, y) in live_cells), count_live_neighbors(live_cells, x, y))
    }


def test_expand():
    assert expand({
        (1, 1)
    }) == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2)
    }


delta_matrix = [(dx, dy) for dx in [0, -1, 1] for dy in [0, -1, 1]]


def expand(positions):
    expanded = set()
    for x, y in positions:
        for dx, dy in delta_matrix:
            expanded.add((x+dx, y+dy))
    return expanded


def test_count_live_neighbors():
    live_cells = {(1, 1), (3, 1), (2, 2), (3, 3)}
    assert count_live_neighbors(live_cells, 2, 2) == 3


def count_live_neighbors(live_cells, x, y):
    return sum(
        1 for cell_x, cell_y in live_cells
        if (x, y) != (cell_x, cell_y) and near(cell_x, x) and near(cell_y, y))


def test_near():
    assert near(1, 2) == True
    assert near(2, 1) == True
    assert near(2, 2) == True
    assert near(1, 3) == False
    assert near(3, 1) == False


def near(a, b):
    return abs(a - b) <= 1


def test_rule_1():
    assert evaluate_rules(True, 0) == False
    assert evaluate_rules(True, 1) == False


def test_rule_2():
    assert evaluate_rules(True, 2) == True
    assert evaluate_rules(True, 3) == True


def test_rule_3():
    assert evaluate_rules(True, 4) == False
    assert evaluate_rules(True, 5) == False


def test_rule_4():
    assert evaluate_rules(False, 0) == False
    assert evaluate_rules(False, 1) == False
    assert evaluate_rules(False, 2) == False
    assert evaluate_rules(False, 3) == True
    assert evaluate_rules(False, 4) == False
    assert evaluate_rules(False, 5) == False


def evaluate_rules(was_live_before, live_neighbors_count):
    if was_live_before:
        return live_neighbors_count in [2, 3]
    else:
        return live_neighbors_count == 3


def test_dump():
    live_cells = {(1, 1), (2, 2)}
    out = dump(live_cells)
    assert out == 'X.\n.X'


def test_dump_3():
    live_cells = {(1, 1), (3, 1), (2, 2), (3, 3)}
    out = dump(live_cells)
    assert out == \
        'X.X\n' \
        '.X.\n' \
        '..X'


def dump(live_cells):
    min_x, max_x, min_y, max_y = get_bounds(live_cells)
    return '\n'.join(''.join(
        'X' if (x, y) in live_cells else '.'
        for x in range(min_x, max_x + 1))
        for y in range(min_y, max_y + 1))


def get_bounds(live_cells):
    if not live_cells:
        return 0, 0, 0, 0
    x_values = [x for x, y in live_cells]
    y_values = [y for x, y in live_cells]
    return min(x_values), max(x_values), min(y_values), max(y_values)


def test_get_bounds():
    live_cells = {(1, 1), (2, 2)}
    min_x, max_x, min_y, max_y = get_bounds(live_cells)
    assert min_x == 1
    assert max_x == 2
    assert min_y == 1
    assert max_y == 2


    #self.self.assertEqual([0, 1, 1], True, 'value ok')
    #assert [0, 1, 1] == True
