from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import uvicorn 
from typing import List
from url import URL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[URL],  
    allow_methods=["POST"],
    allow_headers=["*"],
)

class FunctionRequest(BaseModel):
    functionText: str
    rangeStart: float
    rangeEnd: float

class Point(BaseModel):
    x: float
    y: float

@app.post("/plot", response_model=List[Point])
async def plot_function(request: FunctionRequest):
    try:
        x_values = np.linspace(request.rangeStart, request.rangeEnd, 100)
        y_values = eval(request.functionText.replace('sin', 'np.sin').replace('cos', 'np.cos').replace('tan', 'np.tan').replace('x', 'x_values'))
        points = [{"x": x, "y": y} for x, y in zip(x_values, y_values)]
        return points
    except Exception as e:
        print(f"Error plotting function: {e}")
        return []

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)