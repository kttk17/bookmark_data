#!/bin/bash
#userid_url_201903
eval "python3 data_re.py"
eval "rm data_re.py-e"

#userid_url_2019{04..09}
for i in {04..09}; do echo ${i}; done | while read l
do
  eval "sed -i -e 's/20190$(($l-1))/20190$l/g' data_re.py"
  eval "python3 data_re.py"
  eval "rm data_re.py-e"
done

#userid_url_201910
eval "sed -i -e 's/201909/201910/g' data_re.py"
eval "python3 data_re.py"
eval "rm data_re.py-e"

#userid_url_2019{11..12}
for i in {11..12}; do echo ${i}; done | while read l
do
  eval "sed -i -e 's/2019$(($l-1))/2019$l/g' data_re.py"
  eval "python3 data_re.py"
  eval "rm data_re.py-e"
done

#userid_url_202001
eval "sed -i -e 's/201912/202001/g' data_re.py"
eval "python3 data_re.py"
eval "rm data_re.py-e"

#userid_url_2020{02..07}
for i in {02..07}; do echo ${i}; done | while read m
do
  eval "sed -i -e 's/20200$(($m-1))/20200$m/g' data_re.py"
  eval "python3 data_re.py"
  eval "rm data_re.py-e"
done

eval "sed -i -e 's/202007/201903/g' data_re.py"
echo Finished!
