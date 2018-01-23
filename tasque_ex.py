import tasque
from tasque import transform_future
from tasque import TaskLoop
from tasque import NotGenerator
from tasque import NotRegularFunction

def task1():
    print ("Done with task1")

def my_gen():
    print ("Starting coro/gen my_gen")
    yield None
    print ("Finished coro/gen my_gen")

if __name__ == "__main__":
    print ("Starting test")
    print ("-------------")

    #Instantiate a run loop instance
    loop = TaskLoop()

    #Submit a task to the run loop
    loop.call_soon(task1)
    loop.run_once()

    #start a coroutine and finish it
    loop.run_until_complete(my_gen())

    #Stop the run loop
    loop.stop()
