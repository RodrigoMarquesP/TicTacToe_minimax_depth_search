# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 11:27:19 2020.

@author: sucod
"""

import numpy as np


def minimax_move(actual_state: np.array) -> np.array:
    """
    Find the optimal move in a tictactoe game with recursive depth search.

    Parameters
    ----------
    actual_state : numpy.array
        3x3 array that describes the actual state of the game.

    Returns
    -------
    numpy.array
        3x3 array that describes the best move to be done.

    """
    move_utility = []
    moves = valid_moves(actual_state)
    for move in moves:
        v = minvalue(move)
        if v == 1:  # in case of 1 utility - win -, select this move
            return move
        else:
            # in case of non garanted winning, we look for all states
            # and list its utilitys
            move_utility.append(v)
    try:
        # try to find an "tied utility move", since wasn't a certain win
        return moves[move_utility.index(0)]
    except ValueError:
        # return any move, since all of them lead to a defeat
        # NOTE: this try/except is just for debuging and testing
        # purpose, since the algorithm will never lose in a normal
        # game, so, the ValueError will never happen
        return moves[0]


"""Debug function."""
# def minimax_move(actual_state):
#     move_utility = []
#     moves = valid_moves(actual_state)
#     for move in moves:
#         v = minvalue(move)
#         move_utility.append(v)
#     print(moves)
#     print(move_utility)
#     return move_utility


def valid_moves(state: np.array, marker: int = 1) -> np.array:
    """
    Generate the valid moves for a given state of the game.

    Parameters
    ----------
    state : numpy.array
        3x3 array that describes the state node of the game.
    marker : int, optional
        Mark the valid moves (1 for machine, -1 for oponent). The default is 1.

    Returns
    -------
    moves : numpy.array
        A array of all the possible moves in the node.

    """
    n_moves = 9 - np.count_nonzero(state)  # counting the valid moves
    moves = np.zeros((n_moves, 3, 3), dtype='int8')  # a array of states
    for index, item in np.ndenumerate(state):
        if item == 0:  # if isn't a mark in this position
            new = np.copy(state)
            new[index] = marker  # mark
            moves[n_moves - 1] = new  # put the new move in the moves array
            n_moves -= 1  # ajust the position of the next new state
    np.random.shuffle(moves)  # shuffle the moves
    # the reason of shuffling the states array is to make the
    # moves less predictable, making the machine select any of
    # the states with higher utility
    return moves


def minvalue(state: np.array) -> int:
    """
    Simulate the perfect oponent move - lower utility.

    Parameters
    ----------
    state : numpy.array
        Actual node of the search.

    Returns
    -------
    v : int
        Utility of node according to minimax logics.

    """
    global counter
    counter += 1
    for v in terminal_test(state):
        # using a 'for block' with a single element list
        # allow us to return the utility of the state
        # if it's a terminal one, without a couple of 'if blocks'
        return v
    v = 2  # higher than any real utility
    for move in valid_moves(state, marker=-1):
        # Select the lower utility move between the machine moves
        v = mini(v, maxvalue(move))
    return v


def maxvalue(state: np.array) -> int:
    """
    Choose the best move for the machine - higher utility.

    Parameters
    ----------
    state : numpy.array
        Actual node of the search.

    Returns
    -------
    v : int
        Utility of node according to minimax logics.

    """
    global counter
    counter += 1
    for v in terminal_test(state):
        # using a 'for block' with a single element list
        # allow us to return the utility of the state
        # if it's a terminal one, without a couple of 'if blocks'
        return v
    v = -2  # lower than any real utility
    for move in valid_moves(state):
        # Select the higher utility move between the oponent moves
        v = maxi(v, minvalue(move))
    return v


def mini(a: int, b: int) -> int:
    """
    Return the lower of two arguments.

    Parameters
    ----------
    a : int
        A utility value.
    b : int
        A utility value.

    Returns
    -------
    int
        The lower between the two parameters.

    """
    return a if b > a else b


def maxi(a: int, b: int) -> int:
    """
    Return the higher of two arguments.

    Parameters
    ----------
    a : int
        A utility value.
    b : int
        A utility value.

    Returns
    -------
    int
        The higher between the two parameters.

    """
    return a if a > b else b


def terminal_test(node: np.array) -> list:
    """
    Return the utility of the state.

    ([] if its not a terminal node)
    ([1] if its a winning node)
    ([-1] if its a losing node)

    Parameters
    ----------
    node : np.array
        Actual node of the search.

    Returns
    -------
    list
        A single element list with the utility of the requested node.

    """
    if 3 in np.sum(node, axis=0) or 3 in np.sum(node, axis=1):
        return [1]
    if (node[(0, 0)] + node[(1, 1)] + node[(2, 2)]) == 3:
        return [1]
    if (node[(0, 2)] + node[(1, 1)] + node[(2, 0)]) == 3:
        return [1]
    if -3 in np.sum(node, axis=0) or -3 in np.sum(node, axis=1):
        return [-1]
    if (node[(0, 0)] + node[(1, 1)] + node[(2, 2)]) == -3:
        return [-1]
    if (node[(0, 2)] + node[(1, 1)] + node[(2, 0)]) == -3:
        return [-1]
    if np.count_nonzero(node) == 9:
        # non-terminal state
        return [0]
    return []


if __name__ == '__main__':
    # these instructions is just for testing the code and see its peformance.
    import time
    counter = 0
    table = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype='int8')
    begin = time.time()
    print(minimax_move(table))
    end = time.time()
    delta = end - begin
    print('\n', counter, 'states visited')
    print(f'\n {delta:.5f} seconds to execute')
