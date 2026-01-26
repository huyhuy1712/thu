from typing import List
from pydantic import BaseModel


class RecognitionRequest(BaseModel):
    frames: list
    previous_word: str | None = ""

class CoordinateModel(BaseModel):
    x: List[float]
    y: List[float]
    z: List[float]

class RequestModel(BaseModel):
    data: List[CoordinateModel]

