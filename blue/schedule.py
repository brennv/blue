from .logger import log
import asyncio
import schedule


async def scheduler(function):
    schedule.every().hour.do(function)
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


def async_wrapper(target, *, loop=None):
    """Schedules target coroutine in the given event loop, otherwise *loop*
    defaults to the current thread's event loop. Returns the async task.
    """
    if asyncio.iscoroutine(target):
        return asyncio.ensure_future(target, loop=loop)
    raise TypeError("target must be a coroutine, not {!r}".format(type(target)))
