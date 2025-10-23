from typing import Union
from settings import Logfire
from crewai.flow import Flow, start, listen, router
from core.bini.backend.ai.flows.states import BiniImageInitialState
from core.bini.backend.ai.agents.english_agent.crew import EnglishAgent
from core.bini.backend.ai.agents.reflection_agent.crew import ReflectionAgent
from core.bini.backend.ai.agents.vision_agent.crew import ComputerVisionAgent


log = Logfire(name="bini-flow")


class BiniImage(Flow[BiniImageInitialState]):

    """
    Flow to handle image analysis using multiple agents.
    Steps:
    1. Refine the original prompt using the English agent.
    2. Analyze the image using the Computer Vision agent.
    3. Reflect on the analysis using the Reflection agent. The flow manages state transitions and error handling.
    4. Finalize the result, ensuring JSON format if required.
    5. Complete the flow.
    6. Return the final state containing prompts, results, and reflections.
    7. Log key steps and decisions for traceability.
    8. Handle invalid prompts gracefully.
    """

    def __init__(self, chain_of_thought: bool) -> None:
        self.chain_of_thought = chain_of_thought
        self.english_agent = EnglishAgent(chain_of_thought=chain_of_thought)
        self.computer_vision_agent = ComputerVisionAgent(chain_of_thought=chain_of_thought)
        self.reflection_agent = ReflectionAgent(chain_of_thought=chain_of_thought)
        super().__init__(chain_of_thought=chain_of_thought)

    @start()
    async def refine_prompt(self) -> None:
        """ Refine the original prompt using the English agent."""
        self.state.refined_prompt = self.english_agent.execute(prompt=self.state.original_prompt)
        log.fire.info(f'refined prompt: {self.state.refined_prompt}')

        if 'Invalid Question' in self.state.refined_prompt:
            self.state.cached_state = "INVALID"
        self.state.cached_state = "VALID"

    @router(refine_prompt)
    async def route_after_refine(self) -> str:
        """Route based on cached_state."""
        log.fire.info(f'is the question valid? {self.state.cached_state}')
        return "INVALID" if self.state.cached_state != "VALID" else "VALID"

    @listen("INVALID")
    async def on_invalid(self) -> str:
        """Handle an invalid prompt case."""
        self.state.cached_state = "Invalid question provided. Please provide a clear, well-formed question."
        self.state.result = "Failed: Invalid question provided. Please provide a clear, well-formed question."
        return "DONE"

    @listen("VALID")
    async def analyze_image(self) -> None:
        """Analyze the image using the Computer Vision agent."""
        result = self.computer_vision_agent.execute(prompt=self.state.refined_prompt,
                                                    image_path=self.state.image,
                                                    sample_image=self.state.sample_image)
        self.state.result = result
        log.fire.info(f'image visualization result: {self.state.result}')

    @listen(analyze_image)
    async def reflection_decision(self) -> str:
        """TODO: handle reflection router"""
        self.state.reflection = self.reflection_agent.execute(original_question=self.state.refined_prompt,
                                                              final_answer=self.state.result)
        log.fire.info(f'reflection summary: {self.state.reflection}')
        return "DONE"


async def bini_image(prompt: str,
                     image: str,
                     sample_image: Union[str, list, None] = None,
                     chain_of_thought: bool = True,
                     ) -> BiniImage:

    bini = BiniImage(chain_of_thought=chain_of_thought)
    try:
        response = await bini.kickoff_async({'original_prompt': prompt, 'image': image, 'sample_image': sample_image})
        log.fire.info(f'Refined:, {bini.state.refined_prompt}')
        log.fire.info(f'Result:", {bini.state.result}')
        log.fire.info(f'Reflection:", {bini.state.reflection}')
        return response

    except Exception as e:
        log.fire.error(f'error! {e}')
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(bini_image(prompt="is cat displayed in this image?",
                           image=r"C:\Users\evgenyp\Bini\Bini\tests\data\img.png",
                           chain_of_thought=True))
