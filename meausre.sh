#! /bin/bash 
snapbefore=10
frequency=10
log_perf='.perfi.log'

begin=$(date +%s)

perf stat -a -r 1     -e "power/energy-pkg/"     -e "power/energy-cores/" -e "power/energy-gpu/" $@ 2> $log_perf 

end=$(date +%s)
max_lines=$(((end - begin+snapbefore+100)*frequency ))
tail -n $max_lines /tmp/powerapi-sensor-reporting/watcher/rapl | awk -F ',' '{if  ($5 == 0)  print $1,$6}' | python averageenergy.py $begin $end $log_perf 
rm -f $log_perf