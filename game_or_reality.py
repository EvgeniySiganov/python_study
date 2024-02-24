import tkinter
import random
import time


class TicTacToe(tkinter.Canvas):
    def __init__(self, window):
        super().__init__(window, width=300, height=300)
        self.state = [None, None, None, None, None, None, None, None, None]
        # left button of mouse
        self.bind('<Button-1>', self.click)

    def click(self, event):
        x = int(event.x * 0.01)
        y = int(event.y * 0.01)
        state_mean = x if y == 0 else (3 + x if y == 1 else 6 + x)
        if self.state[state_mean] is None:
            self.state[state_mean] = "x"
        else:
            return
        self.add_x(x, y)
        result = self.get_winner()
        if result is not None:
            self.final_game(result)

        self.bot_move()
        result = self.get_winner()
        if result is not None:
            self.final_game(result)

    def final_game(self, result):
        self.create_text(150, 100, text=result, font=("Helvetica", 28))
        self.state = [None, None, None, None, None, None, None, None, None]
        self.update()
        time.sleep(2.5)
        self.delete("all")
        self.draw_lines()

    def clear_and_redraw(self):
        self.delete("all")
        self.draw_lines()

    def draw_lines(self):
        self.create_line(100, 0, 100, 300, fill='grey')
        self.create_line(200, 0, 200, 300, fill='grey')
        self.create_line(0, 100, 300, 100, fill='grey')
        self.create_line(0, 200, 300, 200, fill='grey')

    def add_x(self, column, row):
        x = column * 100
        y = row * 100
        self.create_line(x, y, x + 100, y + 100, fill='blue', width=3)
        self.create_line(x + 100, y, x, y + 100, fill='blue', width=3)

    # Bot
    def add_o(self, column, row):
        x = column * 100
        y = row * 100
        self.create_oval(x, y, x + 100, y + 100, outline='orange', width=3)

    def bot_move(self):
        list_free = [index for index, value in enumerate(self.state) if value is None]
        random_choose = None
        while len(list_free) > 0:
            random_choose = list_free[random.randint(0, len(list_free) - 1)]
            self.state[random_choose] = "o"
            if self.get_winner() == 'o_win':
                self.move(random_choose)
                break
            else:
                self.state[random_choose] = None
                list_free.remove(random_choose)
        if random_choose:
            self.state[random_choose] = "o"
            self.move(random_choose)

    def move(self, choose):
        if choose < 3:
            self.add_o(choose, 0)
        elif choose < 6:
            self.add_o(choose - 3, 1)
        else:
            self.add_o(choose - 6, 2)

    def get_winner(self):
        conditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        x_win = 0
        o_win = 0
        draw = 0
        for condition in conditions:
            for field in [self.state[i] for i in condition]:
                if field is not None:
                    draw += 1
                    if "x" == field:
                        x_win += 1
                    else:
                        o_win += 1
            if x_win == 3:
                return 'x_win'
            elif o_win == 3:
                return 'o_win'
            else:
                x_win = 0
                o_win = 0
        if draw == 24:
            return 'draw'
        else:
            return None


window = tkinter.Tk()
game = TicTacToe(window)
game.pack()
game.draw_lines()

game.mainloop()
