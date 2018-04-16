import urllib, qrtools

IMG = "temp.png"
URL = "https://nilsbrisset.info/labyqrinthe/"
EXT = ".png"

qr = qrtools.QR()
ID = "5882056720452989866926902"

for i in range(0, 200) :
	print "#", i, "[+] Retrieving:", URL+ID+EXT
	urllib.urlretrieve(URL+ID+EXT, IMG)
	qr.decode(IMG)
	print "#", i, "[+] Decoding:", qr.data
	ID = qr.data
