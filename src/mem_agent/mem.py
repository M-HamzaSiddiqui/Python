import os
from mem0 import Memory
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4.1"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

mem_client = Memory.from_config(config)

chat_history = []

while True:
    

    user_query = input("> ")
    
    search_memory = mem_client.search(
        query=user_query,
        user_id="hamza"
    )
    
    chat_history.append({"role": "user", "content": user_query})
    
    chat_history = chat_history[-5:]
    
    
    user_memory = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" for mem in search_memory.get("results")
    ]
    
    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(user_memory)}
    """
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *chat_history
        ]
    )
    
    ai_response = response.choices[0].message.content
    
    chat_history.append({"role": "assistant", "content": ai_response})
    
    print("AI", ai_response)
    
    mem_client.add(
        user_id="hamza",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )
    
    print("Memory has been saved...")
    
    