import inspect
from collections import deque

from task import Task
from future import Future

class NotGenerator(Exception):
    """
    """
    pass

def async_proc(supposed_future_coro, loop):
    """
    Loop works best with futures or with Tasks
    which wraps a generator object.
    So try to introspect the type of
    `supposed_future` argument and do the best 
    possible conversion of it.

    loop object is for creating the task so that it
    can add a callback.
    """
    if isinstance(supposed_future_coro, Future):
        """
        It is a future object. Nothing to do.
        """
        if loop != supposed_future_coro._loop:
            raise RuntimeError("loop provided is not equal to the loop of future")
        return supposed_future_coro
    elif inspect.isgenerator(supposed_future_coro):
        #Create a task object
        t = loop.add_task(supposed_future_coro)
        return t
    else:
        raise TypeError("Cannot create an asynchronous execution unit from the provided arg")

    assert (False and "Code Not Reached")
    return None




class StopLoopException(Exception):
    """
    If this exception is raised while the loop
    is processing the tasks, then it must close down.
    """
    pass


class TaskLoop(object):
    """
    """
    def __init__(self):
        self._ready = deque()
        self._loop_running = False
        pass

    def total_tasks(self):
        """
        """
        return len(self._ready)

    def run_forever(self):
        """
        """
        pass

    def run_until_complete(self, coro_or_future):
        """
        """
        is_fut = isinstance(coro_or_future, Future)
        pass


    def add_task(self, gen_obj):
        """
        Creates a task object and returns it
        """
        t = Task(self, gen_obj)
        return t

    def call_soon(self, cb, *args):
        """
        """
        pass
