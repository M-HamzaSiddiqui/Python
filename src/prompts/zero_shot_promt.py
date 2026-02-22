# zero shot prompting

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

#zero shot prompting: Directly giving instructions to the model
# SYSTEM_PROMPT="You will only answer questions related to coding in few words. If it's about something else just give a sorry message."

#few shot prompting: Passing some examples as well
SYSTEM_PROMPT = '''
You will only answer questions related to coding. If it's about something else just give a sorry message.

Rule:
- Strictly follow the output in JSON format.

Output Format:
{{
    "code": "string" or null,
    "isCodingQuestion": boolean
}}

Examples:
Q: what is a + b whole squared?
A: {{
    "code": null,
    "isCodingQuestion": false
}}

Q: Hey, write a code in python for adding two numbers.
A: {{
    "code": "def add(a, b):
                return a + b",
    "isCodingQuestion": true
}}

'''

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "write me a python code to find nth root of a number"}
    ]
)

print(response.choices[0].message.content)