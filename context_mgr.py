class GenContextManager(object):
    def __init__(self, func_gen, *args, **kwargs):
        self.gen = func_gen(*args, **kwargs)
        
    def __enter__(self):
        try:
            v = next(self.gen)
            return v
        except StopIteration:
            return
        else:
            raise RuntimeError("Generator threw exception on yield")
        return
    
    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                next(self.gen)
            except StopIteration:
                return
            else:
                raise RuntimeError("Generator failed to terminate")
        else:
            if value is None:
                value = type()
            #This is not enough...
            #Few more exceptions to be handled
            self.gen.throw(type, value, traceback)
            
        pass

def file_op_ctx(file_op_gen_func):
    def inner(*args, **kwargs):
        return GenContextManager(file_op_gen_func, *args, **kwargs)
    
    return inner

@file_op_ctx
def file_op(file_path):
    fd = open(file_path, 'w')
    yield fd
    print ("Closing file")
    fd.close()


with file_op("test.txt") as fd:
    print ("huh??")
