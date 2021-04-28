#!/bin/bash

work_dir=/Users/yisong/Q-Title
# Change it in your own code :P

save_dir=$work_dir/datasets

echo $save_dir

cd $save_dir

echo 'hello!' >> hello.txt

for venue in cvpr nips iccv eccv aaai icml icra www chi kdd uss ccs icassp ijcai icse sp iclr mm infocom acl wsdm iros icc sigmod aistats miccai cikm globecom nsdi sigcomm emnlp ndss sigir wacv icde icdcs wcnc icip icdm fg pepm isit act date naacl eurocrypt soda ijcnn hpca dac
do
	mkdir $venue
	cd $venue
	echo $PWD
	for year in {1990..2020}
	do
	    url=https://dblp.org/db/conf/$venue/$venue$year.html
	    echo $url
	    curl -O $url
	done
	cd ..
done


# ['Dblp-abbr', 'cvpr', 'nips', 'iccv', 'eccv', 'aaai', 'icml', 'icra', 'www', 'chi', 'kdd', 'uss', 'ccs', 'icassp', 'ijcai', 'icse', 'sp', 'iclr', 'mm', 'infocom', 'acl', 'wsdm', 'iros', 'icc', 'sigmod', 'aistats', 'miccai', 'cikm', 'globecom', 'nsdi', 'sigcomm', 'emnlp', 'ndss', 'sigir', 'wacv', 'icde', 'icdcs', 'wcnc', 'icip', 'icdm', 'fg', 'pepm', 'isit', 'act', 'date', 'naacl', 'eurocrypt', 'soda', 'ijcnn', 'hpca', 'dac']