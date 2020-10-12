class Board:
    def __init__(self, row, col, target):
        self.row = row
        self.col = col
        self.target = target
        self.board = []
        self.initialize_board()
        self.number_of_remaining_moves = row * col

    def initialize_board(self):
        for r in range(self.row):
            self.board.append([])
            for c in range(self.col):
                self.board[r].append(' ')

    def is_board_full(self):
        return self.number_of_remaining_moves == 0

    def print_table(self):
        print('-' * (4 * (self.col - 1) + 3))
        for r in range(self.row):
            print(' ', end="")
            for c in range(self.col):
                print(str(self.board[r][c]) + ' ', end="")
                if c == self.col - 1:
                    print(' ')
                else:
                    print('| ', end="")
            print('-' * (4 * (self.col - 1) + 3))

    def is_winning(self, r, c, marker):
        return self.check_column(r, c, marker) or self.check_row(r, c, marker) \
               or self.check_main_diagonal(r, c, marker) or self.check_secondary_diagonal(r, c, marker)

    def check_column(self, r, c, marker):
        number_of_marker = 0

        cur_row = r
        while cur_row >= 0 and self.board[cur_row][c] == marker:
            number_of_marker += 1
            if number_of_marker == self.target:
                return True
            cur_row -= 1

        cur_row = r + 1
        while cur_row < self.row and self.board[cur_row][c] == marker:
            number_of_marker += 1
            if number_of_marker == self.target:
                return True
            cur_row += 1

        return False

    def check_row(self, r, c, marker):
        number_of_marker = 0

        cur_col = c
        while cur_col >= 0 and self.board[r][cur_col] == marker:
            number_of_marker += 1
            if number_of_marker == self.target:
                return True
            cur_col -= 1

        cur_col = c + 1
        while cur_col < self.col and self.board[r][cur_col] == marker:
            number_of_marker += 1
            if number_of_marker == self.target:
                return True
            cur_col += 1

        return False

    def check_main_diagonal(self, r, c, marker):
        number_of_marker = 0

        cur_row = r
        cur_col = c
        while cur_row >= 0 and cur_col >= 0 and self.board[cur_row][cur_col] == marker:
            number_of_marker += 1
            if number_of_marker == self.target:
                return True
            cur_row -= 1
            cur_col -= 1

        cur_row = r + 1
        cur_col = c + 1
        while cur_row < self.row and cur_col < self.col and self.board[cur_row][cur_col] == marker:
            number_of_marker += 1
            if number_of_marker == self.target:
                return True
            cur_row += 1
            cur_col += 1

        return False

    def check_secondary_diagonal(self, r, c, marker):
        number_of_marker = 0

        cur_row = r
        cur_col = c
        while cur_row >= 0 and cur_col < self.col and self.board[cur_row][cur_col] == marker:
            number_of_marker += 1
            if number_of_marker == self.target:
                return True
            cur_row -= 1
            cur_col += 1

        cur_row = r + 1
        cur_col = c - 1
        while cur_row < self.row and cur_col >= 0 and self.board[cur_row][cur_col] == marker:
            number_of_marker += 1
            if number_of_marker == self.target:
                return True
            cur_row += 1
            cur_col -= 1

        return False


class Player:
    def __init__(self, marker, board):
        self.marker = marker
        self.board = board
        self.last_row = -1
        self.last_col = -1
        print("player " + marker + " created")

    def put_marker(self, row, col):
        if self.board.board[row][col] == ' ':
            self.board.board[row][col] = self.marker
            self.last_row = row
            self.last_col = col
            return True
        else:
            return False

    def decrease_remaining_moves(self):
        self.board.number_of_remaining_moves -= 1

    def has_won(self):
        return self.board.is_winning(self.last_row, self.last_col, self.marker)

    def print_winner(self):
        print('Winner is the player with the marker ' + self.marker)

    def move(self):
        pass


class Human_Player(Player):
    def move(self):
        run = True
        while run:
            try:
                user_input = input('Enter b/w 1-' + str(self.board.row * self.board.col) + ' : ')

                user_input = int(user_input) - 1
                if 0 <= user_input < self.board.row * self.board.col:
                    row = int(user_input / self.board.row)
                    col = int(user_input % self.board.col)

                    if self.put_marker(row, col):
                        self.decrease_remaining_moves()
                        run = False
                    else:
                        print('Already entered')
                else:
                    print('Please enter a valid number')
            except:
                print('Enter a number')
        self.board.print_table()


class AI_Player(Player):

    def __init__(self, marker, board):
        super().__init__(marker, board)
        self.available_slots = list(range(board.row * board.col))
        self.available_pointer = 0

    def move(self):

        index = self.find_slot()
        loc = self.available_slots[index]

        row = int(loc / self.board.row)
        col = int(loc % self.board.col)

        if self.put_marker(row, col):
            self.decrease_remaining_moves()
            self.swap(index)
        else:
            self.swap(index)
            self.move()
        self.board.print_table()

    def find_slot(self):
        from random import randrange
        return randrange(self.available_pointer, len(self.available_slots))

    def swap(self, cur_index):
        temp = self.available_slots[cur_index]
        self.available_slots[cur_index] = self.available_slots[self.available_pointer]
        self.available_slots[self.available_pointer] = temp
        self.available_pointer += 1


class TicTacToe:
    def __init__(self, row, col, target):
        self.board = Board(row, col, target)
        self.first_player = Human_Player('X', self.board)
        self.second_player = AI_Player('O', self.board)

    def start(self):
        self.board.print_table()

        while True:

            if not self.board.is_board_full():
                self.first_player.move()
            else:
                print("Stalemate")
                break

            if self.first_player.has_won():
                self.first_player.print_winner()
                break

            if not self.board.is_board_full():
                self.second_player.move()
            else:
                print("Stalemate")
                break

            if self.second_player.has_won():
                self.second_player.print_winner()
                break

if __name__ == "__main__":
    game = TicTacToe(5, 5, 4)
    game.start()
