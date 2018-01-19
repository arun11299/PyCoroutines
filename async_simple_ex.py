import asyncio


@asyncio.coroutine
def coroutine():
    print('in coroutine')
    yield 5


event_loop = asyncio.get_event_loop()

try:
    print('starting coroutine')
    coro = coroutine()
    print('entering event loop')
    event_loop.run_until_complete(coro)
finally:
    print('closing event loop')
    event_loop.close()
