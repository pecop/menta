# STEP1
import time
import threading

def func1():
    for i in range(5):
        print("func1")
        time.sleep(1)

def func2():
    for i in range(5):
        print("func2")
        time.sleep(1)

def main():
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)

    thread_1.start()
    thread_2.start()

    # STEP2
    thread_list = threading.enumerate()
    thread_list.remove(threading.main_thread())
    for thread in thread_list:
        thread.join()
 
    print("All thread is ended.")

if __name__ == "__main__":
    main()
