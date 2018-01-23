
# coding: utf-8

# In[11]:


import threading
import time


# Future states:
# 
# An instance of the future could be in any of these states.
# 1. PENDING : The future does not have the result/exception for the corresponding work.
# 2. RUNNING : TBD
# 3. CANCELLED : The future got cancelled before the result of the associated work was computed.
# 4. FINISHED : The associated work got finished and resulted in giving out a value or exception.

# In[12]:



PENDING   = 'pending'
RUNNING   = 'running'
CANCELLED = 'cancelled'
FINISHED  = 'finished'

FUTURE_STATES = [
    PENDING,
    RUNNING,
    CANCELLED,
    FINISHED
]


# In[13]:


class FutureCancelledError(Exception):
    """"""
    def __init__(self):
        pass


class FutureTimeoutError(Exception):
    """"""
    def __init__(self):
        pass
        


# In[14]:


class Future(object):
    """
    This revision of the Future class integrates with
    the task loop.
    """
    def __init__(self, loop):
        """"""
        self._loop = loop
        self._state = PENDING
        self._condition = threading.Condition()
        self._done_callbacks = []
        
        self._result = None
        self._exception = None
    
    def add_done_callback(self, cb):
        """
        Add the callback to be executed when the future state becomes 
        cancelled/finished
        """
        with self._condition:
            if self._state not in [CANCELLED, FINISHED]:
                self._done_callbacks.append(cb)
                return
        #Call immediately if result/exception already set
        cb(self)
    
    
    def result(self, timeout=None):
        """
        Blocking call on the calling thread.
        
        timeout: time to wait for the result to be ready.
        
        Throws:
        FutureCancelledError if the state of future was CANCELLED
        or became CANCELLED later.
        
        FutureTimeoutError if future did not become ready before
        the timeout.
        """
        with self._condition:
            if self._state in [CANCELLED]:
                raise FutureCancelledError()
            
            if self._state == FINISHED:
                # Already done, return the result
                return self._result
            
            self._condition.wait(timeout)
            
            if self._state in [CANCELLED]:
                raise FutureCancelledError()
            
            if self._state == FINISHED:
                return self._result
            else:
                return FutureTimeoutError()
        pass
        
    def exception(self, timeout=None):
        """
        Blocking call on the calling thread.
        """
        with self._condition:
            if self._state in [CANCELLED]:
                raise FutureCancelledError()
            
            if self._state == FINISHED:
                #Already done. Return the exception
                return self._exception
            
            self._condition.wait(timeout)
            
            if self._state in [CANCELLED]:
                raise FutureCancelledError()
            
            if self._state == FINISHED:
                return self._exception
            else:
                raise FutureTimeoutError()
            
             
    def done(self):
        """Future is finished"""
        with self._condition:
            return self._state in [CANCELLED, FINISHED]
        
    def cancelled(self):
        """ Is the future cancelled or not"""
        with self._condition:
            return self._state == CANCELLED
    
    def cancel(self):
        """Cancel the future if not already finished or running"""
        with self._condition:
            if self._state in [RUNNING, FINISHED]:
                return False
            self._set_state(CANCELLED)
            
            self._condition.notify_all()
        
        self._execute_done_callbacks()
        return True
        
    def set_result(self, result):
        """
        Sets the result of the work associated with this future.
        """
        with self._condition:
            self._result = result
            self._state = FINISHED
            
            self._condition.notify_all()
        
        self._execute_done_callbacks()
            
        
    def set_exception(self, exp):
        """
        Sets the exception that occurred while performing
        the work associated with this future.
        """
        with self._condition:
            self._exception = exp
            self._state = FINISHED
            
            self._condition.notify_all()
        
        self._execute_done_callbacks()
    
    def _set_state(self, state):
        """
        Sets the state.
        Assumes that lock is taken
        """
        self._state = state
        
    def _execute_done_callbacks(self):
        for cb in self._done_callbacks:
            try:
                cb(self)
            except Exception as e:
                print ("ERROR: {}".format(str(e)))
                raise e

    def __iter__(self):
        """
        This future is an iterable now.
        """
        if not self.done():
            yield self

        return self.result()


# Lets write some tests to check our future in action

# In[15]:


def bg_task():
    print ("Background task started")
    time.sleep(10)
    print ("Background task finished")
    return 42


# In[16]:


class ThreadedExecutor(object):
    def __init__(self):
        self._thread = threading.Thread(target=self._runner)
    
    def submit(self, task, *args, **kwargs):
        """"""
        f = Future()
        t = threading.Thread(target=self._runner, args=(f, task, args, kwargs,))
        t.start()
        return f
        
    def _runner(self, fut, task, args, kwargs):
        v = task(*args, **kwargs)
        fut.set_result(v)
        pass


# In[17]:

if __name__ == "__main__":
    f = ThreadedExecutor().submit(bg_task)
    f.result()

