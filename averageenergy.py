import numpy as np
import pandas as pd
import sys
import math
from tabulate import tabulate
snapbefore = 10  ## means 10 secs
frequency = 10


def get_headers():
    with open("/tmp/powerapi-sensor-reporting/watcher/rapl") as f:
        headers = f.readline().strip()
    return (headers)


def get_mean_power(data, begin, end, frequency):
    x = data.loc[np.where(
        np.logical_and(data["timestamp"] > begin,
                       data["timestamp"] < end))].drop([
                           "timestamp", "sensor", "target", "cpu",
                           "time_enabled", "time_running"
                       ],
                                                       axis=1)
    x = x.groupby(["socket"]).mean() / 2**32 * frequency
    x = x.rename(columns=lambda x: x.replace("RAPL_ENERGY_", ""))
    return x


def retrieve_perf(filename=".perfi.log", res={}):
    with open(filename, "r") as f:
        # l=f.readlines()
        data = [data.strip() for data in f if data.strip()]
        for measure in data[1:-1]:
            x = measure.split()
            res[x[2][6:-1]] = float(x[0].replace(",",
                                                 ""))  # remove the world power

        res["execution-time"] = float(data[-1].split(" ")[0].replace(",", ""))
        return res


def main():
    headers = get_headers()
    pd.options.display.float_format = '{:.2f}'.format
    data = pd.read_csv(sys.stdin, names=headers.split(","), sep=",").dropna()

    # data = np.stack([extract(l) for l in sys.stdin])
    begin = int(sys.argv[1]) * 1000  # transform the data into ms
    end = int(sys.argv[2]) * 1000
    before_begin = int(sys.argv[3]) * 1000
    perf_file = sys.argv[4] if len(sys.argv[3]) > 3 else "rep.log"
    results = {}
    results["av-system-power"] = get_mean_power(data, before_begin, begin,
                                                frequency)
    results["av-program-power"] = get_mean_power(data, begin, end, frequency)
    results["system-energy"] = results["av-system-power"] * (
        end - begin) / 1000  #transform data into Joules
    results["program-energy"] = results["av-program-power"] * (end -
                                                               begin) / 1000
    results["program-net-energy"] = results["program-energy"] - results[
        "system-energy"]
    retrieve_perf(perf_file, results)
    return results


if __name__ == "__main__":
    res = main()
    res["av-system-power"] = res["av-system-power"].mean().to_string(
        dtype=False)
    res["av-program-power"] = res["av-program-power"].mean().to_string(
        dtype=False)
    res["system-energy"] = res["system-energy"].sum().to_string(dtype=False)
    res["program-energy"] = res["program-energy"].sum().to_string(dtype=False)
    res["program-net-energy"] = res["program-net-energy"].sum().to_string(
        dtype=False)
    print(
        tabulate([res.values()],
                 res.keys(),
                 tablefmt="fancy_grid",
                 colalign=["center"] * len(res)))
