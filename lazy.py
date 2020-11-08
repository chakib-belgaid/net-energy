import time
import signal
import psutil
import os
import multiprocessing
import functools


def lazy(_func=None, *, affinity=None, charge=100):
    """
    Reduce the workload of a job to [charge] % and set it to the core [affinity]
    """
    def decorator_lazy(worker):
        @functools.wraps(worker)
        def wrapper_lazy(*args, **kwargs):
            sleep_duration = charge / 10000
            pause_duration = 0.0099 - sleep_duration
            process = multiprocessing.Process(target=worker,
                                              args=args,
                                              kwargs=kwargs)
            if affinity is not None:
                if type(affinity) != list:
                    myaffinity = [affinity]
                psutil.Process(process.pid).cpu_affinity(myaffinity)
                psutil.Process(os.getpid()).cpu_affinity(myaffinity)

            if charge == 100:
                worker(*args, **kwargs)
                return
            if charge == 0:
                exit()
            process.start()
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
