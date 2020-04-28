import tkinter as tk
import numpy as np

import random
import copy

import levels as lvl

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
            print(f"function {function.__name__}:\t%.{accuracy}f seconds" % timer)
            return value
        return decorated
    return decorator

#################################################################################
#
#   Données de partie

RANDOM_LEVEL = False
GAME_SPEED = 50
NUMBER_SIMULATION = 10000

if RANDOM_LEVEL:
    level = lvl.get_random_level()
else:
    level = lvl.get_classic_level()

GInit  = np.array(level, dtype=np.int8)
GInit  = np.flip(GInit, 0).transpose()

LARGEUR = 13
HAUTEUR = 17

# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille
    
    def copy(self): 
        return copy.deepcopy(self)

GameInit = Game(GInit,3,5)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel    
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L


Window = tk.Tk()
Window.geometry(str(largeurPix)+"x"+str(hauteurPix))   # taille de la fenetre
Window.title("TRON")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = largeurPix, height = hauteurPix, bg ="black" )
canvas.place(x=0,y=0)

#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()
    
    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x,H-y,x+L,H-y-L,fill=coul)
    
    # dessin des murs 
   
    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if Game.Grille[x,y] == 1  : DrawCase(x,y,"gray" )
           if Game.Grille[x,y] == 2  : DrawCase(x,y,"cyan" )
   
    
    # dessin de la moto
    DrawCase(Game.PlayerX,Game.PlayerY,"red" )

def AfficheScore(Game):
   info = "SCORE : " + str(Game.Score)
   canvas.create_text(80, 13,   font='Helvetica 12 bold', fill="yellow", text=info)
   print(f"score:{Game.Score}")


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI

def Moves_available(Game, x, y):
    pos_moves = []
    if Game.Grille[x - 1, y] == 0:
        pos_moves.append((-1, 0))
    if Game.Grille[x + 1, y] == 0:
        pos_moves.append((1, 0))
    if Game.Grille[x, y + 1] == 0:
        pos_moves.append((0, 1))
    if Game.Grille[x, y - 1] == 0:
        pos_moves.append((0, -1))
    return pos_moves



def SimulationPartie(Game):
    move_possible = []
    while True :
        move_possible = Moves_available(Game, Game.PlayerX, Game.PlayerY)
        if len(move_possible) == 0 : #Si plus de coup possible on renvoit le score de la simulation
            return Game.Score
        Game = Play_simulation(Game, move_possible) #Sinon on continue à jouer 


def MonteCarlo(Game, nbParties, study_move):
    Total = 0
    for i in range(0, nbParties):
        Simulation_Game = Game.copy()
        Simulation_Game.PlayerX += study_move[0] # On étudie les simulations à partir d'une position
        Simulation_Game.PlayerY += study_move[1]
        Simulation_Game.Score += 1 #On rajoute 1 car on a deja fait bouger l'IA une fois
        Total += SimulationPartie(Simulation_Game) #On additionne les scores de toutes les simulations
    return Total;

def MonteCarloVect(Game, study_move):
    simulation_game = Game.copy()
    simulation_game.PlayerX += study_move[0]
    simulation_game.PlayerY += study_move[1]
    simulation_game.Score += 1
    return simulate(simulation_game)

def ChooseMov(Game, next_moves):
    score_max = 0
    nbParties = NUMBER_SIMULATION #Nombre de simulation
    best_move = ()
    for move in next_moves : #On parcout tous les movements possibles
        # move_score = MonteCarlo(Game, nbParties, move) #On les étudie un à un
        move_score = MonteCarloVect(Game, move)
        if move_score > score_max : #Si le score est supérieur à celui actuel, alors on a trouvé un meilleur mouvement
            score_max = move_score
            best_move = move
    return best_move


#Modification de la position de l'IA
def Actualise_game(Game, new_pos, x, y):
    x += new_pos[0]
    y += new_pos[1]
    Game.PlayerX = x  # valide le déplacement
    Game.PlayerY = y  # valide le déplacement
    Game.Score += 1
    return Game


@get_time(5)
def Play(Game):   

    x,y = Game.PlayerX, Game.PlayerY
    #print(x,y)

    Game.Grille[x,y] = 2  # laisse la trace de la moto

    next_move = Moves_available(Game, x, y)
    if len(next_move):
        new_pos = ChooseMov(Game, next_move)
        Game = Actualise_game(Game, new_pos, x, y)
        return False  # la partie continue
    else:
        return True


#Identique a Play à la différence qu'on choisit un mouvement au hasard parmis ceux possible
def Play_simulation(Game, move_possible):   

    x,y = Game.PlayerX, Game.PlayerY
    #print(x,y)

    Game.Grille[x,y] = 2  # laisse la trace de la moto


    new_pos = move_possible[random.randrange(len(move_possible))]
    Game = Actualise_game(Game, new_pos, x, y)
    return Game

def simulate(game):
    G = np.tile(game.Grille, (NUMBER_SIMULATION, 1, 1))
    X = np.tile(game.PlayerX, NUMBER_SIMULATION)
    Y = np.tile(game.PlayerY, NUMBER_SIMULATION)
    S = np.tile(game.Score, NUMBER_SIMULATION)
    I = np.arange(NUMBER_SIMULATION)
    dx = np.array([0, -1, 0, 1, 0], dtype=np.int8)
    dy = np.array([0, 0, 1, 0, -1], dtype=np.int8)
    ds = np.array([0, 1, 1, 1, 1], dtype=np.int8)
    old_score = 0
    while True:
        G[I, X, Y] = 2
        available_moves, indexes = load_move_posibilities(G, X, Y, I)
        choices = get_random_choice(available_moves, indexes, I)

        DX = dx[choices]
        DY = dy[choices]
        X += DX
        Y += DY
        S += (choices != 0) * 1

        new_score = np.sum(S)
        if new_score == old_score:
            return new_score
        old_score = new_score

def load_move_posibilities(G, X, Y, I):
    all_posibilities = np.zeros((NUMBER_SIMULATION, 4), dtype=np.uint8)
    indexes = np.zeros(NUMBER_SIMULATION, dtype=np.uint8)
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
    return all_posibilities, indexes

def push_zeros_back(array):
    valid_mask = array != 0
    flipped_mask = valid_mask.sum(1, keepdims=1) > np.arange(array.shape[1] - 1, -1, -1)
    flipped_mask = flipped_mask[:, ::-1]
    array[flipped_mask] = array[valid_mask]
    array[~flipped_mask] = 0
    return array

def get_random_choice(posibilities, indexes, I):
    random_index = np.random.randint(12, size=NUMBER_SIMULATION)
    random_index = random_index % indexes
    return posibilities[I, random_index]

################################################################################
     
CurrentGame = GameInit.copy()
 

def Partie():

    PartieTermine = Play(CurrentGame)
    
    if not PartieTermine :
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(GAME_SPEED, Partie) 
    else :
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()
      

    
        

      
 

