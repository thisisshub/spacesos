from pydantic_ai import Agent, RunContext
from pydantic_ai.models.vertexai import VertexAIModel

model = VertexAIModel("gemini-1.5-flash")
agent = Agent(model)