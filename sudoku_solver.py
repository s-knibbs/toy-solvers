import sys
from functools import partial


# Toy sudoku solver that can solve most easy to medium puzzle

class Grid(object):

    def __init__(self, initial):
        self.solution = initial
        self.locations = [set(range(1,10)) for _ in range(9*9)]

    @staticmethod
    def _colIdxs(idx):
        col = idx % 9
        return set([col + i*9 for i in range(9)])

    @staticmethod
    def _rowIdxs(idx):
        row = idx // 9
        return set([i + row*9 for i in range(9)])

    @staticmethod
    def _sectorIdxs(idx):
        sector_start_col = ((idx % 9) // 3) * 3
        sector_start_row = ((idx // 9) // 3) * 3
        idxs = [i + sector_start_col + 9 * sector_start_row for i in range(3)]
        idxs.extend([i + sector_start_col + 9*(sector_start_row + 1) for i in range(3)])
        idxs.extend([i + sector_start_col + 9*(sector_start_row + 2) for i in range(3)])
        return set(idxs)

    def _updateIdxs(self, idxs, value):
        solved = []
        for idx in idxs:
            cell_set = self.locations[idx]
            if value in cell_set:
                cell_set.remove(value)
            if len(cell_set) == 1:
                val = cell_set.pop()
                solved.append((idx, val))
        return solved

    def _validIdx(self, value, idx):
        return value in self.locations[idx]

    def _checkSector(self, idx, value):
        idxs = {x for x in self._sectorIdxs(idx) if self._validIdx(value, x)}
        rows = {x // 9 for x in idxs}
        cols = {x % 9 for x in idxs}
        if len(idxs) == 1:
            return [(idx, value)]
        #if len(rows) == 1:
        #    return self._updateIdxs(self._rowIdxs(idx) - self._sectorIdxs(idx), value)
        #if len(cols) == 1:
        #    return self._updateIdxs(self._colIdxs(idx) - self._sectorIdxs(idx), value)
        return []

    def initialSolved(self):
        solved = []
        for idx, value in enumerate(self.solution):
            if value != 0:
                solved.append((idx, value))
        return solved, (9*9 - len(solved))

    def solve(self, solved, count):
        if len(solved) == 0:
            return count
        next_solved = []
        for idx, value in solved:
            self.solution[idx] = value
            self.locations[idx].clear()
            idxs = self._colIdxs(idx) | self._rowIdxs(idx) | self._sectorIdxs(idx)
            next_solved.extend(self._updateIdxs(idxs, value))
        if len(next_solved) == 0:
            for idx, cell_set in enumerate(self.locations):
               for value in cell_set:
                    validIdx = partial(self._validIdx, value)
                    if len([x for x in self._colIdxs(idx) if validIdx(x)]) == 1:
                        next_solved.append((idx, value))
                        continue
                    if len([x for x in self._rowIdxs(idx) if validIdx(x)])  == 1:
                        next_solved.append((idx, value))
                        continue
                    next_solved.extend(self._checkSector(idx, value))
        return self.solve(next_solved, count - len(next_solved))

    def __str__(self):
        solution_str = ""
        for idx, value in enumerate(self.solution):
            solution_str += str(value) + " "
            solution_str += "\n" if idx % 9 == 8 else " "
        return solution_str


def readProblems(filename):
    problems = []
    problem = []
    with open(filename, 'r') as problem_file:
        for row in problem_file:
            row = row.strip()
            if row.startswith("Grid"):
                problem = []
                continue
            problem.extend([int(value) for value in row])
            if len(problem) == 9*9:
                problems.append(problem)
    return problems


if __name__ == "__main__":
    problems = readProblems(sys.argv[1])
    solved_count = 0
    for problem in problems:
        grid = Grid(problem)
        solved, count = grid.initialSolved()
        new_count = grid.solve(solved, count)
        print(grid)
        print("%s : %s" % (count, new_count))
        if new_count <= 0:
            solved_count += 1
    print("Solved %s out of %s" % (solved_count, len(problems)))