from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBF1nvNiI-yfCLxYoYvwwBn5YcE8oyWwhE"
# Validate API key
google_key = os.environ.get('GOOGLE_API_KEY')
if not google_key:
	raise SystemExit('GOOGLE_API_KEY not found in environment. Add it to your .env file.')


model = ChatGoogleGenerativeAI(model='gemini-flash-latest', temperature = 0.5)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

# Checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)









