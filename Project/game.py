"""
@author: Kevin Lai 400539423
"""

import pygame as pg
import sys
from random import randint

#Global Variables
WIN_SIZE = 600 # Controls the window size this can be changed and everything else will scale with it
CELL_SIZE = WIN_SIZE//3
INF = float('inf')
VEC2 = pg.math.Vector2
CELL_CENTER = VEC2(CELL_SIZE / 2)
LINE_WIDTH = 6 # This is the line width to make the TicTacToe board
X_COLOR = (255,0,29) 
O_COLOR = (0,8,255)

class TicTacToe:
    def __init__(self, game):
        self.game = game # game object

        # this is a 2D array to simulate the board
        self.game_array = [[INF,INF,INF],
                           [INF,INF,INF],
                           [INF,INF,INF]]

        #randomly pick to see if X or O starts
        self.player = randint(0,1)

        #This array is to hold all the possibliity of a win scenerio
        self.line_win_array = [[(0,0), (0,1), (0,2)],
                               [(1,0), (1,1), (1,2)],
                               [(2,0), (2,1), (2,2)],
                               [(0,0), (1,0), (2,0)],
                               [(0,1), (1,1), (2,1)],
                               [(0,2), (1,2), (2,2)],
                               [(0,0), (1,1), (2,2)],
                               [(0,2), (1,1), (2,0)]]
        self.winner = None
        #if game step reaches 9 then the board is filled and we have a tie game thus restarting the game
        self.game_steps = 0
        
        #font for the label
        self.font = pg.font.SysFont('Arial', CELL_SIZE // 3, True)

        self.file = open('TicTacToe.txt', 'w')

    # function to check for a winner
    def check_winner(self):
        # loop through each of the indexs in the line win array
        for line in self.line_win_array:
        
            #sum up all the elements in the current index to see if it sums to 0 or 3
            sum_line = sum([self.game_array[i][j] for i,j in line])
            
            #if sum is 0 then O is the winner and if sum is 3 then X is the winner
            if sum_line in {0,3}:
                self.winner = 'XO'[sum_line == 0]
                
                #using the center of the cell, we draw a line from the first and 3rd winning cells
                self.winner_line = [VEC2(line[0][::-1]) * CELL_SIZE + CELL_CENTER,
                                    VEC2(line[2][::-1]) * CELL_SIZE + CELL_CENTER]
    #function to run the game
    def run_game(self):
        current_cell = VEC2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int,current_cell)
        left_click = pg.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == INF and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps +=1
            self.check_winner()
            self.file.write("Move#"+ str(self.game_steps) + ": "+ str(self.game_array)+"\n")
            self.file.flush()

    # function to draw for a winner if there is a winner then a yellow line is drawn
    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.game.screen, 'yellow',*self.winner_line, CELL_SIZE//8)
            label = self.font.render(f'Player "{self.winner}" wins!', True, 'white','black')
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() //2, WIN_SIZE // 4))
   
            
    #function to draw the grid of the TicTacToe board            
    def drawBoard(self):
        bg = (71,255,196) # background color of the board
        grid = (50,50,50)
        self.game.screen.fill(bg)
        #loop to draw a 3 x 3 grid
        for i in range(1,3):
            pg.draw.line(self.game.screen,grid,(0,i * CELL_SIZE),(WIN_SIZE, i * CELL_SIZE), LINE_WIDTH)
            pg.draw.line(self.game.screen,grid,(i * CELL_SIZE,0),(i * CELL_SIZE,WIN_SIZE), LINE_WIDTH)

    #function to draw the game objects X and O
    def draw_game_objects(self):
        y_pos = 0
        #loop through the game array to check position of x and y to draw X or O if y == 1 then X is drawn and if y == 0 then O is drawn we use the cell size to draw
        for x in self.game_array:
            x_pos = 0
            for y in x:
                if y == 1:
                    pg.draw.line(self.game.screen, X_COLOR, (x_pos * CELL_SIZE + CELL_SIZE * 0.15, y_pos * CELL_SIZE + CELL_SIZE * 0.15), (x_pos * CELL_SIZE + CELL_SIZE * 0.85, y_pos * CELL_SIZE + CELL_SIZE * 0.85), LINE_WIDTH)
                    pg.draw.line(self.game.screen, X_COLOR, (x_pos * CELL_SIZE + CELL_SIZE * 0.15, y_pos * CELL_SIZE + CELL_SIZE * 0.85), (x_pos * CELL_SIZE + CELL_SIZE * 0.85, y_pos * CELL_SIZE + CELL_SIZE * 0.15), LINE_WIDTH)
                if y == 0:
                    pg.draw.circle(self.game.screen, O_COLOR, (x_pos * CELL_SIZE + CELL_SIZE//2, y_pos * CELL_SIZE + CELL_SIZE//2),CELL_SIZE//3 , LINE_WIDTH)
                x_pos +=1
            y_pos +=1

    #function to draw the board and game objects and draw winning line
    def draw(self):
        self.drawBoard()
        self.draw_game_objects()
        self.draw_winner()

    #function to display captions messages that are dispayed above the game 
    def print_message(self):
        pg.display.set_caption(f'Player "{"OX"[self.player]}"turn!')
        if self.winner:
            pg.display.set_caption(f'Player "{self.winner}" wins! Press Return/Enter Key to Restart')
        elif self.game_steps == 9:
            pg.display.set_caption(f'Game Over! Press Return/Enter Key to Restart')

    #function to print messages draw objects and run the game
    def run(self):
        self.print_message()
        self.draw()
        self.run_game()

#class to simulate a game higher heirachy since TicTacToe is a game and there are others like Hangman and Pacman ect.
class Game:
    def __init__(self):
        #initilize pygame
        pg.init()
        #create a screen size and set mode
        self.screen = pg.display.set_mode([WIN_SIZE]*2)
        #set clock
        self.clock = pg.time.Clock()
        #instantiate a TicTacToe object
        self.ticTacToe = TicTacToe(self)

    #function to start a new game by instantiating a new TicTacToe object
    def new_game(self):
        self.ticTacToe = TicTacToe(self)

    #function to check events to see if user wants to quit or restart a new game
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.ticTacToe.file.close()
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.ticTacToe.file.close()
                    self.new_game()

    #function to run TicTacToe game
    def run(self):
        while True:
            self.ticTacToe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)
#main function that instantiates a game object and invokes the run function
def main():
   game = Game()
   game.run()
    
main()    
        
    