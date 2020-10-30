
import numpy as np 
import sys 
import math 
from tabulate import tabulate  
snapbefore=10 ## means 10 secs 
frequency=10

def extract(l):
    k=l.strip().split(" ")
    return  (int(k[0]),math.ldexp(int(k[1]),-32) )
    

def get_powers(data,begin,end) : 
    rows,columns = np.where(np.logical_and(data > begin , data < end) )
    return data[rows].T[1]



def retrieve_perf(filename=".perfi.log", res={}): 
    with open(filename ,"r") as f :
        # l=f.readlines() 
        l=[l.strip()for l in f if l.strip()]
        for measure in l[1:-1]:
            x=measure.split()
            res[x[2][6:-1]]=float(x[0].replace(",","")) # remove the world power 

        res["execution-time"]=float(l[-1].split(" ")[0].replace(",",""))
        return res



def main():

    data = np.stack( [ extract(l) for l in sys.stdin ])
    begin=int(sys.argv[1]) *1000 # transform the data into ms 
    before_begin=begin - snapbefore *1000 
    end=int(sys.argv[2]) *1000
    perf_file=sys.argv[3] if len(sys.argv[3])>3  else  "rep.log"
    results={}
    results["av-system-power"] = get_powers(data,before_begin,begin).mean()*frequency
    results["av-program-power"] = get_powers(data,begin,end).mean()*frequency
    results["system-energy"] = results["av-system-power"]*(end-begin)/1000 #transform data into Joules
    results["program-energy"] = results["av-program-power"]*(end-begin)/1000 
    results["program-net-energy"] = results["program-energy"]-results["system-energy"]
    retrieve_perf(perf_file,results)
    return results
    print(results)


if __name__=="__main__" : 
    res=main()
    print(tabulate([res.values()],res.keys(),tablefmt="fancy_grid"))