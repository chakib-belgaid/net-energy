import time
import sys
import signal
import psutil
import os
import multiprocessing
import functools


def lazy(_func=None, *, affinity=0, charge=100):
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


def watcher(affinity=None, charge=100):
    sleep_duration = charge / 10000
    pause_duration = 0.0099 - sleep_duration
    process = multiprocessing.Process(target=worker)
    if affinity is not None:
        if type(affinity) != list:
            myaffinity = [affinity]
        psutil.Process(process.pid).cpu_affinity(myaffinity)
        psutil.Process(os.getpid()).cpu_affinity(myaffinity)
    if charge == 100:
        worker()
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


def worker():
    i = 1
    j = 1
    while i + j >= 0:
        j = i + 1 % 13
        i = j + 2 % 7
    return i + j


def pinned_workers():

    charge = int(sys.argv[1])
    cpu_count = [int(i) for i in sys.argv[2:]]
    # loop , sleepduration = levels[int(argv[2])]
    for i in cpu_count:
        x = multiprocessing.Process(target=watcher, args=(i, charge))
        x.start()


def random_workers():

    charge = int(sys.argv[1])
    cpu_count = int(sys.argv[2])
    # loop , sleepduration = levels[int(argv[2])]
    for i in range(cpu_count):
        x = multiprocessing.Process(target=watcher, args=(None, charge))
        x.start()


if __name__ == "__main__":
    random_workers()
