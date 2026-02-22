from openai import OpenAI
from dotenv import load_dotenv

import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
    You are a expert AI assistant in resolving user queries using chain of thought.
    You work on START, PLAN AND OUTPUT steps.
    You need to first plan what needs to be done. The plan can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    
    Rules:
    - Strictly follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (that can be multiple times) and finally OUTPUT (which is going to be displayed to the user).
    
    Output JSON format:
    {
        "step": "START" | "PLAN" | "OUTPUT",
        "content": string
    }
    
    Example: 
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
"""

print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_query = input("Enter you query: ")

message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=message_history
    )
    
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result = json.loads(raw_result)
    
    if parsed_result.get("step") == "START":
        print("Starting to think!", parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "PLAN":
        print('🧠', parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "OUTPUT":
        print('🤖', parsed_result.get("content"))
        break
    
print("\n\n\n")
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {
#             "role": "user",
#             "content": "write me a python code to find nth root of a number",
#         },
#         # manually keep adding messages
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "START",
#                     "content": "User wants to write Python code to find the nth root of a number.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "PLAN",
#                     "content": "First, we need to understand how to calculate the nth root of a number mathematically, which can be done using exponentiation.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "PLAN",
#                     "content": "In Python, we can use the ** operator or the math module's pow function to compute the nth root.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "PLAN",
#                     "content": "Let's decide on the function signature, which should take two parameters: the base number and the root n.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "PLAN",
#                     "content": "The formula for finding the nth root can be expressed as: root = number ** (1/n). We can implement this into the function.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "PLAN",
#                     "content": "Next, I'll code a simple function that takes input for the number and the root, then returns the computed nth root.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "PLAN",
#                     "content": "I will now write the complete code to achieve this functionality.",
#                 }
#             ),
#         },
#     ],
# )

# print(response.choices[0].message.content)
