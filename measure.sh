#! /bin/bash 
sleep_duration=5
log_perf='.perfi.log'
cpus_count=`grep -c ^processor /proc/cpuinfo `

perf_devices=`perf list | egrep power/  | awk -F " " '{print "-e " $1 }'` 
sleep $sleep_duration
begin=$(date +%s)
perf stat -a -r 1    $perf_devices $@ 2> $log_perf 
end=$(date +%s)
snapbefore=$((begin-sleep_duration))
beginline=`fgrep $snapbefore -n /tmp/powerapi-sensor-reporting/watcher/rapl| head -n 1  | awk  -F  ':'   '{print $1}' `
tail -n +$beginline /tmp/powerapi-sensor-reporting/watcher/rapl | python3 averageenergy.py $begin $end $snapbefore $log_perf 
rm -f $log_perf

#ps we count only cpu 0
