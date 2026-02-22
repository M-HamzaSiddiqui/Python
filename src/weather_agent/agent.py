from openai import OpenAI
from dotenv import load_dotenv
import requests
from pydantic import BaseModel, Field
from typing import Optional
import json
import os

load_dotenv()

client = OpenAI()

class MyOutputFormat(BaseModel):
    step: str = Field(..., description = "The ID of the step. Example: PLAN, OUTPUT, TOOL, etc.")
    content: Optional[str] = Field(None, description="The optional string content for the step.")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")
    
def run_cmd(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city):
    url = f'https://wttr.in/{city.lower()}?format=%C+%t'
    response = requests.get(url)
    
    if response.status_code == 200:
        return f'The weather in {city} is {response.text}'
    else:
        return "Something went wrong"
    
availabe_tools = {
    "get_weather": get_weather,
    "run_cmd": run_cmd
}


SYSTEM_PROMPT = """
    You are a expert AI assistant in resolving user queries using chain of thought.
    You work on START, PLAN AND OUTPUT steps.
    You need to first plan what needs to be done. The plan can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the available list of tools.
    For every tool call wait for the observe step which is the output from the called tool.
    
    Rules:
    - Strictly follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (that can be multiple times), TOOL (when a tool is to be used), OBSERVE (get output of that tool) and finally OUTPUT (which is going to be displayed to the user).
    
    Output JSON format:
    {
        "step": "START" | "PLAN" | "OUTPUT" | "TOOL",
        "content": string,
        "tool": "string",
        "input": "string"
    }
    
    Available Tools:
    - get_weather(city: str): Takes city name as an input string and returns the weather information about the city.
    -run_cmd(cmd: str): Takes a windows system command as string and executes the command on user's system and returns the output from that command.
    
    Example1: 
    START: Hey, can you write a code to solve 2+3*5/10
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in maths problem."}
    PLAN: {"step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method."}
    PLAN: {"step": "PLAN", "content": "Yes, The BODMAS is the correct thing to do here."}
    PLAN: {"step": "PLAN", "content": "First we should divide 5 by 10 which is 0.5"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2+3*0.5."}
    PLAN: {"step": "PLAN", "content": "Now we should multiply 3 and 0.5 which is 1.5."}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 1.5."}
    PLAN: {"step": "PLAN", "content": "Now we should add 1.5 to 2 which is 3.5."}
    PLAN: {"step": "PLAN", "content": "Great, finally we have solved the equation and left with 3.5 as answer."}
    OUTPUT: {"step": "OUTPUT", "content": "3.5"}
    
    Example2: 
    START: What is the weather of Delhi?
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in getting weather of Delhi in India."}
    PLAN: {"step": "PLAN", "content": "Let's see we have any available tool from the list of available tools."}
    PLAN: {"step": "PLAN", "content": "Great, we have get_weather tool available for this query."}
    PLAN: {"step": "PLAN", "content": "I need to call get_weather tool for delhi as input for city."}
    PLAN: {"step": "TOOL", "tool": "get_weather", "input": "delhi"}
    PLAN: {"step": "OBSERVE", "tool": "get_weather", "output": "The weather of delhi is cloudy with 20 C"}
    PLAN: {"step": "PLAN", "content": "Great, I got the weather info about delhi."}
    OUTPUT: {"step": "OUTPUT", "content": "The current weather in delhi is 20 C with some clouds in sky."}
"""

print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_query = input("Enter you query: ")

message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.parse(
    model="gpt-4o-mini",
    response_format=MyOutputFormat,
    messages=message_history
    )
    
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    
    parsed_result = response.choices[0].message.parsed
    
    if parsed_result.step == "START":
        print("Starting to think!", parsed_result.content)
        continue
    if parsed_result.step == "PLAN":
        print('🧠', parsed_result.content)
        continue
    if parsed_result.step == "TOOL":
        tool = parsed_result.tool
        tool_input = parsed_result.input
        print(f'🔨:  {tool} ({tool_input})')
        
        tool_response = availabe_tools[tool](tool_input)
        
        message_history.append({"role": "developer", "content": json.dumps(
            {"step": "OBSERVE", "tool": tool, "input": tool_input, "output": tool_response}
        )})
        
        continue
        
    if parsed_result.step == "OUTPUT":
        print('🤖', parsed_result.content)
        break
    
print("\n\n\n")