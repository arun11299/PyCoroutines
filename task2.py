
# coding: utf-8

# In[1]:


import future
from future import Future


# In[2]:


class Task(Future):
    """
    Wraps a generator yielding a Future
    object and abstracts away the handling of future API
    """
    def __init__(self, gen):
        super().__init__()
        self.gen = gen
    
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
        
    def _fut_done_cb(self, fut):
        try:
            result = fut.result()
            self.step(result, None)
        except Exception as e:
            self.step(None, e)
        pass


