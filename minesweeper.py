# Python Version 2.7.3
# File: minesweeper.py

import Tkinter as tk
import tkMessageBox
import random
import com
from Tkinter import N, S, E, W
from view import TileFrame, BoardFrame
from model import Tile
from collections import deque

class Minesweeper:
    ROWS = 10
    COLS = 10
    BOMBS = 10

    def __init__(self, master):
        # set up frame
        frame = tk.Frame(master)
        frame.pack(fill=tk.BOTH, expand=True)

        self.data = list()
        self.game_ended = False
        self.clicks = 0

        self.board = BoardFrame(frame)
        self.board.grid(row=0, column=0, sticky=N+S+E+W)
        self.board.set_board((Minesweeper.ROWS, Minesweeper.COLS))
        self.board.grid_propagate(True)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_propagate(True)

        self.set_board()
        self.place_bombs()

        for index in range(Minesweeper.ROWS*Minesweeper.COLS):
            self.board.get_view_at(index).canvas.bind('<Button-1>', self.lclicked_wrapper(index))
            self.board.get_view_at(index).canvas.bind('<Button-3>', self.rclicked_wrapper(index))

        self.update()

    def set_board(self):
        # Initialize board with empty tiles
        for row in range(Minesweeper.ROWS):
            row_list = list()
            for column in range(Minesweeper.COLS):
                row_list.append(Tile(row*Minesweeper.COLS+column))
            self.data.append(row_list)

    def get_covered_tiles(self):
        data = reduce(lambda x,y: x+y, self.data)
        covered_tiles = filter(lambda tile: tile.state == 0, data)
        return covered_tiles

    def place_bombs(self):
        mines = 0
        # Looping while we haven't placed anough bombs.
        while mines < Minesweeper.BOMBS:
            while True:
                # Chosing a random place to place a bomb at.
                bomb_index = random.randint(0, Minesweeper.COLS * Minesweeper.ROWS - 1)
                tile = self.tile_at_index(bomb_index)
                # If the chosen random place is not already a bomb, place a bomb there
                if not tile.is_mine:
                    tile.is_mine = True
                    mines += 1

                    # Setting bomb count for tiles around the placed bomb
                    pos = (bomb_index/Minesweeper.COLS, bomb_index%Minesweeper.COLS)
                    for row in range(max(pos[0]-1, 0), pos[0]+2):
                        for col in range(max(pos[1]-1, 0), pos[1]+2):
                            try:
                                tile = self.data[row][col]
                                tile.nearby_mines += 1
                            except IndexError:
                                continue
                    break

    def amount_open_around(self, index):
        state = self.get_state(index, 1)
        state = reduce(lambda x,y: x+y, state)
        open_tiles_around = filter(lambda tile_value: tile_value >= 0 or tile_value == -2, state)
        return len(open_tiles_around)

    def tile_at_index(self, index):
        return self.data[index/Minesweeper.COLS][index%Minesweeper.COLS]

    def check_for_mines(self, key):
        try:
            if self.tile_at_index(key).is_mine:
                return True
        except KeyError:
            pass

    def update(self):
        for row in range(Minesweeper.ROWS):
            for col in range(Minesweeper.COLS):
                tile_view = self.board.get_view_at((row, col))
                tile_view.set_tile(self.data[row][col])
        global root
        root.update()
        root.update_idletasks()

    def lclicked_wrapper(self, index):
        return lambda x: self.lclicked(index)

    def rclicked_wrapper(self, index):
        return lambda x: self.rclicked(index)

    def lclicked(self, x):
        self.clicks += 1
        tile = self.tile_at_index(x)
        tile_view = self.board.get_view_at(x)
        if tile.is_mine: #if a mine
            self.print_state(x, False)
            tile.exploded = True
            # end game
            self.gameover(False)
            return
        else:
            self.print_state(x, True)
            #change image
            if tile.nearby_mines == 0:
                pos = (x/Minesweeper.COLS, x%Minesweeper.COLS)
                self.clear_empty_tiles(pos)
            # if not already set as clicked, change state and count
            if tile.state != 1:
                tile.state = 1
        self.update()

    def rclicked(self, x):
        self.clicks += 1
        tile = self.tile_at_index(x)
        tile_view = self.board.get_view_at(x)

        # if not clicked
        if tile.state == 0:
            if tile.is_mine:
                #print "Correct flag"
                self.print_state(x, False)
            else:
                # No mine, should left click there
                self.print_state(x, True)
            tile.state = 2
            tile_view.unbind('<Button-1>')
        # if flagged, unflag
        elif tile.state == 2:
            tile.state = 0
            tile_view.bind('<Button-1>', self.lclicked_wrapper(x))
        self.update()

    def get_state(self, x, radius=2):
        tile = self.tile_at_index(x)
        # This function #prints the state of the board surrounding a given cell index
        row = x/10
        col = x%10
        row_range = range(row-radius, row+radius+1)
        col_range = range(col-radius,col+radius+1)

        # If cell is uncovered
        return [[self.get_tile_number(row, col) for col in col_range] for row in row_range]

    def print_state(self, x, good_answer):
        tile = self.tile_at_index(x)
        if tile.state == 0:
            data = self.get_state(x)
            data_file = open('input_data.txt', 'a+')
            data_file.write(str([data, int(good_answer)])+"\n")
            data_file.close()
            # for row in data:
            #     #print row
            # #print "Should click there?", good_answer

    def is_win(self):
        for row in range(Minesweeper.ROWS):
            for col in range(Minesweeper.COLS):
                if self.data[row][col].state == 2 and not self.data[row][col].is_mine:
                    return False
        return True

    def get_tile_number(self, row, column):
        try:
            if row < 0 or column < 0:
                raise IndexError
            tile = self.data[row][column]
            # tile is flagged, ignore mistakes
            if tile.state == 2 and tile.is_mine:
                return -2
            elif tile.state == 0:
                return -1
            else:
                return tile.nearby_mines
        except IndexError:
            return -3

    def check_tile(self, pos, queue):
        try:
            tile = self.data[pos[0]][pos[1]] 
            tile_view = self.board.get_view_at(pos)
            if tile.state == 0:
                if tile.nearby_mines == 0:
                    queue.append(pos)
                tile.state = 1
        except IndexError:
            return

    def clear_empty_tiles(self, pos):
        queue = deque([pos])

        while len(queue) != 0:
            pos = queue.popleft()
            for row in range(max(pos[0]-1, 0), pos[0]+2):
                for col in range(max(pos[1]-1, 0), pos[1]+2):
                    if row == pos[0] and col == pos[1]:
                        continue
                    self.check_tile((row, col), queue)        
    
    def ignore_interaction(self):
        for row in range(Minesweeper.ROWS):
            for col in range(Minesweeper.COLS):
                self.board.get_view_at((row, col)).canvas.unbind('<Button-3>')
                self.board.get_view_at((row, col)).canvas.unbind('<Button-1>')

    def gameover(self, iswin):
        global root
        # print self.clicks
        self.ignore_interaction()
        if not iswin:
            for row in range(Minesweeper.ROWS):
                for col in range(Minesweeper.COLS):
                    tile = self.data[row][col]
                    if tile.state == 0:
                        # Uncover bomb
                        tile.state = 1
        self.update()
        if iswin:
            tkMessageBox.showinfo("Game ended.", "You Won!")
        self.game_ended = True
        root.destroy()

