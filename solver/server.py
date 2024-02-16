from fastapi import FastAPI, Query
from pydantic import BaseModel

from solver import AssignmentSolver

app = FastAPI()


class DoubleSolve(BaseModel):
    matrix1: list[list[float]]
    matrix2: list[list[float]]
    coeff1: float
    coeff2: float


@app.post("/solve_single")
def solve_single(matrix: list[list[float | int]], maximaze: bool = Query(True)):
    coeff = 1 if maximaze else -1
    solver = AssignmentSolver(costses=[matrix], coeffs=[coeff])

    resh, sum_proizv = solver.solve()
    return {"resh": resh, "sum": sum_proizv}


@app.post("/solve_double")
def solve_double(payload: DoubleSolve):
    solver = AssignmentSolver(
        costses=[payload.matrix1, payload.matrix2],
        coeffs=[payload.coeff1, payload.coeff2],
    )

    resh, sum_proizv = solver.solve()
    return {"resh": resh, "sum": sum_proizv}
