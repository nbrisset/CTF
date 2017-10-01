from PIL import Image
import binascii
 
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
 
#Opening and loading the image
im = Image.open("code1.png")
#width = 168 and height = 12900
width, height = im.size
 
message = ""
 
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
 
print message