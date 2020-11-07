import asyncio
import sys
import time
from multiprocessing import Process
import psutil
from tabulate import tabulate
PKG0 = '/sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj'


def energy_recorder():
    energyfile = open(
        '/sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj', 'r')
    while True:
        x = float(energyfile.readline()[:-1])
        yield x
        energyfile.seek(0)


energy = energy_recorder()


def watcher():
    cpu_count = psutil.cpu_count()
    s = "power," + ",".join(["cpu_freq_" + str(i)
                             for i in range(cpu_count)]) + ","
    s += ",".join(["cpu_percent_" + str(i) for i in range(cpu_count)])
    s += ",package_0_temp," + \
        ",".join(["cpu_temp_"+str(i) for i in range(cpu_count//2)])
    s = s.split(",")
    # reporter.write(s)
    # with open(PKG0, 'r') as f:
    # old_energy = float(f.readline())
    old_energy = next(energy)
    old_time = time.time_ns()
    sleep_duration = 0.2
    while True:
        # f.seek(0)
        # new_energy = (float(f.readline()))
        new_energy = next(energy)
        new_time = time.time_ns()
        # convert from ns to us cause energy is in uj
        duration = (new_time - old_time) / 1000
        power = (new_energy - old_energy) / duration
        metrics = [power] + [i.current for i in psutil.cpu_freq(percpu=True)]
        # + psutil.cpu_percent(percpu=True) \

        # [i.current for i in psutil.sensors_temperatures()['coretemp']][0:cpu_count // 2 + 1]

        metrics = list(zip(s, metrics))
        print(tabulate(metrics))
        old_energy = new_energy
        old_time = new_time
        time.sleep(sleep_duration)


def lite_watcher():
    old_energy = next(energy)
    old_time = time.time_ns()
    sleep_duration = 0.2
    while True:
        # f.seek(0)
        # new_energy = (float(f.readline()))
        new_energy = next(energy)
        new_time = time.time_ns()
        duration = (new_time - old_time) / 1000
        power = (new_energy - old_energy) / duration
        print(power)
        old_energy = new_energy
        old_time = new_time
        time.sleep(sleep_duration)


def worker(n=3):
    res = 2
    for i in range(1 * 10**n):
        for _ in range(1000):
            res *= 2
        # time.sleep(0.2)
        for _ in range(1000):
            res *= 2
    return res


def main():
    watcher()
    # lite_watcher()


if __name__ == "__main__":
    main()
