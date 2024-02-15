from ortools.sat.python import cp_model


def normalize_matrix(matrix):
    max_value = max(max(row) for row in matrix)
    normalized_matrix = [[(cell / max_value) * 100 for cell in row] for row in matrix]
    return normalized_matrix


def solve_assignment_problem_single(costs: list[list[int]], maximaze: bool):
    num_workers = len(costs)
    num_tasks = len(costs[0])

    model = cp_model.CpModel()

    # Variables
    x = []
    for i in range(num_workers):
        t = []
        for j in range(num_tasks):
            t.append(model.NewBoolVar("x[%i,%i]" % (i, j)))
        x.append(t)

    if num_workers == num_tasks:
        for i in range(num_workers):
            model.Add(sum(x[i][j] for j in range(num_tasks)) == 1)
        for j in range(num_tasks):
            model.Add(sum(x[i][j] for i in range(num_workers)) == 1)
    elif num_workers > num_tasks:
        for i in range(num_workers):
            model.Add(sum(x[i][j] for j in range(num_tasks)) <= 1)
        for j in range(num_tasks):
            model.Add(sum(x[i][j] for i in range(num_workers)) == 1)
    else:
        for i in range(num_workers):
            model.Add(sum(x[i][j] for j in range(num_tasks)) == 1)
        for j in range(num_tasks):
            model.Add(sum(x[i][j] for i in range(num_workers)) <= 1)

    # Objective
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(costs[i][j] * x[i][j])
    if maximaze:
        model.Maximize(sum(objective_terms))
    else:
        model.Minimize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        assigned = [[0] * num_tasks for _ in range(num_workers)]
        sum_proizv = 0
        for i in range(num_workers):
            for j in range(num_tasks):
                if solver.BooleanValue(x[i][j]):
                    assigned[i][j] = 1
                    sum_proizv += costs[i][j]
        return assigned, sum_proizv
    else:
        return None, None


def solve_assignment_problem(
    costs1: list[list[int]], costs2: list[list[int]], coeff1: float, coeff2: float
):
    normalized1 = normalize_matrix(costs1)
    normalized2 = normalize_matrix(costs2)

    num_workers = len(costs1)
    num_tasks = len(costs1[0])

    # Create the model.
    model = cp_model.CpModel()

    # Variables
    x = []
    for i in range(num_workers):
        t = []
        for j in range(num_tasks):
            t.append(model.NewBoolVar("x[%i,%i]" % (i, j)))
        x.append(t)

    # Constraints
    if num_workers == num_tasks:
        for i in range(num_workers):
            model.Add(sum(x[i][j] for j in range(num_tasks)) == 1)
        for j in range(num_tasks):
            model.Add(sum(x[i][j] for i in range(num_workers)) == 1)
    elif num_workers > num_tasks:
        for i in range(num_workers):
            model.Add(sum(x[i][j] for j in range(num_tasks)) <= 1)
        for j in range(num_tasks):
            model.Add(sum(x[i][j] for i in range(num_workers)) == 1)
    else:
        for i in range(num_workers):
            model.Add(sum(x[i][j] for j in range(num_tasks)) == 1)
        for j in range(num_tasks):
            model.Add(sum(x[i][j] for i in range(num_workers)) <= 1)

    # Objective
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            term1 = normalized1[i][j] * x[i][j] * coeff1
            term2 = normalized2[i][j] * x[i][j] * coeff2
            objective_terms.append(term1 + term2)

    model.Maximize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        assigned = [[0] * num_tasks for _ in range(num_workers)]
        sum_proizv = [0, 0, 0.0]
        for i in range(num_workers):
            for j in range(num_tasks):
                if solver.BooleanValue(x[i][j]):
                    assigned[i][j] = 1
                    sum_proizv[0] += costs1[i][j]
                    sum_proizv[1] += costs2[i][j]
                    sum_proizv[2] += (
                        normalized1[i][j] * coeff1 + normalized2[i][j] * coeff2
                    )
        return assigned, sum_proizv
    else:
        return None, None


# Example usage
if __name__ == "__main__":
    costs1 = [
        [3, 2, 5, 0, 0, 1, 4],
        [7, 9, 9, 9, 4, 5, 4],
        [10, 7, 2, 3, 7, 8, 10],
        [2, 5, 7, 5, 8, 10, 3],
        [1, 3, 4, 9, 9, 8, 0],
        [8, 6, 8, 4, 5, 2, 1],
        [6, 1, 3, 10, 9, 7, 8],
        [6, 8, 2, 6, 6, 6, 6],
    ]
    costs2 = [
        [1043, 857, 861, 1014, 1434, 1460, 1442],
        [1281, 1144, 1286, 634, 754, 1205, 989],
        [1360, 738, 1321, 706, 1312, 1244, 1019],
        [1217, 1105, 1371, 1497, 1406, 512, 647],
        [707, 1143, 1233, 515, 1248, 977, 1495],
        [1390, 788, 1302, 1095, 1241, 1486, 914],
        [1150, 1303, 560, 655, 1406, 858, 1444],
        [1304, 1463, 1120, 609, 1086, 1328, 1137],
    ]

    assigned, sum_proizv = solve_assignment_problem(costs1, costs2, 0.5, -0.5)
    if assigned is not None:
        for row in assigned:
            print(row)
        print(f"{sum_proizv=}")
    else:
        print("No solution found.")
