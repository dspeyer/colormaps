#!/bin/bash -ex

wget http://xkcd.com/color/colorsurvey.tar.gz
tar xzvf colorsurvey.tar.gz
sqlite3 xkcd.sqllite < mainsurvey_sqldump.txt
