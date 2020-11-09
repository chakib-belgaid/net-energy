# Net energy consumption of program 

a script that will  use `powerapi/hwpc-sensor` to gather the average power into the  machine , and substruct it from the programs global energy conusmption 

# Steps 
 - install perf 
    
    sudo apt install linux-tools-common gawk

- install the required python libraries 

- Launch `hwpc-sensor` with the `watcher.sh`

-use the script `measure.sh` to measure the enregy of your work

-./measure.sh something 

## Remark 
To avoid lack of space in the computer we create a cleaner that will delete the reporting file each day 

1. create the cleaner script and put it in `/opt/scripts/watcher.cleaner.sh` :
    the script will contain this instruction 

    echo "" >  /tmp/powerapi-sensor-reporting/watcher/rapl 

2. add it the a schedular using the command `crontab -e` 
     for this u need just to add his **absolute path** to the config file 

## Workers  

In order to simulate real production environment we create a script that customise the worload of the cpu 

it accepts two parameters 
- the workload of the cpu , a value from 0-100 : 100 means 100% of the ressource 
- the number of threads to be used 

    python workers.py workload threads_counts 