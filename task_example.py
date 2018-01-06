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

def compute(x, y):
    return x + y

def perform_async_task():
    result = yield ThreadedExecutor().submit(my_long_running_task)
    print ("Gotcha {}".format(result))
    return result

def do_after(delay, gen):
    yield ThreadedExecutor().submit(time.sleep, 3)
    yield gen


def do_after_fixed(delay, gen):
    yield ThreadedExecutor().submit(time.sleep, 3)
    yield from gen

if __name__ == "__main__":
    #t = Task(perform_async_task())
    #t.step()


    """
    Well this is cool!! We have used the generator to split the function at the 'yield' statement
    and get control over what can be returned by it by making use of gen.send.
    
    But there is one problem with this kind of structure. 
    a) Cant get the result out from the task
    b) What about chaining generators ?
       Lets see below example:
    """
    #Task(do_after(3, perform_async_task())).step()

    """
    For ^^^^^ we get below error:
        ERROR: 'generator' object has no attribute 'add_done_callback'
        Check out the task code snippet:
            try:
                if exp:
                    self.gen.throw(exp)
                else:
                    fut = self.gen.send(snd_val)
                    fut.add_done_callback(self._fut_done_cb) <<<<------

            except StopIteration:
                return 

        In our previous example "self.gen.send" on its second run threw StopIteration
        exception. But in this case, it did not as we had another yield statement following.
        The second yield gives a generator which has no 'add_done_callback' method obviously
        because its not a future object.
    """

    """
    Fix the above problem using "yield from".
    "yield from" works on an iterable object only.
    """
    Task(do_after_fixed(3, perform_async_task())).step()

