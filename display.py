"""Functions for display the game
"""

import tkinter as tk

import global_var as glb


def create_frame(id_frame):
    """Create a new frame and assign an id

    Arguments:
        id_frame {int} -- The id to assign

    Returns:
        Frame -- The frame object
    """
    new_frame = tk.Frame(glb.FRAME)
    glb.FRAME_LIST[id_frame] = new_frame
    new_frame.grid(row=0, column=0, sticky="nsew")
    return new_frame


def display_frame(id_frame):
    """Raise the id widget

    Arguments:
        id_frame {int} -- The frame id
    """
    glb.FRAME_ACTIVE = id_frame
    glb.FRAME_LIST[id_frame].tkraise()


def display_game(game):
    """Draw the game on the canvas

    Arguments:
        game {Game} -- The game
    """
    glb.CANVAS.delete("all")
    height = glb.CANVAS.winfo_height()

    def draw_case(x, y, color):
        x *= glb.CASE_SIZE
        y *= glb.CASE_SIZE
        glb.CANVAS.create_rectangle(
            x,
            height - y,
            x + glb.CASE_SIZE,
            height - y - glb.CASE_SIZE,
            fill=color
        )

    for x in range(glb.WIDTH):
        for y in range(glb.HEIGHT):
            if game.grid[x, y] == 1: # Wall
                draw_case(x, y, "gray")
            elif game.grid[x, y] == 2: # IA #1
                draw_case(x, y, "cyan")
            elif game.grid[x, y] == 3: # IA #2
                draw_case(x, y, "purple")
            elif game.grid[x, y] == -1: # TP
                draw_case(x, y, "green")
    draw_case(game.player1_x, game.player1_y, "red") # Player head
    draw_case(game.player2_x, game.player2_y, "red") # Player head


def display_score(game):
    """Draw the score when the game is over

    Arguments:
        game {Game} -- The game
    """
    info = f"P1:{game.score_player1} P2:{game.score_player2}"
    glb.CANVAS.create_text(80, 13, font='Helvetica 12 bold', fill="yellow", text=info)
    print(info)
