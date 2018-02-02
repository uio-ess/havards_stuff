#!/bin/bash

python ~/git/havards_stuff/st_gen.py

source $HOME/bin/source-me
which caget >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "caget not found in PATH!"
	exit 1
fi

cd $SHI_IOCS/imgioc-D1/iocBoot/iocImg || exit 1
#../../bin/linux-x86_64/imgApp st.cmd
../../bin/linux-x86_64/imgApp /tmp/st_gen.cmd
