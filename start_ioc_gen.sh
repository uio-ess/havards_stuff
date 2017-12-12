#!/bin/bash

python ~/git/havards_stuff/st_gen.py
source $HOME/bin/ng3esetup.sh
which caget >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "caget not found in PATH!"
	exit 1
fi

cd $NG3E_IOCS/imgioc-master+4/iocBoot/iocImg || exit 1
../../bin/linux-x86_64/imgApp /tmp/st_gen.cmd
