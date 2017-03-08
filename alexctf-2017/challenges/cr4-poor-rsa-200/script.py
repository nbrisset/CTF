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
