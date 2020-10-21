#!/bin/bash

for i in {4..12}; do echo ${i}; done | while read l
do
	if [ $l -lt 10 ]; then
		eval "python3 url_count.py"
		eval "sed -i -e 's/20190$((l-1))/20190$l/g' url_count.py"
	elif [ $l = 10 ]; then
		eval "python3 url_count.py"
		eval "sed -i -e 's/201909/201910/g' url_count.py"
		eval "python3 url_count.py"
	else
		eval "sed -i -e 's/2019$((l-1))/2019$l/g' url_count.py"
		eval "python3 url_count.py"
	fi
done
eval "sed -i -e 's/201912/202001/g' url_count.py"
eval "python3 url_count.py"
for j in {2..7}; do echo ${j}; done | while read m
do
	eval "sed -i -e 's/20200$((m-1))/20200$m/g' url_count.py"
	eval "python3 url_count.py"
done
eval "sed -i -e 's/202007/201903/g' url_count.py"
echo Finished!!
