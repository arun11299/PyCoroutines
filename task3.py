
# coding: utf-8

# In[1]:


import future
from future import Future


# In[2]:


class Task(Future):
    """
    Wraps a generator yielding a Future
    object and abstracts away the handling of future API

    This version adds loop to the task
    """
    def __init__(self, loop, gen):
        """
        """
        super().__init__(loop)
        assert (loop is not None)
        self._loop = loop
        self.gen = gen
        self._loop.call_soon(self.step)
    
    def step(self, snd_val=None, exp=None):
        """"""
        try:
            if exp:
                self.gen.throw(exp)
            else:
                fut = self.gen.send(snd_val)

        except StopIteration as e:
            self.set_result(snd_val)
        except Exception as e:
            self.set_exception(e)

        else:
            #if no exceptions, we need to check what kind
            #of generator function we are dealing with
            #Why ? Because not all generator functions would
            #yield a future.
            if isinstance(fut, Future):
                fut.add_done_callback(self._fut_done_cb)

            elif fut is None:
                #The generator yielded noting or None
                #so we call step again for finishing off
                #the generator execution till the return statement
                #or to the next yield statement
                self._loop.call_soon(self.step)
        
    def _fut_done_cb(self, fut):
        """
        Called if the yielded future by the coroutine
        is ready
        """
        try:
            result = fut.result()

        except Exception as e:
            self.step(None, e)
        else:
            #Call the step again to continue
            #with the coroutine execution.
            self.step(result, None)
        pass


