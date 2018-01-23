
class Handle(object):
    """
    A wrapper for holding a callback and the
    arguments it takes.
    """
    def __init__(self, fn, loop, args):
        """
        Constructor.
        Arguments:
            fn   : The callback function. Has to be a regular function.
            loop : The loop which would call the handler.
            args : The argument pack the callback expects.
        """
        self._cb = fn
        self._args = args
        self._loop = loop
        #Set to true if the handler is cancelled
        #Cancelled handlers are not executed by the loop
        self._cancelled = False
        #Set to true if the handler has finished execution
        self._finished = False

    def __call__(self):
        """
        The function call operator.
        """
        assert self._finished == False
        try:
            self._cb(*self._args)
        except Exception as e:
            self._finished = True
            raise e

    def cancel(self):
        """
        Cancel the handle
        """
        assert self._cancelled == False
        if not self._finished:
            self._cancelled = True
        return

    def is_cancelled(self):
        """
        """
        return self._cancelled
