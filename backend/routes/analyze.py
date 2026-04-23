from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from models.schemas import AnalyzeResponse
from services.multimodal_fusion import analyze_multimodal

router = APIRouter(tags=["analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    responses={
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    },
)
async def analyze(
    text: str = Form(...),
    image: UploadFile | None = File(None),
) -> AnalyzeResponse:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="`text` is required.")

    try:
        result = await analyze_multimodal(text=text, image=image)
        return AnalyzeResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

