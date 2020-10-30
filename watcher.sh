#! /bin/sh

exp_name=watcher 
docker run --net=host --privileged --name powerapi-$exp_name --rm  -d            -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro            -v /tmp/powerapi-sensor-reporting/$exp_name:/reporting/   powerapi/hwpc-sensor:latest   -f 100         -n machine           -s rapl -e RAPL_ENERGY_PKG            -r csv -U /reporting/

