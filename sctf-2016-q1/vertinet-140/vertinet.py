from PIL import Image
from io import BytesIO
import base64, binascii, re, socket, sys
 
hote = 'problems1.2016q1.sctf.io'
port = 50000 
 
#function givecolor(hex)
#returns the value of the "color shift"
def givecolor(hex) :
    decal = 0
    if(hex == "#ff0000") : decal = 0 #red
    elif(hex == "#800080") : decal = 1 #purple
    elif(hex == "#0000ff") : decal = 2 #blue
    elif(hex == "#008000") : decal = 3 #green
    elif(hex == "#ffff00") : decal = 4 #yellow
    elif(hex == "#ffa500") : decal = 5 #orange
    return decal

#function colortobin(color)
#it's black, it's white, whoo
def colortobin(color) :
    bit = ''
    if(color == "#000000") : bit = '{:b}'.format(1) #black = 1
    elif(color == "#ffffff") : bit = '{:b}'.format(0) #white = 0
    return bit

#function rgb2hex(r, g, b)
#returns the hexa value from the RGB one
def rgb2hex(r, g, b) :
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def traitementImage(m) :
    test = re.findall ("<html><img src='data:image/png;base64,(.*?)'></img>", m, re.DOTALL)
    imageb64 = "".join(test)

    imVertical = Image.open(BytesIO(base64.b64decode(imageb64)))
    imVertical.save('somepixels.png', 'PNG')
 
    im = Image.open("somepixels.png")
    pix = im.load()
 
    message = ""
    width, height = im.size
    pixels = im.convert('RGBA').load()
    #each square is 12x12 pixels
 
    #for each line...
    for y in range(1, height, 12) :
          #for each 12x12 pixel...
          for x in range(1, width, 12) :
              r, g, b, a = pixels[x, y]
              hexa = rgb2hex(r, g, b)
              if x in range(1, 74) :
                    #which color is the pixel?
                    color = givecolor(hexa)
                    bits = ""
              if x in range(85, 158) :
                    #gimme the 01010101010101...
                    bits += colortobin(hexa)
         
          #shifting
          fragment = chr(int(bits, 2) - int(color))
          #writing
          message += fragment
    return message
 
#connect to problems1.2016q1.sctf.io
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
 
#keep solving and keep solving
while True :
    msg_recu = connexion_avec_serveur.recv(2048)
    print msg_recu
    reponse = traitementImage(msg_recu)
    print reponse
    connexion_avec_serveur.send(reponse)