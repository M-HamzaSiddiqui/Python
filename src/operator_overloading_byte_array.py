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

# generator

prices = [10, 212, 38, 5, 6, 92, 9, 93, 12]

sum_price_above_12 = sum(price for price in prices if price > 12) #this is very memory efficient method to make generators in such cases

print(sum_price_above_12)

# generators with yeild in python

def nums():
    nums = [1, 2, 3]
    for num in nums:
        yield num

numbers = nums()
print(numbers)
# for num in numbers:
#     print(num)
        
        
print(next(numbers))
print(next(numbers))


# infinite generators

def infinite_series():
    count = 1
    while True:
        yield count
        count += 1

series = infinite_series()

for _ in range(5):
    print(next(series))
    

def input_generater():
    num = yield
    
    while True:
        print("current yeild", num)
        num = yield
        
        
generator = input_generater()

next(generator)
generator.send(2)
generator.send(3)
generator.send(4)

generator.close()

# always close a generator

# decorators 

def my_decorator(func):
    
    def wrapper():
        print("before running the function")
        func()
        print("after running the function")
    
    return wrapper

@my_decorator
def greet():
    print("hello, how ary you?")
    
greet()

from functools import wraps

def log_activity(func):
    @wraps(func)
    
    def wrapper(*args, **kwargs):
        print(f'calling {func.__name__}')
        result = func(*args, **kwargs)
        print(f'calling {func.__name__}')
        return result

    return wrapper


@log_activity
def brew_chai(type):
    print(f'brewing {type} chai')
    

brew_chai("masala")

from functools import wraps

def require_admin(func):

    @wraps(func)
    def wrapper(user_role):
        if user_role != 'admin':
            print("unauthorized")
            return None
        else: 
            return func(user_role)
    
    return wrapper

@require_admin
def access_tea_inventory(role):
    print("Access granted to tea inventory")
    

access_tea_inventory("user")
access_tea_inventory("admin")
        
        
        

    
        


