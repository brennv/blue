from .logger import log
import time


def throttle(rate=0, calls=0, span=0, unit=1.0):   # unused
    """ Throttle function calls with a call rate limit, a total call limit
    and/or limit calls made over a total time span. Units in seconds. """
    if rate != 0:
        interval = unit / float(rate)
    if span != 0 and unit != 1.0:
        span *= unit

    def decorate(func):
        start = [time.time()]
        prior = [time.time()]
        count = [0]

        def wrapper(*args, **kargs):
            life = time.time() - start[0]
            if span == 0 or (span != 0 and life < span):
                if calls == 0 or (calls != 0 and count[0] < calls):
                    if rate != 0:
                        elapsed = time.time() - prior[0]
                        wait = interval - elapsed
                        if wait > 0:
                            time.sleep(wait)
                        prior[0] = time.time()
                    count[0] += 1
                    return func(*args, **kargs)
                else:
                    log.warning('Throttled call limit: %s' % calls)
                pass
            else:
                log.warning('Throttled call lifespan: %s' % span)
            pass
        return wrapper
    return decorate
