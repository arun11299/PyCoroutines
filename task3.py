
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
        super().__init__()
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
            fut.add_done_callback(self._fut_done_cb)

        except StopIteration as e:
            self.set_result(snd_val)
        except Exception as e:
            self.set_exception(e)
        
    def _fut_done_cb(self, fut):
        try:
            result = fut.result()
            self.step(result, None)
        except Exception as e:
            self.step(None, e)
        pass


