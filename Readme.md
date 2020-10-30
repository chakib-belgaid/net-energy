# Net energy consumption of program 

a script that will  use `powerapi/hwpc-sensor` to gather the average power into the  machine , and substruct it from the programs global energy conusmption 

# Steps 
- Launch `hwpc-sensor` with the `watcher.sh` 
- [optional] to avoid lack of space in the computer we create a cleaner that will delete the reporting file each day 

    1 - create the cleaner script and put it in `/opt/scripts/watcher.cleaner.sh` :
        the script will contain this instruction 

    echo "" >  /tmp/powerapi-sensor-reporting/watcher/rapl 

    2 - add it the a schedular using the command `crontab -e` 
     for this u need just to add his **absolute path** to the config file 

    3 - install perf 
    
    use the script `measure.sh` to measure the enregy of your work 

    ./measure.sh something 

<!-- tail -n 1000 /tmp/powerapi-sensor-reporting/watcher/rapl | awk -F ',' '{if  ($5 == 0)  print $1,$6}'  -->
