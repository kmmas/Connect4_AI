from heuristic import heuristic
from constant import *
from State import State
import random
import copy


def minMaxWithProuning(
    state: State, maxDepth, turn, alpha=float("-inf"), beta=float("inf")
):
    if maxDepth == 0 or state.isTerminalState():
        val = heuristic(state)
        state.setValue(val)
        return val, state, 0
    return (
        MinWithProuning(state, alpha, beta, maxDepth)
        if turn == AI
        else MaxWithProuning(state, alpha, beta, maxDepth)
    )


def MaxWithProuning(state: State, alpha, beta, depth):
    v = float("-inf")
    n: State = None
    state.getActions(AI)
    count = 1
    for neighbour in state.children:
        tmp = minMaxWithProuning(neighbour, depth - 1, AI, alpha, beta)
        count += tmp[2]
        vDash = tmp[0]
        if vDash > v:
            v = vDash
            n = neighbour
        if vDash >= beta:
            state.setValue(v)
            return v, neighbour, count
        alpha = max(alpha, vDash)
    state.setValue(v)
    return v, n, count


def MinWithProuning(state: State, alpha, beta, depth):
    v = float("inf")
    n: State = None
    state.getActions(PLAYER)
    count = 1
    for neighbour in state.children:
        tmp = minMaxWithProuning(neighbour, depth - 1, PLAYER, alpha, beta)
        count += tmp[2]
        vDash = tmp[0]
        if vDash < v:
            v = vDash
            n = neighbour
        if vDash <= alpha:
            state.setValue(v)
            return v, neighbour, count
        beta = min(beta, vDash)
    state.setValue(v)
    return v, n, count
