from pydantic import BaseModel, Field


class AnalyzeResponse(BaseModel):
    prediction: str = Field(..., examples=["Likely Fake"])
    confidence: float = Field(..., ge=0.0, le=1.0, examples=[0.85])
    explanation: str = Field(..., examples=["Reasoning here"])


class ErrorResponse(BaseModel):
    detail: str

