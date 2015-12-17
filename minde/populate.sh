#!/bin/bash

DIR=data

if [ ! -d $DIR ]; then
    mkdir -p $DIR
fi

for i in {1..20}; do
    ecell3-session -e simulator.py 2>&1 > /dev/null
    sed -i -e "1s/\(.*\)/#\1/" IterateLog.csv
    fname=$(printf IterateLog.%03d.csv $i)
    mv IterateLog.csv $DIR/$fname
    echo "Generated $fname"
done
