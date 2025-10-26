class AgentBase:
    def __init__(self, llm):
        self.llm = llm

    def invoke(self, query: str):
        raise NotImplementedError("Subclasses must implement the invoke method")
