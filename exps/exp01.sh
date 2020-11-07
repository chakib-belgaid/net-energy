#! /bin/bash
# test the energy behaviour using different topologies 

counter()
{   s=0
    for i in $@ ;
    do
        s=$((s+1))
    done 
    echo $s
}


exp()
{
    charge=$1 
    shift
    echo $charge $@ 
    sleep 5
    cd ../
    python3 workers.py $charge $@  & 
    pid_workers=`echo $!`
    sleep 5 

    ./meausre.sh sleep 5 
    cd exps
    kill -9 $pid_workers 
    ps -au | egrep workers | awk  -F ' '  '{print $2}' |xargs -I@  kill -9 @ ;
}

 
for i in {1..10}
do 
    for charge in 0 15 30 50 75 100 ; 
    do  

        # physical cpu 0 
        list=`seq -s " " 0 2 18 `
         exp $charge $list

        # half pyscial half hyper thread cpu 0 
        list=`seq -s " " 0 4 38 `
        exp $charge $list

        # half physical cpu0 half pysical cpu 1 
        list=`seq -s " " 0 1 9 `
        exp $charge $list
    done 
done 
