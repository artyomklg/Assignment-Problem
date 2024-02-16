from ortools.sat.python import cp_model


class AssignmentSolver:
    def __init__(self, costses: list[list[list[int]]], coeffs: list[float]):
        if len(costses) == 2:
            self._costs1 = costses[0]
            self._costs2 = costses[1]
            self._normalized1 = self._normalize_matrix(self._costs1)
            self._normalized2 = self._normalize_matrix(self._costs2)
            if len(self._costs1) == len(self._costs2):
                self._num_workers = len(self._costs1)
            else:
                raise Exception
            if len(self._costs1[0]) == len(self._costs2[0]):
                self._num_tasks = len(self._costs1[0])
            else:
                raise Exception
            self._coeff1 = coeffs[0]
            self._coeff2 = coeffs[1]

            self.__single = False

        else:
            self._costs = costses[0]
            self._num_workers = len(self._costs)
            self._num_tasks = len(self._costs[0])
            self._coeff = coeffs[0]
            self.__single = True

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
            if self.__single:
                sum_proizv = 0
            else:
                sum_proizv = [0, 0, 0.0]
            for i in range(self._num_workers):
                for j in range(self._num_tasks):
                    if solver.BooleanValue(self._x[i][j]):
                        if self.__single:
                            assigned[i][j] = 1
                            sum_proizv += self._costs[i][j]
                        else:
                            assigned[i][j] = 1
                            sum_proizv[0] += self._costs1[i][j]
                            sum_proizv[1] += self._costs2[i][j]
                            sum_proizv[2] += (
                                self._normalized1[i][j] * self._coeff1
                                + self._normalized2[i][j] * self._coeff2
                            )
            return assigned, sum_proizv
        else:
            return None, None

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
                if self.__single:
                    self._objective_terms.append(
                        self._costs[i][j] * self._x[i][j] * self._coeff
                    )
                else:
                    term1 = self._normalized1[i][j] * self._x[i][j] * self._coeff1
                    term2 = self._normalized2[i][j] * self._x[i][j] * self._coeff2
                    self._objective_terms.append(term1 + term2)

    def _normalize_matrix(self, matrix):
        max_value = max(max(row) for row in matrix)
        normalized_matrix = [
            [(cell / max_value) * 100 for cell in row] for row in matrix
        ]
        return normalized_matrix
