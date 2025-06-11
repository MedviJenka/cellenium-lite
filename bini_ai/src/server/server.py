import uvicorn
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from bini_ai.src.utils.bini_utils import BiniUtils
from dotenv import load_dotenv
from fastapi import FastAPI


router = APIRouter(prefix="/api/v1", tags=["Bini"])
load_dotenv()
app = FastAPI(title="Bini AI API", version="1.0.0")
app.include_router(router)


class BiniImageRequest(BaseModel):
    prompt: str
    image_path: str
    sample_image: List[str]


class BiniResponse(BaseModel):
    status: str
    result: dict


def get_bini_utils() -> BiniUtils:
    return BiniUtils(to_json=True)


@router.get("/")
def health_check():
    return {"status": "healthy"}


@router.post("/bini_image", response_model=BiniResponse)
def run_bini_image(request: BiniImageRequest, bini: BiniUtils = Depends(get_bini_utils)):
    result = bini.run_image(prompt=request.prompt, image_path=request.image_path, sample_image=request.sample_image)
    if hasattr(result, "to_json"):
        return result.to_json()
    return {
        "status": "error",
        "result": result
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
