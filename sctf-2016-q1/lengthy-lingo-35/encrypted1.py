#Opening the file
file = open("encrypted.dat")
numbers = file.read()
file.close()

#Removing commas and line breaks
numbers = numbers.replace("\r\n","").split(", ")

#Counting the characters
numbers = map(len, numbers)
print numbers

"""[115, 99, 116, 102, 123, 49, 48, 49, 95, 116, 104, 51, 95, 110, 117, 109, 98, 51, 114,
53, 95, 100, 49, 100, 110, 39, 55, 95, 51, 118, 51, 110, 95, 109, 52, 116, 116, 51, 114, 125]"""

#Displaying characters from their ASCII code
numbers = "".join(map(chr, numbers))
print numbers

#sctf{101_th3_numb3r5_d1dn'7_3v3n_m4tt3r}
