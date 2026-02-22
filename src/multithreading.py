import time
import threading

def take_order():
    for i in range(4):
        print(f'taking order for {i} \n')
        time.sleep(2)
        
def make_chai():
    for flavor in ["masala", "ginger", "cinnamon"]:
        print(f'preparing {flavor} chai')
        time.sleep(4)
        
# create threadsṇ
order_thread = threading.Thread(target=take_order)
chai_thread = threading.Thread(target=make_chai)

order_thread.start()
chai_thread.start()

# wait for both to finish

order_thread.join()
chai_thread.join()

print("done")