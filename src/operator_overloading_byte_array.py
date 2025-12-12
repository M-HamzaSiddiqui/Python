base = ['milk', 'water']
extra = ['ginger']

new_base = base + extra    

print(new_base) 

raw = bytearray(b'cinnamon')

print(raw)

#walrus operator

b = 21

if (remainder := b%2):
    print(f'remainder is {remainder}')
    
    
# non local searches just one scope above the current scope whereas global refers to the global scope