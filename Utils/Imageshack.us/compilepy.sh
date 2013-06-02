#!/bin/bash
python2.7 -OO -m compileall $1
mv ${1}o $2
echo "compilepy.sh ..."