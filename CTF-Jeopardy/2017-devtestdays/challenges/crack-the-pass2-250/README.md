_[<<< Return to Dev Test Days 2017 tasks and writeups](/2017-devtestdays)_
# Crack the Pass #2 (Misc, 250 points)

>L'enquête s'accélère : [un document sensible](FIND_THE_PASS2.zip) a été intercepté, toujours protégé par un mot de passe. Une écoute téléphonique ultérieure révèle que le propriétaire de ce fichier utilise désormais des mots français de six lettres, choisis au hasard dans le dictionnaire.

>Encore une fois, pouvez-vous nous aider et [récupérer le flag](FIND_THE_PASS2.zip) ?

```console
root@blinils:/DTD2017# unzip FIND_THE_PASS2.zip
Archive:  FIND_THE_PASS2.zip
[FIND_THE_PASS2.zip] holy_flag.txt password: 
password incorrect--reenter: 
password incorrect--reenter: 
   skipping: holy_flag.txt           incorrect password
```

...

```console
root@blinils:/DTD2017# time fcrackzip --dictionary -p "/usr/share/dict/words" -v -u FIND_THE_PASS2.zip
found file 'holy_flag.txt', (size cp/uc     56/    44, flags 9, chk baed)


PASSWORD FOUND!!!!: pw == police

real	0m0,733s
user	0m0,578s
sys	0m0,121s
```

...

```console
root@blinils:/DTD2017# ls
FIND_THE_PASS2.zip

root@blinils:/DTD2017# unzip -P police FIND_THE_PASS2.zip
Archive:  FIND_THE_PASS2.zip
 extracting: holy_flag.txt

root@blinils:/DTD2017# ls
FIND_THE_PASS1.zip  holy_flag.txt

root@blinils:/DTD2017# cat holy_flag.txt
DevTestDays{You're_a_good_password_cracker!}
```
