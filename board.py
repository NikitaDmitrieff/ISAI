import numpy as np


class Game:
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.p1 = []
        self.p2 = []
        self.k = k
        self.occupied_cells = []

    def initialize_game(self):
        return self.m, self.n

    def max(self):
        x = int(input('P1, Please input row number'))
        y = int(input('P1, Please input column number'))
        while not self.is_valid((x,y)):
            print('Invalid')
            x = int(input('P1, Please input row number'))
            y = int(input('P1, Please input column number'))
        self.p1.append((x,y))
        self.occupied_cells.append((x, y))

    def min(self):
        x = int(input('P2, Please input row number'))
        y = int(input('P2, Please input column number'))
        while not self.is_valid((x,y)):
            print('Invalid')
            x = int(input('P2, Please input row number'))
            y = int(input('P2, Please input column number'))
        self.p2.append((x,y))
        self.occupied_cells.append((x, y))


    def drawboard(self):
        x_dim, y_dim = self.initialize_game()
        matrix = np.full((x_dim * y_dim), [' '], dtype=str).reshape(self.initialize_game())

        for pos in self.p1:
            x, y = pos
            new_pos = (x - 1, y - 1)
            matrix[new_pos] = 'O'

        for pos in self.p2:
            x, y = pos
            new_pos = (x - 1, y - 1)
            matrix[new_pos] = 'X'

        lines = [' ' + '-' * (y_dim * 4 + 1)]
        for x in matrix:
            number = []
            for idx, y in enumerate(x):
                number.append(str(y))

            each_lines = " | " + " | ".join(number) + " | "
            lines.append(each_lines)

            lines.append(' ' + '-' * (len(x) * 4 + 1))

        return print("\n".join(lines))

    def is_valid(self, cell):
        cells = [(x, y) for x in range(1, self.m + 1) for y in range(1, self.n + 1)]
        if (cell in cells) and (cell not in self.occupied_cells):
            return True
        return False

    def is_terminal(self):
        cells = [(x, y) for x in range(1, self.m + 1) for y in range(1, self.n + 1)]
        left_diag = []
        right_diag = []
        rows = []
        columns = []

        to_check = []
        for cell in cells:
            x, y = cell
            if (x == 1) or (y == self.n):
                to_check.append(cell)

        for cell in to_check:
            x, y = cell
            diag = [(x, y)]
            while x < self.m and y > 1:
                x += 1
                y -= 1
                diag.append((x, y))
            right_diag.append(diag)

        to_check = []
        for cell in cells:
            x, y = cell
            if (x == 1) or (y == 1):
                to_check.append(cell)

        for cell in to_check:
            x, y = cell
            diag = [(x, y)]
            while x < self.m and y < self.m:
                x += 1
                y += 1
                diag.append((x, y))
            left_diag.append(diag)

        for x in range(self.m):
            row = []
            for y in range(self.n):
                row.append((x + 1, y + 1))
            rows.append(row)

        for y in range(self.n):
            column = []
            for x in range(self.m):
                column.append((x + 1, y + 1))
            columns.append(column)

        total = right_diag + left_diag + rows + columns

        for each_list in total:
            if len(set(self.p1).intersection(set(each_list))) == self.k:
                return True
            if len(set(self.p2).intersection(set(each_list))) == self.k:
                return True
        return False

if __name__ == '__main__':

    board = Game(3, 3, 3)

    while not board.is_terminal():
        board.max()
        board.drawboard()
        if board.is_terminal():
            break
        board.min()
        board.drawboard()

