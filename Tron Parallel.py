import time
import numpy as np
import copy
import levels as lvl

RANDOM_LEVEL = False
NUMBER_GAME = 10000
DEBUG = False

import functools
import time

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
            timer *= 1000
            print(f"function {function.__name__}:\t%.{accuracy}f seconds" % timer)
            return value
        return decorated
    return decorator

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
# Si impossible de bouger mettre en sur place

dx = np.array([0, -1, 0, 1, 0], dtype=np.int8)
dy = np.array([0, 0, 1, 0, -1], dtype=np.int8)

# Scores associés à chaque déplacement
ds = np.array([0, 1, 1, 1, 1], dtype=np.int8)

debug = DEBUG
nb = NUMBER_GAME # Nombre de parties

def push_zeros_back(array):
    valid_mask = array != 0
    flipped_mask = valid_mask.sum(1, keepdims=1) > np.arange(array.shape[1] - 1, -1, -1)
    flipped_mask = flipped_mask[:, ::-1]
    array[flipped_mask] = array[valid_mask]
    array[~flipped_mask] = 0
    return array

# @get_time(5)
def load_move_posibilities(G, X, Y, I):
    all_posibilities = np.zeros((nb, 4), dtype=np.uint8)
    indexes = np.zeros(nb, dtype=np.uint8)
    list_of_directions = np.array([
        G[I, X - 1, Y], # Gauche
        G[I, X, Y + 1], # Haut
        G[I, X + 1, Y], # Droite
        G[I, X, Y - 1], # Bas
    ], dtype=np.uint8)
    for i, direction in enumerate(list_of_directions[:]):
        all_posibilities[:, i] = (direction == 0) * (i + 1)
    all_posibilities = push_zeros_back(all_posibilities) # On applique un masque pour decaler les 0
    indexes = np.count_nonzero(all_posibilities, axis=1) # On compte les non null
    indexes[indexes == 0] = 1
    if debug:
        [print(f"{i + 1} :\t{posibility} | {indexes[i]}") for i, posibility in enumerate(all_posibilities)]
    return all_posibilities, indexes

@get_time(5)
def old_load_move_posibilities(G, X, Y, I):
    all_posibilities = np.zeros((nb, 4), dtype=np.uint8)
    indexes = np.zeros(nb, dtype=np.uint8)
    list_of_directions = np.array([
        G[I, X - 1, Y], # Gauche
        G[I, X, Y + 1], # Haut
        G[I, X + 1, Y], # Droite
        G[I, X, Y - 1], # Bas
    ], dtype=np.uint8)
    for i, direction in enumerate(list_of_directions):
        list_of_directions[i] = (direction == 0) * 1
    list_of_directions = list_of_directions.transpose()
    for i in range(nb):
        for j in range(4):
            if list_of_directions[i][j]:
                all_posibilities[i][indexes[i]] = j + 1
                indexes[i] += 1
    indexes[indexes == 0] = 1
    if debug:
        [print(f"{i + 1} :\t{posibility} | {indexes[i]}") for i, posibility in enumerate(all_posibilities)]
    return all_posibilities, indexes


def get_random_choice(posibilities, indexes, I):
    random_index = np.random.randint(12, size=nb)
    random_index = random_index % indexes
    if debug:
        print(f"Indexes :\t{random_index}")
    return posibilities[I, random_index]


def simulate(game):
    # On copie les datas de départ pour créer plusieurs parties en //
    G = np.tile(game.grille, (nb, 1, 1))
    X = np.tile(game.player_x, nb)
    Y = np.tile(game.player_y, nb)
    S = np.tile(game.score, nb)
    I = np.arange(nb)

    old_score = 0

    while True:
        if debug: print(f"X :\t{X}")
        if debug: print(f"Y :\t{Y}")
        if debug: print(f"S :\t{S}")

        # Marque le passage de la moto
        G[I, X, Y] = 2

        available_moves, indexes = load_move_posibilities(G, X, Y, I)
        choices = get_random_choice(available_moves, indexes, I)

        # Deplacement
        DX = dx[choices]
        DY = dy[choices]
        if debug: print(f"DX :\t{DX}")
        if debug: print(f"DY :\t{DY}")
        X += DX
        Y += DY

        # Debug
        if debug: display_grid(G, X, Y)
        if debug: input("Next...")
        if debug: print(f"Moves :\t\t{choices}")

        # Increment du score
        S += (choices != 0) * 1

        # Fin des parties
        new_score = np.sum(S)
        if new_score == old_score:
            print("End of simulation")
            print(f"Min:\t{np.min(S)}\nMax:\t{np.max(S)}\nMoy:\t{np.mean(S)}\n")
            return

        old_score = new_score
        # print("Scores :", np.mean(S))

simulate(game_initial)
