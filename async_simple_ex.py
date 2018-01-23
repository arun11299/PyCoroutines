import asyncio


@asyncio.coroutine
def coroutine():
    print('in coroutine')
    #yield 5

def task1():
    print ("task1 executed")


event_loop = asyncio.get_event_loop()

try:
    print('starting coroutine')
    coro = coroutine()
    print('entering event loop')
    event_loop.run_until_complete(coro)
    event_loop.call_soon(task1)
    event_loop._run_once()
finally:
    print('closing event loop')
    event_loop.close()
