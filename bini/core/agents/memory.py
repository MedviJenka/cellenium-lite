from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional,Never


class Memory(ABC):

    @abstractmethod
    def set_memory(self, *args: Optional[any], **kwargs: Optional[any]) -> Never:
        pass


@dataclass
class AgentMemory(Memory):

    """
    Why Does an Agent Need Memory?

    An agent in LangChain requires memory to store and retrieve information during decision-making.
    Memory is essential for maintaining context and recalling previous interactions, which is crucial for
     providing personalized and coherent responses.

    Here are a few reasons why an agent needs memory:

    Contextual Understanding: Memory helps an agent understand the context of a conversation.
    By storing previous messages or user inputs, the agent can refer back to them and provide
     more accurate and relevant responses. This ability to maintain a coherent conversation enhances the agent’s
      understanding of the user’s intent.

    Long-Term Knowledge: Memory enables an agent to accumulate knowledge over time. By storing information,
     the agent can build a knowledge base to answer questions or provide recommendations. This allows the agent
     to deliver more informed and accurate responses based on past interactions.

    Personalization: Memory allows an agent to personalize its responses based on the user’s preferences or history.
     By remembering previous interactions, the agent can tailor its responses to the specific
      needs or interests of the user. This enhances the user experience and makes the agent more
      effective in achieving its objectives.

    """

    storage: list = field(default_factory=list)

    def set_memory(self, *args: Optional[any], **kwargs: Optional[any]) -> Never:
        ...
