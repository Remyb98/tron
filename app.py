#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""Tron game"""
import copy
import functools
import time

import tkinter as tk
import numpy as np

import global_var as glb
import display as dsp
import levels as lvl
import ia


class Game:
    """Game object with his parameters
    """
    def __init__(self, grid, player1_x, player1_y, player2_x, player2_y, score_player1=0, score_player2=0):
        """Game constructor

        Arguments:
            grid {np.array[][]} -- The level
            player1_x {int} -- Player x position
            player1_y {int} -- Player y position

        Keyword Arguments:
            score {number} -- The current score (default: {0})
        """
        self.player1_x = player1_x
        self.player1_y = player1_y
        self.player2_x = player2_x
        self.player2_y = player2_y
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.grid = grid

    def copy(self):
        """Return a copy of the object

        Returns:
            Game -- The game copied
        """
        return copy.deepcopy(self)


def get_time(accuracy=10):
    """Decorateur pour connaitre le temps d execution
    d une fonction
    """
    def decorator(function):
        @functools.wraps(function)
        def decorated(*args, **kwargs):
            start = time.time()
            value = function(*args, **kwargs)
            timer = time.time() - start
            print(f"function {function.__name__}:\t%.{accuracy}f seconds" % timer)
            return value
        return decorated
    return decorator


def moves_available(game, x, y):
    """Get all moves available for the game configuration

    Arguments:
        game {Game} -- The game
        x {int} -- The current x position
        y {int} -- The current y position

    Returns:
        list -- List of moves available
    """
    pos_moves = []
    if game.grid[x - 1, y] <= 0:
        pos_moves.append((-1, 0))
    if game.grid[x + 1, y] <= 0:
        pos_moves.append((1, 0))
    if game.grid[x, y + 1] <= 0:
        pos_moves.append((0, 1))
    if game.grid[x, y - 1] <= 0:
        pos_moves.append((0, -1))
    return pos_moves


def move_player(game, new_position, player):
    """Move the player in the level

    Arguments:
        game {Game} -- The game
        new_position {list} -- The new position
        x {int} -- The current x position
        y {int} -- The current y position

    Returns:
        Game -- The game
    """
    if player == 1:
        game.player1_x += new_position[0]
        game.player1_y += new_position[1]
        game.score_player1 += 1
    elif player == 2:
        game.player2_x += new_position[0]
        game.player2_y += new_position[1]
        game.score_player2 += 1
    return game


def teleport_player(game, player):
    """Teleport the player in the other place

    Arguments:
        game {Game} -- The game
    """
    if player == 1:
        game.grid[game.player1_x, game.player1_y] = 2 # TP trigger
        index_tp = np.where(game.grid == -1)
        game.player1_x = index_tp[0][0]
        game.player1_y = index_tp[1][0]
    elif player == 2:
        game.grid[game.player2_x, game.player2_y] = 3 # TP trigger
        index_tp = np.where(game.grid == -1)
        game.player2_x = index_tp[0][0]
        game.player2_y = index_tp[1][0]


# @get_time(5)
def play(game):
    """Move the IA

    Arguments:
        game {Game} -- The game

    Returns:
        bool -- If the game is over
    """
    no_more_moves = True
    if game.grid[game.player1_x, game.player1_y] == -1:
        teleport_player(game, 1)
    if game.grid[game.player2_x, game.player2_y] == -1:
        teleport_player(game, 2)
    x1, y1 = game.player1_x, game.player1_y
    x2, y2 = game.player2_x, game.player2_y

    next_move_first = moves_available(game, x1, y1)
    if len(next_move_first) != 0:
        new_position = ia.choose_mov(game, next_move_first, 1)
        game = move_player(game, new_position, 1)
        no_more_moves = False
        game.grid[x1, y1] = 2  # Laisse la trace de la moto

    next_move_second = moves_available(game, x2, y2)
    if len(next_move_second) != 0:
        new_position = ia.choose_mov(game, next_move_second, 2)
        game = move_player(game, new_position, 2)
        no_more_moves = False
        game.grid[x2, y2] = 3  # Laisse la trace de la moto
    return no_more_moves


def partie():
    """Mainloop of the game
    """
    partie_termine = play(CURRENT_GAME)
    if not partie_termine:
        dsp.display_game(CURRENT_GAME)
        WINDOW.after(glb.GAME_SPEED, partie)
    else:
        dsp.display_score(CURRENT_GAME)


def generate_level():
    """Load the level

    Returns:
        np.array[][] -- The level
    """
    if glb.RANDOM_LEVEL:
        level = lvl.get_random_level()
    else:
        level = lvl.get_classic_level()
    return level


if __name__ == '__main__':
    G_INIT = np.array(generate_level(), dtype=np.int8)
    G_INIT = np.flip(G_INIT, 0).transpose()
    GAME_INIT = Game(G_INIT, 3, 5, 10, 10)
    CURRENT_GAME = GAME_INIT.copy()

    P_WIDTH = glb.WIDTH * glb.CASE_SIZE
    P_HEIGHT = glb.HEIGHT * glb.CASE_SIZE

    WINDOW = tk.Tk()
    WINDOW.geometry(f"{P_WIDTH}x{P_HEIGHT}")
    WINDOW.title("TRON")

    glb.FRAME = tk.Frame(WINDOW)
    glb.FRAME.pack(side="top", fill="both", expand=True)
    glb.FRAME.grid_rowconfigure(0, weight=1)
    glb.FRAME.grid_columnconfigure(0, weight=1)

    glb.CANVAS = tk.Canvas(dsp.create_frame(0), width=P_WIDTH, height=P_HEIGHT, bg="black")
    glb.CANVAS.place(x=0, y=0)

    dsp.display_frame(0)
    WINDOW.after(100, partie)
    WINDOW.mainloop()
