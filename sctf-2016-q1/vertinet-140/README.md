_[<<< Return to sCTF 2016 Q1 tasks and writeups](/sctf-2016-q1)_
# Vertinet

>Welcome to Vertinet.

>This problem follows the same specifications as the previous Verticode problem, except that you have to solve
many of them by developing a client to communicate with the server available at problems1.2016q1.sctf.io:50000. Good luck.

Il s'agit du même principe que le challenge
[Verticode](https://github.com/nbrisset/CTF/tree/master/sctf-2016-q1/verticode-90),
à ceci près que l'on devra résoudre des codes en boucle.

En se connectant au serveur via la commande `nc problems1.2016q1.sctf.io 50000` voici ce que l'on obtient.

```html
<html>
 <img src='data:image/png;base64,blablablablablablablablablablablabla=='></img>
<br><br>
```

Voici les étapes à suivre pour récupérer le flag. #1 Se connecter au serveur #2 Récupérer les données envoyées par le serveur #3 Extraire à l'aide d'une expression rationnelle la chaîne de caractères en base64 #4 Convertir cette dernière en image PNG #5 Procéder au traitement de l'image en réutilisant le code Python écrit pour le challenge Verticode #6 Envoyer le résultat au serveur #7 Tant que le serveur répond, recommencer à partir du #2. 

Voici [le snippet en Python](vertinet.py) qui, une fois exécuté, récupère le flag après 30 secondes de résolution intense de codes !

Solution: sctf{y0ub34tth3v3rt1c0d3}

