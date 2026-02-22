import time
import threading

def monitor_tea_temp():
    while True:
        print(f'Monitoring tea temperature...')
        time.sleep(2)
        

t = threading.Thread(target=monitor_tea_temp)
t.start()

# thread keeps on running even if the main thread is executed