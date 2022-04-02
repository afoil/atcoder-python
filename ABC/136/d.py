import io
import sys

_INPUT = """\
RRRLLRLLRRRLLLLL
"""
sys.stdin = io.StringIO(_INPUT)

# submit code--------------------------------------------------------
"""
文字列Sに必ずRLの部分列は存在し、マス間の移動はこの部分列でループする。
今回、試行回数が10^100と十分に多く、マス間の移動がループするまでの回数は
高々len(S)しか必要ないことから、10^100回施行した後は全てのマスがループしている。
そのためRLの文字列の左側Rに到達する回数(mod 2)と、どのRLの文字列に到達したかを
各マス目において計算すればよい。
すべてのマス目において計算すると計算量がO(len(S)^2)になるので途中経過を保持する。
"""
from typing import NamedTuple


class EquilibriaState(NamedTuple):
    dst_to_RL_mod2: int
    loc_RL: int


# input
S = input()

# initialize
equilibria_states = [EquilibriaState(dst_to_RL_mod2=0, loc_RL=0)] * len(S)

# 左側から
for i, char in enumerate(S):
    if char == "R":
        # visitedな場合は前の結果を使う
        if i > 0 and S[i - 1] == "R":
            state = equilibria_states[i - 1]
            dst = (state.dst_to_RL_mod2 - 1) % 2
            loc = state.loc_RL
            equilibria_states[i] = EquilibriaState(dst_to_RL_mod2=dst, loc_RL=loc)
        else:
            for j in range(i + 1, len(S)):
                if S[j] == "L":
                    equilibria_states[i] = EquilibriaState(
                        dst_to_RL_mod2=(j - 1 - i) % 2, loc_RL=j - 1
                    )
                    break

# 右側から
for i in range(len(S) - 1, -1, -1):
    if S[i] == "L":
        # visitedな場合は前の結果を使う
        if i < len(S) - 1 and S[i + 1] == "L":
            state = equilibria_states[i + 1]
            dst = (state.dst_to_RL_mod2 - 1) % 2
            loc = state.loc_RL
            equilibria_states[i] = EquilibriaState(dst_to_RL_mod2=dst, loc_RL=loc)
        else:
            for j in range(i - 1, -1, -1):
                if S[j] == "R":
                    equilibria_states[i] = EquilibriaState(
                        dst_to_RL_mod2=(i - j) % 2, loc_RL=j
                    )
                    break

# output
answer = [0] * len(S)
for i, state in enumerate(equilibria_states):
    dst = state.dst_to_RL_mod2
    loc = state.loc_RL
    answer[(dst % 2) + loc] += 1


print(" ".join(list(map(str, answer))))
# --------------------------------------------------------
