from heuristic import heuristic
from State import State
from constant import *
import copy


def minMax(state: State, maxDepth: int, turn: str):
    if maxDepth == 0 or state.isTerminalState():
        val = heuristic(state)
        state.setValue(val)
        return val, state, 0
    return min_minMax(state, maxDepth) if turn == AI else max_minMax(state, maxDepth)


def min_minMax(state: State, maxDepth: int):
    value = float("inf")
    n: State = None
    state.getActions(PLAYER)
    count = 1
    for child in state.children:
        tmp = minMax(child, maxDepth - 1, PLAYER)
        count += tmp[2]
        v = min(value, tmp[0])
        if v < value:
            value = v
            n = child
    state.setValue(value)
    return value, n, count


def max_minMax(state: State, maxDepth: int):
    value = float("-inf")
    n: State = None
    state.getActions(AI)
    count = 1
    for child in state.children:
        tmp = minMax(child, maxDepth - 1, AI)
        count += tmp[2]
        v = max(value, tmp[0])
        if v > value:
            value = v
            n = child
    state.setValue(value)
    return value, n, count
