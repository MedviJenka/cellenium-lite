import os
import tempfile
from pydantic import BaseModel, create_model, Field
from fastapi import FastAPI
from typing import AsyncGenerator, Type, Any, Dict
from typing import Optional, List
from backend.settings import Config
from backend.utils.logger import Logfire
from contextlib import asynccontextmanager
from backend.ai.flows.chat import BiniChatFlow
from backend.api.v1.bini.schemas import AnalysisResponse, ChatRequest
from backend.api.v1.bini.logic import validate_image_file
from backend.utils.bini_service import BiniServiceUtils
from fastapi import File, UploadFile, Form, APIRouter, HTTPException


log = Logfire(name='bini-api')


def json_schema_to_pydantic(schema: Dict[str, Any]) -> Type[BaseModel]:
    """Convert JSON schema dict to Pydantic BaseModel class."""
    type_map = {'string': str, 'integer': int, 'number': float, 'boolean': bool, 'array': list, 'object': dict}
    fields = {
        name: (type_map.get(info.get('type', 'string'), str), info.get('default', ...))
        for name, info in schema.get('properties', {}).items()
    }
    return create_model(schema.get('title', 'DynamicModel'), **fields)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    log.fire.info("Bini service started successfully")
    yield
    log.fire.info("Bini service shutting down")


router = APIRouter(prefix=f"/api/{Config.API_VERSION}/bini", tags=["bini"])


@router.post(path="/image")
async def analyze_image(prompt: str = Form(...),
                        image: UploadFile = File(...),
                        chain_of_thought: bool = Form(False),
                        sample_images: Optional[List[UploadFile]] = File(None)
                        ) -> AnalysisResponse or None:
    """
    Analyze the provided main image with optional sample images.
    """
    temp_file_path = None
    temp_sample_paths = []

    try:
        # Read and validate the main image
        main_content = await image.read()
        main_ext = validate_image_file(image.filename, len(main_content))

        with tempfile.NamedTemporaryFile(delete=False, suffix=main_ext) as temp_file:
            temp_file.write(main_content)
            temp_file_path = temp_file.name

        # Process sample images if provided
        processed_sample_images = None

        if sample_images:

            processed_sample_images = []

            for sample_img in sample_images:
                sample_content = await sample_img.read()
                sample_ext = validate_image_file(sample_img.filename, len(sample_content))

                with tempfile.NamedTemporaryFile(delete=False, suffix=sample_ext) as temp_sample_file:
                    temp_sample_file.write(sample_content)
                    temp_sample_paths.append(temp_sample_file.name)
                    processed_sample_images.append(temp_sample_file.name)

        # Run analysis
        bini = BiniServiceUtils(chain_of_thought=chain_of_thought)
        result = await bini.run_image(prompt=prompt, image_path=temp_file_path, sample_image=processed_sample_images)

        return result

    except HTTPException:
        raise
    except Exception as e:
        log.fire.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error during analysis: {str(e)}")

    finally:
        # Clean up temp files
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                log.fire.info("Cleaned up main temp file")
            except Exception as e:
                log.fire.warning(f"Failed to clean up main temp file: {e}")

        for temp_path in temp_sample_paths:
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                    log.fire.info(f"Cleaned up sample temp file: {temp_path}")
                except Exception as e:
                    log.fire.warning(f"Failed to clean up sample temp file {temp_path}: {e}")


@router.post("/chat")
async def analyze_text(request: ChatRequest) -> dict:
    """
    Analyze text with optional structured output schema.
    
    Args:
        request: ChatRequest containing prompt, chain_of_thought, and optional schema_output
    """
    try:
        # Convert schema dict to Pydantic model if provided
        pydantic_schema = None
        if request.schema_output:
            log.fire.info(f"Received schema: {request.schema_output}")
            pydantic_schema = json_schema_to_pydantic(request.schema_output)
            log.fire.info(f"Created dynamic schema: {pydantic_schema.__name__}")

        bini_chat = BiniChatFlow()

        response = await bini_chat.kickoff_async(inputs={
                "prompt": request.prompt,
                "chain_of_thought": request.chain_of_thought,
                "schema_output": pydantic_schema,
            }
        )

        return response
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        log.fire.error(f"Chat analysis failed: {error_details}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
