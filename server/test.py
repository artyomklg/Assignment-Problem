from pprint import pprint

from ortools.sat.python import cp_model

from solver import AssignmentSolver

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

    solvern = AssignmentSolver(costses=[costs1, costs2], coeffs=[0.5, -0.5])

    reshn, sumn, a = solvern.solve()

    pprint(resh1)
    print(sum1)
    print("\n\n")
    pprint(resh2)
    print(sum2)
    print("\n\n")
    pprint(reshn)
    print(sumn)
    print("\n\n")
