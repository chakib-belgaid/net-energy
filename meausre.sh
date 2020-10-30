#! /bin/bash 
snapbefore=10
frequency=10
log_perf='.perfi.log'
cpus_count=`grep -c ^processor /proc/cpuinfo `
perf_devices=`perf list | egrep power  | awk -F " " '{print "-e " $1 }'` 
begin=$(date +%s)

perf stat -a -r 1    $perf_devices $@ 2> $log_perf 

end=$(date +%s)
max_lines=$(((end - begin+snapbefore+30)*frequency*cpus_count ))
tail -n $max_lines /tmp/powerapi-sensor-reporting/watcher/rapl | awk -F ',' '{if  ($4 == 0 && $5 == 0)  print $1,$6}' | python averageenergy.py $begin $end $log_perf 
rm -f $log_perf

#ps we count only cpu 0