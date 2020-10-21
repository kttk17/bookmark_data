#!/bin/bash
eval "./calc_similarity.sh"
for var in dice simpson
do
  echo "$var"
  eval "sed -i -e 's/jaccard/$var/g' calc_similarity.sh"
  eval "./calc_similarity.sh"
done
eval "sed -i -e 's/simpson/jaccard/g' calc_similarity.sh"
#eval "sed -i -e 's/userid_url_/userid_url_only_bookmark_/g' calc_similarity.sh"
#eval "./calc_similarity.sh"
#for var2 in dice simpson
#do
#  echo "$var2"
#  eval "sed -i -e 's/jaccard/$var2/g' calc_similarity.sh"
#  eval "./calc_similarity.sh"
#done
#eval "sed -i -e 's/simpson/jaccard/g' calc_similarity.sh"
echo Finished!
