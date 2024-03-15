from decimal import Decimal
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from solver import AssignmentSolver

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


class Payload(BaseModel):
    matrix: list[list[float]]
    coefficient: float
    option: Literal["min", "max"]


class ReshResponse(BaseModel):
    resh: list[list[Literal[0, 1]]]
    sum_proizv: list[float]
    normalized_sum: float


@app.post("/solve", response_model=ReshResponse)
def solve(payloads: list[Payload]):
    total_coefficient = Decimal("0")
    for payload in payloads:
        total_coefficient += Decimal(str(payload.coefficient))
    if total_coefficient != Decimal("1"):
        raise HTTPException(
            status_code=400, detail="The total coefficient is not equal to 1"
        )
    matrixes = []
    coeffs = []
    for payload in payloads:
        matrixes.append(payload.matrix)
        coeffs.append(
            payload.coefficient if payload.option == "max" else payload.coefficient * -1
        )
    solver = AssignmentSolver(costses=matrixes, coeffs=coeffs)

    matrix_resh, normalized_sum, sum_proizv = solver.solve()
    return {
        "resh": matrix_resh,
        "sum_proizv": sum_proizv,
        "normalized_sum": normalized_sum,
    }
