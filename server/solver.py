from ortools.sat.python import cp_model


class AssignmentSolver:
    def __init__(self, costses: list[list[list[float | int]]], coeffs: list[float]):
        self._len = len(costses)
        self._costses = costses
        self._normalizeds = [self._normalize_matrix(cost) for cost in self._costses]
        self._coeffs = coeffs
        self._num_workers = len(self._costses[0])
        self._num_tasks = len(self._costses[0][0])

        self._model = cp_model.CpModel()

        self._make_variables()
        self._make_constraints()
        self._make_objectives()
        self._model.Maximize(sum(self._objective_terms))

    def solve(self):
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)

        if status == cp_model.OPTIMAL:
            assigned = [[0] * self._num_tasks for _ in range(self._num_workers)]
            normalized_resh = 0.0
            resh = [0.0 for _ in range(self._len)]

            for i in range(self._num_workers):
                for j in range(self._num_tasks):
                    if solver.BooleanValue(self._x[i][j]):
                        assigned[i][j] = 1
                        for idx in range(self._len):
                            resh[idx] += self._costses[idx][i][j]
                            normalized_resh += (
                                self._normalizeds[idx][i][j] * self._coeffs[idx]
                            )
            return assigned, normalized_resh, resh
        else:
            return None, None, None

    def _make_variables(self):
        self._x = []
        for i in range(self._num_workers):
            t = []
            for j in range(self._num_tasks):
                t.append(self._model.NewBoolVar("x[%i,%i]" % (i, j)))
            self._x.append(t)

    def _make_constraints(self):
        if self._num_workers == self._num_tasks:
            for i in range(self._num_workers):
                self._model.Add(sum(self._x[i][j] for j in range(self._num_tasks)) == 1)
            for j in range(self._num_tasks):
                self._model.Add(
                    sum(self._x[i][j] for i in range(self._num_workers)) == 1
                )
        elif self._num_workers > self._num_tasks:
            for i in range(self._num_workers):
                self._model.Add(sum(self._x[i][j] for j in range(self._num_tasks)) <= 1)
            for j in range(self._num_tasks):
                self._model.Add(
                    sum(self._x[i][j] for i in range(self._num_workers)) == 1
                )
        else:
            for i in range(self._num_workers):
                self._model.Add(sum(self._x[i][j] for j in range(self._num_tasks)) == 1)
            for j in range(self._num_tasks):
                self._model.Add(
                    sum(self._x[i][j] for i in range(self._num_workers)) <= 1
                )

    def _make_objectives(self):
        self._objective_terms = []
        for i in range(self._num_workers):
            for j in range(self._num_tasks):
                term = 0
                for idx in range(self._len):
                    term += (
                        self._normalizeds[idx][i][j] * self._x[i][j] * self._coeffs[idx]
                    )
                self._objective_terms.append(term)

    def _normalize_matrix(self, matrix) -> list[list[float]]:
        max_value = max(max(row) for row in matrix)
        normalized_matrix = [
            [(cell / max_value) * 100 for cell in row] for row in matrix
        ]
        return normalized_matrix
