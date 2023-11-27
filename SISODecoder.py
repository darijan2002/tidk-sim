import math
import itertools
import numpy as np

from trellis import Trellis
from copy import copy, deepcopy

"""
Soft-in soft-out decoder for guessing
the appropriate bit based on the input signal
"""


class SISODecoder():
    def __init__(self):
        self.block_size = 9  # 7 data bits + 2 tail bits

        self.gamma = [[[0.0] * 4 for _ in range(4)] for _ in range(self.block_size)]
        self.alpha = [[0] + x[1:] for x in [[-math.inf] * 4 for _ in range(self.block_size+1)]]
        self.beta = deepcopy(self.alpha)

        self.LLR = [0] * self.block_size

    def decode(self, input_tuples):

        # first we compute the branch coefficients (gamma)
        for k in range(self.block_size):
            # at moment k calculate all branch metrics
            for old_state, new_state in Trellis.possible_transitions:
                input_signal, output_signal = Trellis.transition_matrix[old_state][new_state]

                self.gamma[k][old_state][new_state] = \
                    (
                            input_signal * (input_tuples[k][0] + input_tuples[k][2]) +
                            output_signal * input_tuples[k][1]
                    )

        def compute_forward(k, current_state):
            states_to_current = Trellis.origin_state[current_state]

            forward_metrics = [self.alpha[k - 1][states_to_current[0]],self.alpha[k - 1][states_to_current[1]]]
            branch_metrics = [self.gamma[k - 1][states_to_current[0]][current_state], self.gamma[k - 1][states_to_current[1]][current_state]]

            self.alpha[k][current_state] = Trellis.log_sum_of_branch_and_path_metrics(forward_metrics, branch_metrics)

        def compute_backward(k, current_state):
            states_from_current = Trellis.future_state[current_state]

            r = self.block_size - k

            backward_metrics = [self.beta[k - 1][states_from_current[0]],self.beta[k - 1][states_from_current[1]]]
            branch_metrics = [self.gamma[r][current_state][states_from_current[0]],self.gamma[r][current_state][states_from_current[1]]]

            self.beta[k][current_state] = Trellis.log_sum_of_branch_and_path_metrics(backward_metrics, branch_metrics)

        # then we compute the forward and backward coeffs (alpha and beta)
        for k in range(1, self.block_size + 1):
            for current_state in range(4):
                compute_forward(k, current_state)
                compute_backward(k, current_state)

        # finally we compute the soft output given the calculated prediction coeffs
        for k in range(self.block_size):
            r = self.block_size - k - 1

            max_neg = 0
            max_pos = 0

            for (old_state, new_state) in Trellis.possible_transitions:
                input_signal, _ = Trellis.transition_matrix[old_state][new_state]

                forward_metric = self.alpha[k][old_state]
                backward_metric = self.beta[r][new_state]
                branch_metric = self.gamma[k][old_state][new_state]

                if input_signal > 0:
                    max_pos = max(max_pos, forward_metric + backward_metric + branch_metric)
                else:
                    max_neg = max(max_neg, forward_metric + backward_metric + branch_metric)

            self.LLR[k] = max_pos - max_neg

        return self.LLR
