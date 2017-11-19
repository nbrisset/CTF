_[<<< Return to Dev Test Days 2017 tasks and writeups](/devtestdays-2017)_
# Crack the Pass #1 (Misc, 200 points)

>Dans le cadre d'une vaste affaire d'espionnage sur le site de Meylan, l'agence de renseignement Orange Hats [a intercepté un document sensible](FIND_THE_PASS1.zip) ; or impossible de l'ouvrir car il faut un mot de passe. Tout ce que nous savons est que le propriétaire de ce fichier n'est pas très précautionneux et utilise systématiquement des mots de passe à cinq chiffres.

>Pouvez-vous nous aider et récupérer le flag ?

Indeed, a password is required to open the archive FIND_THE_PASS1.zip, whereas the flag seems to be in a PNG file.

```console
root@blinils:/DTD2017# unzip FIND_THE_PASS1.zip
Archive:  FIND_THE_PASS1.zip
[FIND_THE_PASS1.zip] such_a_dog.png password: 
password incorrect--reenter: 
password incorrect--reenter: 
   skipping: such_a_dog.png          incorrect password
```

Passwords are generally cracked using one of the following methods : guessing, dictionary attacks or bruteforce attacks.

* Guessing: for example, a list of the most commonly used passwords (azerty, 123456, password, orange...) 
is published every year. Your birth place, your favorite color [or your pet name...](https://www.youtube.com/watch?v=lRqT3PtxA0Q) an easy password to
remember, but an easy password to guess or to find on the social networks.

* [Dictionary attacks](https://en.wikipedia.org/wiki/Password_cracking): this attack is
"based on trying all the strings in a [...] list of words such as in a dictionary".

* [Brute-force attacks](https://en.wikipedia.org/wiki/Brute-force_attack): every possible combination is tested, which may take
a very VERY long time but the password will be eventually found. Assuming that the password is five characters long and only
consists in digits, there are 100 000 possible combinations (00000 to 99999), thus this method will be used for this challenge.

Actually, desktop computers can test over a hundred million passwords per second using password cracking tools.

We are going to use [fcrackzip](https://korben.info/cracker-des-zip-rar-7z-et-pdf-sous-linux.html),
a tool dedicated to crack passwords put on archive files (like pdfcrack for PDF files).

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

Let's begin the attack!

```console
root@blinils:/DTD2017# time fcrackzip -b -c 1 -v -u -l5 FIND_THE_PASS1.zip
found file 'such_a_dog.png', (size cp/uc 355725/355699, flags 9, chk 05eb)


PASSWORD FOUND!!!!: pw == 97531

real	0m0,900s
user	0m0,720s
sys	0m0,149s
```

The 5-digit password was found at lightning speed (kind of). We open the ZIP archive and...

```console
root@blinils:/DTD2017# ls
FIND_THE_PASS1.zip

root@blinils:/DTD2017# unzip -P 97531 FIND_THE_PASS1.zip
Archive:  FIND_THE_PASS1.zip
  inflating: such_a_dog.png

root@blinils:/DTD2017# ls
FIND_THE_PASS1.zip  such_a_dog.png
```

... taadaaam! We can now [read the flag](such_a_dog.png) and score 200 points!
