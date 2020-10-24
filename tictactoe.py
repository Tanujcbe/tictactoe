class PlayerEnv:
    def __init__(self, bound):
        self.human = Human('X', bound)
        self.computer = Computer('O', bound)
        self.human_turn = True

    def move(self, board_obj):
        if self.human_turn:
            self.human.make_move(board_obj)
        else:
            self.computer.make_move(board_obj)

    def change_turn(self):
        self.human_turn = not self.human_turn

    def get_last_row(self):
        if self.human_turn:
            return self.human.get_last_row()
        else:
            return self.computer.get_last_row()

    def get_last_col(self):
        if self.human_turn:
            return self.human.get_last_col()
        else:
            return self.computer.get_last_col()

    def print_winner(self):
        if self.human_turn:
            self.human.print_winner()
        else:
            self.computer.print_winner()


class Player:
    def __init__(self, marker, bound):
        self.marker = marker
        self.bound = bound
        self.last_row = -1
        self.last_col = -1
        self.validator = InputValidator
        self.row_col_extractor = RowColExtractor

    def set_last_move(self, row, col):
        self.last_row = row
        self.last_col = col

    def get_last_row(self):
        return self.last_row

    def get_last_col(self):
        return self.last_col

    def print_winner(self):
        print("Player " + self.marker + " has won!")

    def make_move(self, board_obj):
        pass


class InputValidator:
    @staticmethod
    def check_validity(input, bound):
        return 0 < input <= bound


class RowColExtractor:
    @staticmethod
    def get_row(input, col):
        return int((input - 1) / col)

    @staticmethod
    def get_col(input, col):
        return int((input - 1) % col)


class Human(Player):

    def __init__(self, marker, bound):
        super().__init__(marker, bound)
        self.io_handler = IOHandler()

    def make_move(self, board_obj):

        while True:
            user_input = self.io_handler.get_user_input(self.bound)
            if user_input != -1:
                if self.validator.check_validity(user_input, self.bound):
                    cur_row = self.row_col_extractor.get_row(user_input, len(board_obj.board[0]))
                    cur_col = self.row_col_extractor.get_col(user_input, len(board_obj.board[0]))
                    if board_obj.check_empty_cell(cur_row, cur_col):
                        board_obj.put_marker(cur_row, cur_col, self.marker)
                        self.set_last_move(cur_row, cur_col)
                        break
                    else:
                        print("Already entered")
                else:
                    print("Please enter a valid number")
            else:
                print('Please enter a number')


class IOHandler:
    def get_user_input(self, bound):
        try:
            user_input = input('Enter b/w 1-' + str(bound) + ' : ')
            return int(user_input)
        except:
            return -1


class Computer(Player):

    def __init__(self, marker, bound):
        super().__init__(marker, bound)
        self.available_slots = list(range(self.bound))
        self.available_pointer = 0

    def make_move(self, board_obj):

        index = self.find_slot()
        loc = self.available_slots[index]

        cur_row = self.row_col_extractor.get_row(loc, len(board_obj.board[0]))
        cur_col = self.row_col_extractor.get_col(loc, len(board_obj.board[0]))
        self.swap(index)

        if board_obj.check_empty_cell(cur_row, cur_col):
            board_obj.put_marker(cur_row, cur_col, self.marker)
            self.set_last_move(cur_row, cur_col)
        else:
            self.make_move(board_obj)

    def find_slot(self):
        from random import randrange
        return randrange(self.available_pointer, len(self.available_slots))

    def swap(self, cur_index):
        temp = self.available_slots[cur_index]
        self.available_slots[cur_index] = self.available_slots[self.available_pointer]
        self.available_slots[self.available_pointer] = temp
        self.available_pointer += 1


class Board:
    def __init__(self, row, col):
        self.board = []
        self.initialize_board(row, col)
        self.number_of_remaining_moves = row * col

    def initialize_board(self, row, col):
        for r in range(row):
            self.board.append([])
            for c in range(col):
                self.board[r].append(' ')

    def check_empty_cell(self, r, c) -> bool:
        return self.board[r][c] == ' '

    def put_marker(self, r, c, marker):
        self.board[r][c] = marker


class BoardPrinter:
    @staticmethod
    def print(board):
        row = len(board)
        col = len(board[0])
        print('-' * (4 * (col - 1) + 3))
        for r in range(row):
            print(' ', end="")
            for c in range(col):
                print(str(board[r][c]) + ' ', end="")
                if c == col - 1:
                    print(' ')
                else:
                    print('| ', end="")
            print('-' * (4 * (col - 1) + 3))


