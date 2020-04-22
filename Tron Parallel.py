import time
import numpy as np

import levels as lvl

RANDOM_LEVEL = 0
NUMBER_GAME = 5

if RANDOM_LEVEL:
    level = lvl.get_random_level()
else:
    level = lvl.get_classic_level()

game_params = np.array(level, dtype=np.int8)
game_params = np.flip(game_params, 0).transpose()

class Game:
    def __init__(self, grille, player_x, player_y, score=0):
        self.player_x = player_x
        self.player_y = player_y
        self.score = score
        self.grille = grille

    def copy(self):
        return copy.deepcopy(self)

game_initial = Game(game_params, 3, 5)

#############################################################
#
#  Affichage en mode texte


def display_grid(G, X, Y):
    game_number, larg, haut = G.shape
    for y in range(haut - 1, -1, -1):
        for i in range(game_number):
            for x in range(larg):
                g = G[i]
                c = ' '
                if G[i, x, y] == 1: c = 'M' # Mur
                if G[i, x, y] == 2: c = 'O' # Trace
                if (X[i], Y[i]) == (x, y): c = 'X' # Joueur
                print(c, sep='', end='')
                print(" ", sep='', end='') # Espace entre les grilles
                print("") # Retour à la ligne


###########################################################
#
# Simulation en parallèle des parties


# Liste des directions :
# 0: sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0, 1, 0], dtype=np.int8)
dy = np.array([0, 0, 1, 0, -1], dtype=np.int8)

# Scores associés à chaque déplacement
ds = np.array([0, 1, 1, 1, 1], dtype=np.int8)

debug = True
nb = NUMBER_GAME # Nombre de parties


def simulate(game):
    # On copie les datas de départ pour créer plusieurs parties en //
    G = np.tile(game.grille, (nb, 1, 1))
    X = np.tile(game.player_x, nb)
    Y = np.tile(game.player_y, nb)
    S = np.tile(game.score, nb)
    I = np.arange(nb)  # 0, 1, 2, 3, 4, 5...
    if debug: display_grid(G, X, Y)

    # VOTRE CODE ICI

    while True:
        if debug: print("X : ", X)
        if debug: print("Y : ", Y)
        if debug: print("S : ", S)

        # Marque le passage de la moto
        G[I, X, Y] = 2

        # Direction : 2 = vers le haut
        choice = np.ones(nb, dtype=np.uint8) * 2

        # DEPLACEMENT
        DX = dx[choice]
        DY = dy[choice]
        if debug: print("DX : ", DX)
        if debug: print("DY : ", DY)
        X += DX
        Y += DY

        # Debug
        if debug: display_grid(G, X, Y)
        if debug: time.sleep(2)

        print("Scores : ", np.mean(S))

simulate(game_initial)
