from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from version import __version__

app = FastAPI(
    title="API Калькулятор",
    description="Простой API для выполнения арифметических операций.",
    version=__version__
)

class Calculation(BaseModel):
    operation: str
    operands: list[float]

@app.post("/calculate")
async def calculate(calc: Calculation):
    if not calc.operands:
        raise HTTPException(status_code=400, detail="Не предоставлены операнды.")
    
    operation = calc.operation.lower()
    operands = calc.operands

    if operation == "add":
        result = sum(operands)
    elif operation == "subtract":
        result = operands[0]
        for num in operands[1:]:
            result -= num
    elif operation == "multiply":
        result = 1
        for num in operands:
            result *= num
    elif operation == "divide":
        result = operands[0]
        try:
            for num in operands[1:]:
                result /= num
        except ZeroDivisionError:
            raise HTTPException(status_code=400, detail="Деление на ноль.")
    else:
        raise HTTPException(status_code=400, detail="Неподдерживаемая операция.")
    
    return {"result": result}
