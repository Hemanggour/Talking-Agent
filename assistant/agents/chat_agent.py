import uuid

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from assistant.config.settings import settings
from assistant.core.agent_base import AgentBase
from assistant.utils.prompts.system_prompts import CHAT_AGENT_PROMPT


class ChatAgent(AgentBase):
    def __init__(self):
        self.workflow = StateGraph(state_schema=MessagesState)

        self.llm = init_chat_model(
            model=settings.LANGUAGE_MODEL,
            model_provider=settings.LANGUAGE_MODEL_PROVIDER,
        )

        def call_model(state: MessagesState):
            response = self.llm.invoke(state["messages"])
            return {"messages": response}

        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", call_model)

        self.memory = MemorySaver()

        self.app = self.workflow.compile(checkpointer=self.memory)

        self.thread_id = uuid.uuid4()
        self.config = {"configurable": {"thread_id": self.thread_id}}

    def invoke(self, query: str):
        input_messages = [
            SystemMessage(content=CHAT_AGENT_PROMPT),
            HumanMessage(content=query),
        ]

        for event in self.app.stream(
            {"messages": input_messages}, self.config, stream_mode="values"
        ):

            response = event["messages"][-1]

        return response.content
