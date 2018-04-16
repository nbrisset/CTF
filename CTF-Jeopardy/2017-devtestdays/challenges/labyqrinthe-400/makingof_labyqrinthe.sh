#!/bin/bash
COUNTER="DevTestDays{congratz_for_qrlooping!}"
for i in `seq 1 150`;
do
	OUTPUT="$(cat /dev/urandom | tr -dc '0-9' | fold -w 25 | head -n1)"
	qr $COUNTER > $OUTPUT.png.old
	echo $OUTPUT
	COUNTER=$OUTPUT 
done
