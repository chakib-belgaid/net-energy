import time
import signal
import psutil
import os
import multiprocessing
import functools

def lazy(_func=None, *, affinity=0, charge=100):
    """
    Reduce the workload of a job to [charge] % and set it to the core [affinity]
    """
    if type(affinity) != list:
        affinity = [affinity]

    def decorator_lazy(worker):
        @functools.wraps(worker)
        def wrapper_lazy(*args, **kwargs):

            psutil.Process(os.getpid()).cpu_affinity(affinity)
            if charge == 100:
                worker()
                return

            sleep_duration = charge / 10000
            pause_duration = 0.0099 - sleep_duration
            process = multiprocessing.Process(target=worker)
            process.start()
            psutil.Process(process.pid).cpu_affinity(affinity)
            while process.is_alive():
                os.kill(process.pid, signal.SIGSTOP)
                time.sleep(pause_duration)
                os.kill(process.pid, signal.SIGCONT)
                time.sleep(sleep_duration)
            return

        return wrapper_lazy

    if _func is None:
        return decorator_lazy
    else:
        return decorator_lazy(_func)

