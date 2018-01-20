import inspect
from collections import deque

from task import Task
from future import Future
from handle import Handle

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
        #A deque of handles
        self._ready = deque()
        self._loop_running = False
        pass

    def total_tasks(self):
        """
        """
        return len(self._ready)

    def run_once(self):
        """
        Execute a task from the ready queue
        """
        if len(self._ready) == 0:
            #There are no tasks to be executed
            return

        hndl = self._ready.pop()
        #Call the handler which invokes the
        #wrapped function
        hndl()

    def run_forever(self):
        """
        """
        self._loop_running = True

        while True:
            try:
                self.run_once()
            except StopLoopException:
                break
            except Exception as e:
                print ("Error in run_forever: {}".format(str(e)))
        return 

    def run_until_complete(self, coro_or_future):
        """
        Run the event loop until the future
        is ready with result or exception.
        """

        if self._loop_running:
            raise RuntimeError("loop already running")

        task_or_fut = async_proc(coro_or_future, self)
        assert task_or_fut is not None

        is_new_task = not isinstance(task_or_fut, Future)
        #Add a callback to stop loop once the future is ready
        task_or_fut.add_done_callback(self._stop_loop)

        try:
            self.run_forever()
        except Exception as e:
            raise e

    def add_task(self, gen_obj):
        """
        Creates a task object and returns it
        """
        t = Task(self, gen_obj)
        return t

    def call_soon(self, cb, *args):
        """
        """
        hndl = Handle(cb, args)
        self._ready.append(hndl)
        return hndl

    def _stop_loop(self):
        """
        Raise the stop loop exception
        """
        raise StopLoopException("stop the loop")
