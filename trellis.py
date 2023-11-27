class Trellis:

    @staticmethod
    def log_sum_of_branch_and_path_metrics(path_m, branch_m):
        result = [path + branch for path, branch in zip(path_m, branch_m)]
        return max(result)

    transition_matrix = [[(-1, -1), None, (1, 1), None],
                                  [(1, -1), None, (-1, 1), None],
                                  [None, (-1, -1), None, (1, 1)],
                                  [None, (1, -1), None, (-1, 1)]]

    origin_state = [(0, 1), (2, 3), (0, 1), (2, 3)]
    future_state = [(0, 2), (0, 2), (1, 3), (1, 3)]

    possible_transitions = [(0,0),(0,2),(1,0),(1,2),(2,1),(2,3),(3,0),(3,2)]
