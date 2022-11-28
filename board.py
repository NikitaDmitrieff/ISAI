import numpy as np
import time


class Game:
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k
        self.p1 = set()
        self.p2 = set()
        self.occupied_cells = set()
        self.cells = set([(x, y) for x in range(1, self.m + 1) for y in range(1, self.n + 1)])
        self.possible_victories = (self.get_possible_victories())

    def initialize_game(self):
        return self.m, self.n

    def get_possible_states(self, available_cells, occupied_cells):
        return set(available_cells) - set(occupied_cells)

    def max(self, auto=False, pruned=False):
        bestMove = self.find_best_max_move(pruned)
        print("The Optimal Move is :", bestMove)
        if auto:
            self.p1.add(bestMove)
            self.occupied_cells.add(bestMove)
        else:
            x = int(input('P1, Please input row number'))
            y = int(input('P1, Please input column number'))
            while not self.is_valid((x, y)):
                print('Invalid')
                x = int(input('P1, Please input row number'))
                y = int(input('P1, Please input column number'))
            self.p1.add((x, y))
            self.occupied_cells.add((x, y))

    def min(self, auto=False, pruned=False):
        bestMove = self.find_best_min_move(pruned)
        print("The Optimal Move is :", bestMove)
        if auto:
            self.p2.add(bestMove)
            self.occupied_cells.add(bestMove)
        else:
            x = int(input('P2, Please input row number'))
            y = int(input('P2, Please input column number'))
            while not self.is_valid((x, y)):
                print('Invalid')
                x = int(input('P2, Please input row number'))
                y = int(input('P2, Please input column number'))
            self.p2.add((x, y))
            self.occupied_cells.add((x, y))

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

    def get_possible_victories(self):
        left_diagonal = []
        right_diagonal = []
        rows = []
        columns = []

        to_check = set()
        for cell in self.cells:
            x, y = cell
            if (x == 1) or (y == self.n):
                to_check.add(cell)

        for cell in to_check:
            x, y = cell
            diagonal = [(x, y)]
            while x < self.m and y > 1:
                x += 1
                y -= 1
                diagonal.append((x, y))
            if len(diagonal) == self.k:
                right_diagonal.append(set(diagonal))
            if len(diagonal) > self.k:
                for i in range(len(diagonal) % self.k + 1):
                    right_diagonal.append(set(diagonal[i:self.k + i]))

        to_check = []
        for cell in self.cells:
            x, y = cell
            if (x == 1) or (y == 1):
                to_check.append(cell)

        for cell in to_check:
            x, y = cell
            diagonal = [(x, y)]
            while x < self.m and y < self.n:
                x += 1
                y += 1
                diagonal.append((x, y))
            if len(diagonal) == self.k:
                left_diagonal.append(set(diagonal))
            if len(diagonal) > self.k:
                for i in range(len(diagonal) % self.k + 1):
                    left_diagonal.append(set(diagonal[i:self.k + i]))

        for x in range(self.m):
            row = []
            for y in range(self.n):
                row.append((x + 1, y + 1))
            for i in range(self.n % self.k + 1):
                rows.append(set(row[i:self.k + i]))

        for y in range(self.n):
            column = []
            for x in range(self.m):
                column.append((x + 1, y + 1))
            for i in range(self.m % self.k + 1):
                columns.append(set(column[i:self.k + i]))

        return right_diagonal + left_diagonal + rows + columns

    def get_score(self):
        for each_list in self.possible_victories:
            if len(self.p1.intersection(each_list)) == self.k:
                return 10
            if len(self.p2.intersection(each_list)) == self.k:
                return -10
            else:
                return 0

    def is_terminal(self):
        for each_list in self.possible_victories:
            if len(self.p1.intersection(each_list)) == self.k:
                return 'Player 1 (O) wins', True
            elif len(self.p2.intersection(each_list)) == self.k:
                return 'Player 2 (X) wins', True
            elif len(self.cells) == len(self.occupied_cells):
                return 'It is a draw', True
        return '', False

    def find_best_max_move(self, pruned=False):
        start = time.time()
        if pruned:
            m, bestMove = board.pruned_minimax(True, float('-inf'), float('inf'))
        else:
            m, bestMove = board.minimax(True)
        end = time.time()
        print('Evaluation time: {}s'.format(round(end - start, 7)))
        print('Recommended move:', bestMove)
        return bestMove

    def find_best_min_move(self, pruned=False):
        start = time.time()
        if pruned:
            m, bestMove = board.pruned_minimax(False, float('-inf'), float('inf'))
        else:
            m, bestMove = board.minimax(False)
        end = time.time()
        print('Evaluation time: {}s'.format(round(end - start, 7)))
        print('Recommended move:', bestMove)
        return bestMove

    def minimax(self, is_max):
        score = self.get_score()

        if score == 10:
            return score, 0

        if score == -10:
            return score, 0

        if len(self.get_possible_states(self.cells, self.occupied_cells)) == 0:
            return 0, 0

        if is_max:
            bestScore = float('-inf')
            for state in self.get_possible_states(self.cells, self.occupied_cells):
                self.p1.add(state)
                self.occupied_cells.add(state)
                score, position = self.minimax(not is_max)
                if score > bestScore:
                    bestScore = score
                    bestMove = state
                self.p1.remove(state)
                self.occupied_cells.remove(state)
            return bestScore, bestMove

        else:
            bestScore = float('inf')
            for state in self.get_possible_states(self.cells, self.occupied_cells):
                self.p2.add(state)
                self.occupied_cells.add(state)
                score, position = self.minimax(not is_max)
                if score < bestScore:
                    bestScore = score
                    bestMove = state
                self.p2.remove(state)
                self.occupied_cells.remove(state)
            return bestScore, bestMove

    def pruned_minimax(self, is_max, alpha, beta):
        score = self.get_score()

        if score == 10:
            return score, 0

        if score == -10:
            return score, 0

        if len(self.get_possible_states(self.cells, self.occupied_cells)) == 0:
            return 0, 0

        if is_max:
            bestScore = float('-inf')
            for state in self.get_possible_states(self.cells, self.occupied_cells):
                self.p1.add(state)
                self.occupied_cells.add(state)
                score, position = self.pruned_minimax(not is_max, alpha, beta)
                if score > bestScore:
                    bestScore = score
                    bestMove = state
                self.p1.remove(state)
                self.occupied_cells.remove(state)
                if bestScore >= beta:
                    return bestScore, bestMove
                if bestScore > alpha:
                    alpha = bestScore
            return bestScore, bestMove

        else:
            bestScore = float('inf')
            for state in self.get_possible_states(self.cells, self.occupied_cells):
                self.p2.add(state)
                self.occupied_cells.add(state)
                score, position = self.pruned_minimax(not is_max, alpha, beta)
                if score < bestScore:
                    bestScore = score
                    bestMove = state
                self.p2.remove(state)
                self.occupied_cells.remove(state)
                if bestScore <= alpha:
                    return bestScore, bestMove
                if bestScore < beta:
                    beta = bestScore

            return bestScore, bestMove


if __name__ == '__main__':

    board = Game(3, 3, 3)

    while True:
        board.max(auto=True, pruned=True)
        board.drawboard()
        winner, end = board.is_terminal()
        if end:
            print(winner)
            break
        board.min(auto=True, pruned=True)
        board.drawboard()
        winner, end = board.is_terminal()
        if end:
            print(winner)
            break
