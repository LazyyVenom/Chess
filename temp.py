import threading
import queue

stop_event = threading.Event()

def th(i, result_queue):
    if stop_event.is_set():
        return
    
    result = i * 2
    
    if result == 10:
        stop_event.set()
    
    if not stop_event.is_set():
        result_queue.put(result)

threads = []
results = queue.Queue()

for i in range(10):
    thread = threading.Thread(target=th, args=(i, results))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

while not results.empty():
    result = results.get()
    print(result)
