
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
    rows,columns = np.where(np.logical_and(data > begin , data <= end) )
    return data[rows].T[1]



def retrieve_perf(filename="rep.log", x={}): 
    with open(filename ,"r") as f :
        l=f.readlines() 
        # print(f.readlines())
        # return 
       
        x["energy_pkg"]=float(l[3].strip().split(" ")[0].replace(",",""))
        x["energy_core"]=float(l[4].strip().split(" ")[0].replace(",",""))
        x["energy_gpu"]=float(l[5].strip().split(" ")[0].replace(",",""))
        x["execution_time"]=float(l[7].strip().split(" ")[0].replace(",",""))
        return x 



def main():

    data = np.stack( [ extract(l) for l in sys.stdin ])
    begin=int(sys.argv[1]) *1000 # transform the data into ms 
    bfeore_begin=begin-snapbefore *1000 
    end=int(sys.argv[2]) *1000
    perf_file=sys.argv[3] if len(sys.argv[3])>3  else  "rep.log"
    results={}
    results["system_power"] = get_powers(data,bfeore_begin,begin).mean()*frequency
    results["program_power"] = get_powers(data,begin,end).mean()*frequency
    results["system_energy"] = results["system_power"]*(end-begin)/1000 #transform data into Joules
    results["program_energy"] = results["program_power"]*(end-begin)/1000 
    results["program_net_energy"] = results["program_energy"]-results["system_energy"]
    retrieve_perf(perf_file,results)
    return results
    print(results)


if __name__=="__main__" : 
    res=main()
    print(tabulate([res.values()],res.keys(),tablefmt="grid"))