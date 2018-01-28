_[<<< Return to AlexCTF 2017 tasks and writeups](/CTF-Jeopardy/2017-alexctf)_
# Poor RSA (Cryptography, 200 points)

>This time Fady decided to go for modern cryptography implementations.
>He is fascinated with choosing his own prime numbers, so he picked up RSA once more.
>Yet he was unlucky again!

This is a basic "RSA challenge". We are given [an RSA public key](key.pub) (n, e) and [an encrypted message in base64](flag.b64) (c), which is likely to be the flag. The security of [the RSA algorithm](http://sebsauvage.net/comprendre/encryptage/crypto_rsa.html) is based on the mathematical difficulty of finding two prime factors of a very large number.

```console
root@blinils:~/ALEXCTF# openssl rsa -pubin -in key.pub -modulus -text
Public-Key: (399 bit)
Modulus:
    52:a9:9e:24:9e:e7:cf:3c:0c:bf:96:3a:00:96:61:
    77:2b:c9:cd:f6:e1:e3:fb:fc:6e:44:a0:7a:5e:0f:
    89:44:57:a9:f8:1c:3a:e1:32:ac:56:83:d3:5b:28:
    ba:5c:32:42:43
Exponent: 65537 (0x10001)
Modulus=52A99E249EE7CF3C0CBF963A009661772BC9CDF6E1E3FBFC6E44A07A5E0F894457A9F81C3AE132AC5683D35B28BA5C324243
writing RSA key
-----BEGIN PUBLIC KEY-----
ME0wDQYJKoZIhvcNAQEBBQADPAAwOQIyUqmeJJ7nzzwMv5Y6AJZhdyvJzfbh4/v8
bkSgel4PiURXqfgcOuEyrFaD01soulwyQkMCAwEAAQ==
-----END PUBLIC KEY-----
```

Running this [Python script](script.py) gave us the flag and 200 points.

```python
import gmpy
from Crypto.PublicKey import RSA

#reading the public key
pubkey = open('key.pub', 'r').read()
pub = RSA.importKey(pubkey)

#retrieving n and e
n = long(pub.n)
e = long(pub.e)

#computing p and q (n = p*q) thanks to factorDB
p = 863653476616376575308866344984576466644942572246900013156919
q = 965445304326998194798282228842484732438457170595999523426901

#computing the private key exponent d
d = long(gmpy.invert(e, (p-1)*(q-1)))

#recovering the private key
key = RSA.construct((n,e,d))

#decoding and printing the flag
flag = open('flag.b64', 'r').read().decode('base64')
print key.decrypt(flag)
```

```console
root@blinils:~/ALEXCTF# python script.py
�&�d��#H�u6Lۮ��:ALEXCTF{SMALL_PRIMES_ARE_BAD}
```
