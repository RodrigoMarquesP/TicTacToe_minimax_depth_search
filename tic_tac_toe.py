# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 11:27:19 2020

@author: sucod
"""

import numpy as np


def jogada_minimax(estado_atual):
    utilidade = []
    jogadas = jogadas_validas(estado_atual)
    for jogada in jogadas:
        v = valormin(jogada)
        if v == 1:
            return jogada
        else:
            utilidade.append(v)
    try:
        return jogadas[utilidade.index(0)]
    except ValueError:
        return jogadas[0]


"""função para testes."""
# def jogada_minimax(estado_atual):
#     utilidade = []
#     jogadas = jogadas_validas(estado_atual)
#     for jogada in jogadas:
#         v = valormin(jogada)
#         utilidade.append(v)
#     print(jogadas)
#     print(utilidade)
#     return utilidade


def jogadas_validas(estado, marcar=1):
    n_jogadas = 9 - np.count_nonzero(estado)
    jogadas = np.zeros((n_jogadas, 3, 3), dtype='int8')
    for index, elemento in np.ndenumerate(estado):
        if elemento == 0:
            novo = np.copy(estado)
            novo[index] = marcar
            jogadas[n_jogadas - 1] = novo
            n_jogadas -= 1
    np.random.shuffle(jogadas)
    return jogadas


def valormin(estado):
    for v in teste_terminal(estado):
        return v
    v = 2
    for jogada in jogadas_validas(estado, marcar=-1):
        v = mini(v, valormax(jogada))
    return v


def valormax(estado):
    for v in teste_terminal(estado):
        return v
    v = -2
    for jogada in jogadas_validas(estado):
        v = maxi(v, valormin(jogada))
    return v


def mini(a, b):
    return a if b > a else b


def maxi(a, b):
    return a if a > b else b


def teste_terminal(no):
    if 3 in np.sum(no, axis=0) or 3 in np.sum(no, axis=1):
        return [1]
    if (no[(0, 0)] + no[(1, 1)] + no[(2, 2)]) == 3:
        return [1]
    if (no[(0, 2)] + no[(1, 1)] + no[(2, 0)]) == 3:
        return [1]
    if -3 in np.sum(no, axis=0) or -3 in np.sum(no, axis=1):
        return [-1]
    if (no[(0, 0)] + no[(1, 1)] + no[(2, 2)]) == -3:
        return [-1]
    if (no[(0, 2)] + no[(1, 1)] + no[(2, 0)]) == -3:
        return [-1]
    if np.count_nonzero(no) == 9:
        return [0]
    return []


x = np.array([[0, -1, 0], [0, 0, 0], [0, 0, 0]])
# tabuleiro = np.zeros((3, 3), dtype='int8')
# print(jogadas_validas(tabuleiro))
print(jogada_minimax(x))
