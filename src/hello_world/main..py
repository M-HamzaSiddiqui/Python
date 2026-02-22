from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system", "content": "You will only answer questions related to politics in few words. If it's about something else just give a sorry message."},
        {"role": "user", "content": "what is the formula of hypotenuse. Who is president of uae?"}
    ]
)

print(response.choices[0].message.content)