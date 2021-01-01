from tkinter import *


MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9


class SudokuUI(Frame):
    def __init__(self, parent, game):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self, width=500, height=500)
        self.parent = parent
        self.game = game
        self.row, self.col = 0, 0
        self.initUI()

    def initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.__draw_grid()
        self.__draw_puzzle()
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        for i in range(10):
            color = "black" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        for i in range(9):
            for j in range(9):
                answer = self.game.board[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE // 2
                    y = MARGIN + i * SIDE + SIDE // 2
                    original = self.game.board[i][j]
                    color = "black" if answer == original else "red"
                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color, font=("Times New Roman", 17))

    def __cell_clicked(self, event):
        x, y = event.x, event.y
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE
            print(f"row: {row}, col: {col}")
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.board[row][col] == 0:
                self.row, self.col = row, col

        self.__draw_cursor()

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.board[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__end_game()

    def __end_game(self):
        print("You Win!")
        return


class SudokuGame(list):
    def __init__(self, board_file):
        super().__init__()
        self.board = board_file
        self.game_over = False

    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False
        for column in range(9):
            if not self.__check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True

    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.board[row])

    def __check_column(self, column):
        return self.__check_block([self.board[row][column] for row in range(9)])

    def __check_square(self, row, column):
        return self.__check_block([
            self.board[r][c]
            for r in range(row * 3, (row + 1) * 3)
            for c in range(column * 3, (column + 1) * 3)
        ])


if __name__ == '__main__':
    temp_board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    debug_board = [
        [2, 1, 7, 3, 8, 5, 4, 6, 9],
        [3, 8, 5, 4, 6, 9, 7, 1, 2],
        [4, 9, 6, 7, 2, 1, 8, 3, 5],
        [5, 2, 4, 8, 1, 6, 9, 7, 3],
        [6, 3, 9, 5, 4, 7, 2, 8, 1],
        [8, 7, 1, 2, 9, 3, 5, 4, 6],
        [7, 6, 2, 1, 5, 8, 3, 9, 4],
        [9, 5, 3, 6, 7, 4, 1, 2, 8],
        [1, 4, 8, 9, 3, 2, 6, 5, 0]
    ]
    sudoku_game = SudokuGame(debug_board)
    root = Tk()
    app = SudokuUI(root, sudoku_game)
    root.mainloop()
