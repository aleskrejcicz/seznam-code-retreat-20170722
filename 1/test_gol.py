from textwrap import dedent
from pytest import skip

class Space:

    def __init__(self):
        self.cells = {}

    def get(self, x, y):
        return self.cells.get((x, y), False)

    def set(self, x, y, value):
        self.cells[(x, y)] = value

    def count_alive_neighbors(self, x, y):
        n = 0
        for xd in [-1, 0, 1]:
            for yd in [-1, 0, 1]:
                if xd == 0 and yd == 0:
                    continue
                n += self.get(x + xd, y + yd)
        return n

    def get_neighbors(self, x, y):
        npos = []
        for xd in [-1, 0, 1]:
            for yd in [-1, 0, 1]:
                if xd == 0 and yd == 0:
                    continue
                npos.append((x + xd, y + yd))
        return npos

    def get_bounds(self):
        min_x, max_x, min_y, max_y = None, None, None, None
        fmin = lambda a, b: b if a is None else min(a, b)
        fmax = lambda a, b: b if a is None else max(a, b)
        for (x, y), value in self.cells.items():
            if value:
                min_x = fmin(min_x, x)
                max_x = fmax(max_x, x)
                min_y = fmin(min_y, y)
                max_y = fmax(max_y, y)
        return min_x, max_x, min_y, max_y

    def dump(self):
        min_x, max_x, min_y, max_y = self.get_bounds()
        if min_x is None:
            return ''
        rows = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                row.append('X' if self.get(x, y) else '.')
            rows.append(''.join(row))
        return ''.join(row + '\n' for row in rows)

    def list_alive_cells(self):
        return sorted(pos for pos, alive in self.cells.items() if alive)

    def should_be_alive(self, x, y):
        alive_before = self.get(x, y)
        n = self.count_alive_neighbors(x, y)
        return self.evaluate_rules(alive_before, n)

    def evaluate_rules(self, alive_before, n):
        # 1, 3
        if alive_before and (n < 2 or n > 3):
            return False
        # 2
        if alive_before and n in [2, 3]:
            return True
        # 4
        if not alive_before and n == 3:
            return True
        return alive_before


def test_evaluate_rule_1():
    space = Space()
    assert space.evaluate_rules(True, 0) == False
    assert space.evaluate_rules(True, 1) == False


def test_evaluate_rule_2():
    space = Space()
    assert space.evaluate_rules(True, 2) == True
    assert space.evaluate_rules(True, 3) == True


def test_evaluate_rule_3():
    space = Space()
    assert space.evaluate_rules(True, 4) == False
    assert space.evaluate_rules(True, 5) == False


def test_evaluate_rule_4():
    space = Space()
    assert space.evaluate_rules(False, 3) == True


def test_enumerate_alive_cells_empty():
    space = Space()
    assert space.list_alive_cells() == []


def test_enumerate_alive_cells():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(0, 1, True)
    assert space.list_alive_cells() == sorted([
        (1, 1), (1, 2), (0, 1),
    ])


def test_space_get_default():
    space = Space()
    assert space.get(1, 1) == False


def test_space_set_and_get():
    space = Space()
    space.set(1, 1, True)
    assert space.get(1, 1) == True


def test_space_count_alive_neighbors():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(0, 1, True)
    assert space.count_alive_neighbors(1, 1) == 2


def test_space_count_alive_neighbors_2():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(0, 1, True)
    assert space.get_neighbors(1, 1) ==  [
        (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]


def test_space_bounds():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(0, 1, True)
    assert space.get_bounds() == (0, 1, 1, 2)


def test_dump():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(0, 1, True)
    assert space.dump() == dedent('''\
        XX
        .X
    ''')


def test_rule_keep_alive():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(0, 1, True)
    assert space.should_be_alive(1, 1) == True
    assert space.should_be_alive(1, 2) == True
    assert space.should_be_alive(0, 1) == True


def test_rule_make_alive():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(0, 1, True)
    assert space.should_be_alive(0, 2) == True



def tick(space):
    space2 = Space()

    def process(x, y):
        if space.should_be_alive(x, y):
            space2.set(x, y, True)

    for x, y in space.list_alive_cells():
        process(x, y)
        for nx, ny in space.get_neighbors(x, y):
            process(nx, ny)

    return space2


def test_tick():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(0, 1, True)
    assert space.dump() == dedent('''\
        XX
        .X
    ''')

    space2 = tick(space)

    assert space2.dump() == dedent('''\
        XX
        XX
    ''')


def test_run_dead():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(3, 1, True)

    for i in range(10):
        print(space.dump())
        space = tick(space)

    assert space.list_alive_cells() == []


def test_run():
    space = Space()
    space.set(1, 1, True)
    space.set(1, 2, True)
    space.set(2, 1, True)
    space.set(3, 1, True)

    for i in range(10):
        print(space.dump())
        space = tick(space)

    assert space.list_alive_cells() == []

    assert 0
