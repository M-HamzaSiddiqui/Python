from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

class State(TypedDict):
    messages: Annotated[list, add_messages]
    

def chatbot(state: State):
    print("\n\nINSIDE CHATBOT NODE", state)
    return {'messages': ["Hi, this is a message from Chatbot Node"]}

def sample_node(state: State):
    print("\n\nINSIDE SAMPLE NODE", state)
    return {'messages': ['Sample message appended']}
    
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample_node", sample_node)

graph_builder.add_edge(START, 'chatbot')
graph_builder.add_edge('chatbot', 'sample_node')
graph_builder.add_edge('sample_node', END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({'messages': ["Hi, My name is Hamza."]}))

print("\n\nupdated_state", updated_state)

