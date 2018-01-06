import time
import future
from future import Future
from future import ThreadedExecutor

import task
from task import Task

"""
What we want is not to keep polling futures done method or get blocked while calling the result method. Neither do we want the callback based approach in our code. We want to make the code look as much synchronous as possible.
Something like below....
"""

def my_long_running_task(work_load=2):
    print ("Work started")
    time.sleep(work_load)
    print ("Done work_load")
    #Calculated result after so much effort
    return 42

def perform_async_task():
    result = yield ThreadedExecutor().submit(my_long_running_task)
    print ("Gotcha {}".format(result))
    return result

if __name__ == "__main__":
    t = Task(perform_async_task())
    t.step()

