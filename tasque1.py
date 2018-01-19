import inspect
from collections import deque

from task import Task
from future import Future

class NotGenerator(Exception):
    """
    """
    pass

def task(func):
    """
    Wraps a function inside a Task object which
    is also a Future.
    The returned task can be passed on to the 
    task execution loop for completion.

    Users can add done callbacks to this task which would be called
    once the passed in function is completely executed.
    """
    def _wrap(*args, **kwargs):
        """
        """
        gen = func(*args, **kwargs)

        if inspect.isgenerator(gen):
            raise NotGenerator("{} does not return a generator".format(func.__name__))

        assert (gen is not None)

        t = Task(gen)
        return t
    
    return _wrap()


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


    def add_task(self, coro):
        """
        """
        pass

    def call_soon(self, cb, *args):
        """
        """
        pass