class WinnerChecker:
    def __init__(self, target: int):
        self.target = target

    def check(self, board: list, row: int, col: int) -> bool:
        def count_consecutive_markers(row_inc: int, col_inc: int) -> int:
            marker = board[row][col]
            number_of_marker = 0
            cur_row = row
            cur_col = col

            while 0 <= cur_row < len(board) and 0 <= cur_col < len(board[0]) and board[cur_row][cur_col] == marker:
                number_of_marker += 1
                cur_row += row_inc
                cur_col += col_inc

            return number_of_marker

        def check_direction(row_dir: int, col_dir: int) -> bool:
            count = count_consecutive_markers(row_dir, col_dir) + count_consecutive_markers(-row_dir, -col_dir) - 1
            return count >= self.target

        return check_direction(1, 0) or check_direction(0, 1) or check_direction(1, 1) or check_direction(1, -1)


class RemainingMoveCtr:
    def __init__(self, num_of_remaining_moves: int):
        self.num_of_remaining_moves = num_of_remaining_moves

    def decrease_num_of_remainig_moves(self):
        self.num_of_remaining_moves -= 1

    def is_num_of_remaining_moves_zero(self):
        return self.num_of_remaining_moves == 0


class GameEnv:
    def __init__(self, row, col, target):
        self.board_obj = Board(row, col)
        self.printer = BoardPrinter()
        self.checker = WinnerChecker(target)
        self.counter = RemainingMoveCtr(row * col)
        self.player_env = PlayerEnv(row * col)

    def print_board(self):
        self.printer.print(self.board_obj.board)

    def decrease_num_of_remaining_moves(self):
        self.counter.decrease_num_of_remainig_moves()

    def check_remaining_moves_is_zero(self):
        return self.counter.is_num_of_remaining_moves_zero()

    def check_state_is_winning(self):
        return self.checker.check(self.board_obj.board, self.player_env.get_last_row(), self.player_env.get_last_col())

    def play(self):
        self.player_env.move(self.board_obj)

    def change_turn(self):
        self.player_env.change_turn()

    def print_winner(self):
        self.player_env.print_winner()


class TicTacToe:
    def __init__(self, row, col, target):
        self.game_env = GameEnv(row, col, target)
        self.game_env.print_board()

    def start(self):

        while not self.game_env.check_remaining_moves_is_zero():
            self.game_env.play()
            self.game_env.print_board()
            if self.game_env.check_state_is_winning():
                self.game_env.print_winner()
                break
            self.game_env.change_turn()
            self.game_env.decrease_num_of_remaining_moves()

        if self.game_env.check_remaining_moves_is_zero():
            print("Stalemate")


def get_row_from_io():
    row = -1
    while row == -1:
        try:
            row = input('Please enter number of rows: ')
        except:
            print('Please enter a number')
    return int(row)


def get_valid_row_from_io():
    row = get_row_from_io()
    while row < 3:
        print('Row number can\'t be lower than 3')
        row = get_row_from_io()
    return row


def get_col_from_io():
    col = -1
    while col == -1:
        try:
            col = input('Please enter number of cols: ')
        except:
            print('Please enter a number')
    return int(col)


def get_valid_col_from_io():
    col = get_col_from_io()
    while col < 3:
        print('Col number can\'t be lower than 3')
        col = get_col_from_io()
    return col


def get_target_from_io():
    target = -1
    while target == -1:
        try:
            target = input(
                'Please enter number of consecutive markers to win(This can\'t be greater than rows and cols): ')
        except:
            print('Please enter a number')
    return int(target)


def get_valid_target_from_io(row, col):
    target = get_target_from_io()
    while target > col or target > row:
        target = get_target_from_io()
    return target


if __name__ == "__main__":
    game_mode = input('Would you like to play traditional TicTacToe game: ')
    while game_mode != 'yes' and game_mode != 'no':
        game_mode = input('Please enter "yes" or "no": ')
    game = None
    if game_mode == 'yes':
        game = TicTacToe(3, 3, 3)
    else:
        row = get_valid_row_from_io()
        col = get_valid_col_from_io()
        target = get_valid_target_from_io(row, col)

        game = TicTacToe(row, col, target)

    game.start()