class Solver:
    def __init__(self, minesweeper, addr = "127.0.0.1", port = 8080):
        self.minesweeper = minesweeper
        self.open_tiles = list()
        self.communicator = com.Communicator(addr, port)

    def is_flag_percent(self, tile):
        # Getting data for chosen index.
        data = self.minesweeper.get_state(tile.index)
        data = reduce(lambda x,y: x+y, data)
        # Getting the result, should we click there or no?
        return self.communicator.get_result(data)

    def solve(self):
        global root
        if self.minesweeper.game_ended:
            return

        self.open_tiles = self.minesweeper.get_covered_tiles()
        # If stuck, start a new game
        if len(self.open_tiles) == 0:
            if self.minesweeper.is_win():
                self.minesweeper.gameover(True)
            else:
                self.minesweeper.gameover(False)
            return

        chances = map(self.is_flag_percent, self.open_tiles)
        max_index = chances.index(max(chances)) 
        (max_tile, max_percent) = self.open_tiles[max_index], chances[max_index]
        min_index = chances.index(min(chances))
        (min_tile, min_percent) = self.open_tiles[min_index], chances[min_index]

        played = False
        if min_percent < 0.08 or Minesweeper.COLS * Minesweeper.ROWS - len(self.open_tiles) < 10:
            self.minesweeper.lclicked(min_tile.index)
            played = True
        if max_percent > 0.97:
            self.minesweeper.rclicked(max_tile.index)
            played = True
        
        if not played:
            if abs(0.5-max_percent) > abs(0.5-min_percent):
                self.minesweeper.rclicked(max_tile.index)
            else:
                self.minesweeper.lclicked(min_tile.index)

        root.after(1, self.solve)

### END OF CLASSES ###

def main():
    while True:
        global root
        try:
            # create Tk widget
            root = tk.Tk()
            # set program title
            root.title("Minesweeper")
            # create game instance
            minesweeper = Minesweeper(root)
            root.geometry('500x500+200+200')

            Tile.MINE_IMAGE = tk.PhotoImage(file = "images/mine.gif")
            Tile.FLAG_IMAGE = tk.PhotoImage(file = "images/flag.gif")

            solver = Solver(minesweeper, "127.0.0.1")
            root.after(0, solver.solve)
            # run event loop
            root.mainloop()
        except KeyboardInterrupt:
            print "Shutting down."
            break

if __name__ == "__main__":
    main()