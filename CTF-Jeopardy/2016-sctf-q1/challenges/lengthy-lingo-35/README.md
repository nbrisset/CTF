_[<<< Return to sCTF 2016 Q1 tasks and writeups](/2016-sctf-q1)_
# Lengthy Lingo (Cryptography, 35 points)

>Can you crack the code? We intercepted [this flag](encrypted.dat) but can't seem to figure out how it was encrypted.

"The numbers don't seem to follow a specific pattern" says the hint, but we can still calculate a lot of numbers: there are 39 commas then 40 numbers, 382 times zero, 399 times one, 404 times two, 391 times three, 383 times four, 392 times five, 408 times six, 400 times seven, 406 times eight... but no nine. 3823994043913833924084004060 is the concatenated result, then we apply the same method.

In this number, there are 6 times zero, 1 times one, 2 times two, 6 times three, 5 times four, 0 times five, 1 times six, 0 times seven, 2 times eight and 4 times nine, so we got 6126501024, then 2220112000, 4240000000, 7010200000, 7110000100, 6300000100, 7101001000, 6300000100, 7101001000, 6300000100, 7101001000, 6300000100, 7101001000, 6300000100, 7101001000, 6300000100, 7101001000, 6300000100... that's an infinite loop!

Well, in fact, [we needed to find the number of digits in each integer](encrypted1.py), corresponding to ASCII values.

```python
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
```

Solution: sctf{101_th3_numb3r5_d1dn'7_3v3n_m4tt3r}

