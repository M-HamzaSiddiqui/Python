import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "hey there, my name is Hamza"

tokens = enc.encode(text)
print(tokens)

decoded = enc.decode([48467, 1354, 11, 922, 1308, 382, 20665, 2051])

print(decoded)