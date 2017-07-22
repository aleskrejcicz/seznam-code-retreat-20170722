import pytest

def test_is_live():
    assert is_live({(1, 1)}, 1, 1) == True

def test_exist_any_alive_cells():
    assert exist_any_alive() == True

def exist_any_alive():
    return True

def test_how_many_live_is_around():
    assert how_many_live_is_around({(1, 1)}, 1, 1) == 0

def test_how_many_live_is_around_2():
    assert how_many_live_is_around({(1, 1)}, 2, 1) == 1


def how_many_live_is_around(space, x, y):
    return sum(map(
        lambda dxy: is_live1(space, pos_plus((x, y), dxy)),
        around_offsets()))


def apply_rules(was_live_before, live_around):
    return was_live_before * (live_around in [2, 3]) + \
        (not was_live_before) * (live_around == 3)


def test_apply_rules_live():
    assert apply_rules(True, 0) == False
    assert apply_rules(True, 1) == False
    assert apply_rules(True, 2) == True
    assert apply_rules(True, 3) == True
    assert apply_rules(True, 4) == False
    assert apply_rules(True, 5) == False
    assert apply_rules(True, 6) == False
    assert apply_rules(True, 7) == False
    assert apply_rules(True, 8) == False

def test_apply_rules_dead():
    assert apply_rules(False, 0) == False
    assert apply_rules(False, 1) == False
    assert apply_rules(False, 2) == False
    assert apply_rules(False, 3) == True
    assert apply_rules(False, 4) == False
    assert apply_rules(False, 5) == False
    assert apply_rules(False, 6) == False
    assert apply_rules(False, 7) == False
    assert apply_rules(False, 8) == False


def test_tick():
    cells = {(1, 1), (1, 2), (2, 2)}
    new_cells = tick(cells)
    assert new_cells == {(1, 1), (1, 2), (2, 2), (2, 1)}


def tick(cells):
    return set(filter(
        lambda pos: apply_rules(
            pos in cells,
            how_many_live_is_around(cells, *pos)),
        expand(cells)))


def test_expand():
    assert expand({(1, 1)}) == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    }


def expand(positions):
    return expand_x(expand_y(positions))


def test_expand_x():
    assert expand_x({(0, 1)}) == {(-1, 1), (0, 1), (1, 1)}


def expand_x(positions):
    def f(pos):
        x, y = pos
        yield x-1, y
        yield x, y
        yield x+1, y
    return set().union(*map(f, positions))


def expand_y(positions):
    def f(pos):
        x, y = pos
        yield x, y-1
        yield x, y
        yield x, y+1
    return set().union(*map(f, positions))


def around_offsets():
    yield -1, 0
    yield -1, -1
    yield -1, 1
    yield 0, -1
    yield 0, 1
    yield 1, 0
    yield 1, -1
    yield 1, 1


def pos_plus(a, b):
    ax, ay = a
    bx, by = b
    return (ax+bx, ay+by)


def is_live(live_cells, x, y):
    return (x, y) in live_cells


def is_live1(live_cells, pos):
    x, y = pos
    return (x, y) in live_cells
