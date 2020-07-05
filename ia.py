"""IA stuff for the game
"""

import numpy as np

import global_var as glb


def monte_carlo_vect(game, study_move, player):
    """Monte Carlo evaluation

    Arguments:
        game {Game} -- The game
        study_move {list} -- The move to try

    Returns:
        int -- The score of the simulation
    """
    simulation_game = game.copy()
    if player == 1:
        simulation_game.player1_x += study_move[0]
        simulation_game.player1_y += study_move[1]
        player_x = simulation_game.player1_x
        player_y = simulation_game.player1_y
        simulation_game.score_player1 += 1
    elif player == 2:
        simulation_game.player2_x += study_move[0]
        simulation_game.player2_y += study_move[1]
        player_x = simulation_game.player2_x
        player_y = simulation_game.player2_y
        simulation_game.score_player2 += 1
    return simulate(simulation_game, player_x, player_y, player)


def choose_mov(game, next_moves, player):
    """Choose the best move

    Arguments:
        game {Game} -- The game
        next_moves {list} -- List of moves available

    Returns:
        list -- The best move available
    """
    score_max = 0
    for move in next_moves: # On parcout tous les movements possibles
        move_score = monte_carlo_vect(game, move, player)
        if move_score > score_max:
            score_max = move_score
            best_move = move
    return best_move


def simulate(game, x, y, player):
    """Create a simulation of the current game

    Arguments:
        game {Game} -- The game to simulate

    Returns:
        int -- The score
    """
    if player == 1:
        base_score = game.score_player1
    elif player == 2:
        base_score = game.score_player2
    G = np.tile(game.grid, (glb.NUMBER_SIMULATION, 1, 1))
    X = np.tile(x, glb.NUMBER_SIMULATION)
    Y = np.tile(y, glb.NUMBER_SIMULATION)
    S = np.tile(base_score, glb.NUMBER_SIMULATION)
    I = np.arange(glb.NUMBER_SIMULATION)
    dx = np.array([0, -1, 0, 1, 0], dtype=np.int8)
    dy = np.array([0, 0, 1, 0, -1], dtype=np.int8)
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
    """Load all move available for the simulation

    Arguments:
        G {np.array[I, X, Y]} -- Game simulated
        X {np.array[I]} -- All X position
        Y {np.array[I]} -- All Y position
        I {np.array[]} -- A np.arange() of number of simulation

    Returns:
        tuple -- all move possible for the simulation and indexes available
    """
    all_posibilities = np.zeros((glb.NUMBER_SIMULATION, 4), dtype=np.uint8)
    indexes = np.zeros(glb.NUMBER_SIMULATION, dtype=np.uint8)
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
    """Put all 0 into the end of the array

    Arguments:
        array {np.array[]} -- The array

    Returns:
        np.array[] -- The array formatted
    """
    valid_mask = array != 0
    flipped_mask = valid_mask.sum(1, keepdims=1) > np.arange(array.shape[1] - 1, -1, -1)
    flipped_mask = flipped_mask[:, ::-1]
    array[flipped_mask] = array[valid_mask]
    array[~flipped_mask] = 0
    return array


def get_random_choice(posibilities, indexes, I):
    """Return a random move for each game simulated

    Arguments:
        posibilities {np.array[I][]} -- All move for each game
        indexes {np.array[I][]} -- All indexes for each game
        I {np.array[]} -- arange of number of game

    Returns:
        np.array[I] -- Array of indexes of direction
    """
    random_index = np.random.randint(12, size=glb.NUMBER_SIMULATION)
    random_index = random_index % indexes
    return posibilities[I, random_index]
