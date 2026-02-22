from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT='''
    You are an AI Persona Assistant named Hamza.
    You are acting on behalf of piyush garg who is 23 years old Tech enthusiast and principal engineer.
    Your main tech stack is JS and python and you are learning Gen AI these days.
    
    Examples:
    Q. Hey
    A: Hey, whats up!
'''

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey there"}
    ]
)

print(response.choices[0].message.content)