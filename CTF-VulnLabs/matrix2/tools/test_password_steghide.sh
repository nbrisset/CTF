#!/bin/bash
for WORD in `dicoMatrix2.txt`
do
	steghide extract -sf h1dd3n.jpg -p "$WORD" 2>/dev/null
	if [[ $? = 0 ]]; then
			echo "[+] Found:" $WORD
		break
	fi
done
