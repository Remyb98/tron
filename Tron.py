import tkinter as tk
import random
import numpy as np
import copy 

#################################################################################
#
#   Données de partie

Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1] ]

GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

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
    print(pos_moves)

def Move(direction, x, y):
    if direction == "haut":
        y += 1
    if direction == "bas":
        y -= 1
    if direction == "droite":
        x += 1
    if direction == "gauche":
        x -= 1
    return [x, y]

def Play(Game):   

    x,y = Game.PlayerX, Game.PlayerY
    print(x,y)

    Game.Grille[x,y] = 2  # laisse la trace de la moto

    Moves_available(Game, x, y)
    direction = ["haut", "bas", "gauche", "droite"]
    next_move = Move(direction[random.randrange(3)], x, y)
    #y += 1  # on essaye de bouger vers le haut
    x = next_move[0]
    y = next_move[1]
    v = Game.Grille[x,y]
    
    if v > 0 :
        # collision détectée
        return True # partie terminée
    else :
       Game.PlayerX = x  # valide le déplacement
       Game.PlayerY = y  # valide le déplacement
       Game.Score += 1
       return False   # la partie continue
     

################################################################################
     
CurrentGame = GameInit.copy()
 

def Partie():

    PartieTermine = Play(CurrentGame)
    
    if not PartieTermine :
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(1000,Partie) 
    else :
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()
      

    
        

      
 

