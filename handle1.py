
class Handle(object):
    """
    """
    def __init__(self, fn, *args, loop):
        """
        """
        self._cb = cb
        self._args = args
        self._loop = loop
        self._cancelled = False
        self._finished = False

    def __call__(self):
        """
        """
        self._cb(self._args)
        self._finished = True
        pass

    def cancel(self):
        """
        """
        assert self._cancelled == False
        if not self._finished:
            self._cancelled = True
        return

    def is_cancelled(self):
        """
        """
        return self._cancelled
