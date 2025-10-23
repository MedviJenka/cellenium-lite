from typing import Optional, Dict, Any
from backend.ai.flows.bini import BiniImage
from backend.ai.flows.chat import BiniChatFlow
from dataclasses import dataclass
from backend.utils.logger import Logfire


log = Logfire(name='bini-service-utils')


@dataclass
class BiniServiceUtils:

    to_json: Optional[bool] = True
    chain_of_thought: Optional[bool] = True,

    def __post_init__(self) -> None:
        self.__bini_image = BiniImage(chain_of_thought=self.chain_of_thought, to_json=self.to_json)

    async def run_image(self, prompt: str, image_path: str, sample_image=None) -> Dict[str, Any]:
        """Async version - for FastAPI endpoints"""
        try:
            # Run the flow
            flow_result = await self.__bini_image.kickoff_async(inputs={
                "original_prompt": prompt,
                "image": image_path,
                "sample_image": sample_image
            })

            # FIXED: Return the actual AI analysis, not just status
            # The AI analysis should be in the flow state
            final_state = self.__bini_image.state

            if self.__bini_image.chain_of_thought:
                # Return full details when chain_of_thought is True
                return {
                    "analysis": final_state.result,  # The actual AI analysis
                    "metadata": {
                        "original_prompt": final_state.original_prompt,
                        "refined_prompt": final_state.refined_prompt,
                        "image_path": final_state.image,
                        "sample_images": final_state.sample_image,
                        "chain_of_thought": final_state.chain_of_thought,
                        "to_json": final_state.to_json
                    },
                    "cache": final_state.cached_data,
                    "flow_result": flow_result  # Include the flow execution result
                }
            else:
                # Return simplified response when chain_of_thought is False
                return {
                    "analysis": final_state.result,
                    "prompt": final_state.original_prompt
                }

        except Exception as e:
            log.fire.error(f"Image analysis failed: {e}")
            raise


@dataclass
class BiniChatUtils:

    file_path: Optional[str] = None
    to_json: Optional[bool] = True
    chain_of_thought: Optional[bool] = True,

    def __post_init__(self) -> None:
        self.__bini_chat = BiniChatFlow(chain_of_thought=self.chain_of_thought)

    async def run(self, prompt: str, content: str) -> ...:
        """ask bini to analyze text"""
        try:
            flow = self.__bini_chat.kickoff_async(inputs={"prompt": prompt, "content": content})
            return flow

        except Exception as e:
            raise Exception(f"Text analysis failed: {str(e)}")
