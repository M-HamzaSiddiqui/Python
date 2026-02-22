orders = ["masala", "ginger"]

try:
    print(orders[2])
except IndexError as e:
    print(e)
    
# print(orders[2]) 