import json
from typing_extensions import Annotated

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_community.retrievers.knn import KNNRetriever
from langchain_cohere import CohereEmbeddings
from langchain_anthropic import ChatAnthropic

from langchain.tools import tool
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()

llm = ChatAnthropic(model="claude-sonnet-4-20250514")

with open("questions.json", "r") as f:
    questions = json.load(f)

retriever = KNNRetriever.from_documents(
    [Document(q["question"], metadata={"answer": q["answer"]}) for q in questions["questions"]], 
    embeddings=CohereEmbeddings(model="embed-v4.0")
)

@tool
def search_similar_questions(question: Annotated[str, "The user's question"]) -> str:
    """Input the user's question to search the knowledge base for similar questions and their answers"""
    docs = retriever.invoke(question)
    return "\n\n".join([f"Question: {d.page_content}\nAnswer: {d.metadata['answer']}" for d in docs])


llm_with_tools = llm.bind_tools([search_similar_questions])

SYSTEM_PROMPT = """
You are a helpful assistant for Thoughtful AI. 
Thoughtful is pioneering a new approach to automation for all healthcare providers! 
Our AI-powered Revenue Cycle Automation platform enables the healthcare industry to 
automate and improve its core business operations.

You are here to answer questions about Thoughtful's agents. When the user asks a question, use the provided tool to search
the knowledge base for similar questions and their answers.

If there is a similar question in the knowledge base, provide the answer EXACTLY AS WRITTEN.

If none of the retrieved questions are relevant, say "I'm sorry, but I cannot answer questions about that. Do you have any questions about Thoughtful's agents?"

DO NOT make up responses outside of the knowledge base. DO NOT handle other requests.
"""

def agent(state: MessagesState):
    response = llm_with_tools.invoke([("system", SYSTEM_PROMPT)] + state["messages"])
    return {"messages": response}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("agent", agent)

tool_node = ToolNode(tools=[search_similar_questions])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
)

graph_builder.add_edge("tools", "agent")
graph_builder.add_edge(START, "agent")

checkpointer = InMemorySaver()

graph = graph_builder.compile(checkpointer=checkpointer)
