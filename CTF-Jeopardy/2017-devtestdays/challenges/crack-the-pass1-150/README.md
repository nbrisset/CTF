_[<<< Return to Dev Test Days 2017 tasks and writeups](/CTF-Jeopardy/2017-devtestdays)_
# Crack the Pass #1 (Misc, 150 points)

>Dans le cadre d'une vaste affaire d'espionnage sur le site de Meylan, l'agence de renseignement Orange Hats [a intercepté un document sensible](FIND_THE_PASS1.zip) ; or impossible de l'ouvrir car il faut un mot de passe. Tout ce que nous savons est que le propriétaire de ce fichier n'est pas très précautionneux et utilise systématiquement des mots de passe à cinq chiffres.

>Pouvez-vous nous aider et récupérer le flag ?

Voyons voir à quoi ressemble ce document. Que se passe-t-il si nous tentons de le décompresser sans fournir de mot de passe ?

```console
root@blinils:/DTD2017# unzip FIND_THE_PASS1.zip
Archive:  FIND_THE_PASS1.zip
[FIND_THE_PASS1.zip] such_a_dog.png password: 
password incorrect--reenter: 
password incorrect--reenter: 
   skipping: such_a_dog.png          incorrect password
```

Cela n'a pas fonctionné, mais nous apprenons que le flag réside très certainement dans un fichier PNG.

Nous allons devoir trouver ce fameux mot de passe à cinq chiffres. Le faire à la main serait très fastidieux, c'est pourquoi nous allons faire appel à un outil permettant d'automatiser la recherche. Pour rappel, voici les différentes techniques pour crack^^W tester la robustesse d'un mot de passe (en anglais).

Passwords are generally cracked using one of the following methods : guessing, dictionary attacks or bruteforce attacks.

* Guessing: for example, a list of the most commonly used passwords (azerty, 123456, password, orange...) 
is published every year. Your birth place, your favorite color [or your pet name...](https://www.youtube.com/watch?v=lRqT3PtxA0Q) an easy password to
remember, but an easy password to guess or to find on the social networks.

* [Dictionary attacks](https://en.wikipedia.org/wiki/Password_cracking): this attack is
"based on trying all the strings in a [...] list of words such as in a dictionary".

* [Brute-force attacks](https://en.wikipedia.org/wiki/Brute-force_attack): every possible combination is tested, which may take 
a very VERY long time but the password will be eventually found. Actually, desktop computers can test over a hundred million 
passwords per second using password cracking tools.

Étant donné que le sésame est constitué d'uniquement cinq chiffres, cela nous donne 100 000 (00000 to 99999) combinaisons à tester.

Nous allons donc effectuer une attaque de type bruteforce, à l'aide d'un outil spécialisé 
nommé [fcrackzip](https://allanfeid.com/content/cracking-zip-files-fcrackzip).

```console
root@blinils:/DTD2017# man fcrackzip

-b, --brute-force
   Select brute force mode. This tries all possible combinations of the letters you specify.

-c, --charset characterset-specification
   Select the characters to use in brute-force cracking. Must be one of

   [...]
   1   include the digits [0-9]
   [...]

-u, --use-unzip
   Try to decompress the first file by calling unzip with the guessed password.

-l, --length min[-max]
   Use an initial password of length min, and check all passwords up to passwords of length max.
```

Avec toutes ces informations, nous allons pouvoir lancer l'attaque !

```console
root@blinils:/DTD2017# time fcrackzip -b -c 1 -v -u -l5 FIND_THE_PASS1.zip
found file 'such_a_dog.png', (size cp/uc 355725/355699, flags 9, chk 05eb)


PASSWORD FOUND!!!!: pw == 97531

real	0m0,900s
user	0m0,720s
sys	0m0,149s
```

Et hop ! Le mot de passe est trouvé en moins d'une demi-seconde, nous pouvons désormais décompresser le fichier ZIP.

```console
root@blinils:/DTD2017# ls
FIND_THE_PASS1.zip

root@blinils:/DTD2017# unzip -P 97531 FIND_THE_PASS1.zip
Archive:  FIND_THE_PASS1.zip
  inflating: such_a_dog.png

root@blinils:/DTD2017# ls
FIND_THE_PASS1.zip  such_a_dog.png
```

Le flag est bel et bien situé dans [le fichier PNG](such_a_dog.png), ce qui nous donne 15O points supplémentaires !
