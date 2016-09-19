# Musical Penguins (Forensics, 45 points)

>[This file](https://github.com/nbrisset/CTF/blob/master/sctf-2016-q1/musical-penguins-45/mystery.tg) is a complete mystery to me, I've never seen notes like these!

Maybe another stegano?

```
root@kali-nils:~/SCTF2016# file mystery.tg
mystery.tg: data
root@kali-nils:~/SCTF2016# head -c 80 mystery.tg
TuxGuitar File Format - 1.2�x
```

TuxGuitar is an opensource music editor. Once downloaded, we load this mysterious file in it, and... taadaaam!

![mystery.tg once loaded in TuxGuitar](mystery.png)

Well, the output is truncated, there are actually 194 bars of five notes/pulses each.
But something jumped out at me: there are only two different notes, E (mi) and C (do).
At first sight, it could be either binary numbers: E equals 0, C equals 1 and vice versa --- or morse code: 
E is a dot, C is a dash and vice versa. As nothing conclusive had turned up with the binary, let's work on the morse code.

I listened to the whole piece, "di di da da da di di da da da", and wrote down some dots and dashes.

By the way, I learned that the European musical scale,
"ut/do–re–mi–fa–so–la-si", comes from the first verse of a Latin hymn, "[Ut queant laxis](https://en.wikipedia.org/wiki/Ut_queant_laxis)".
Steganography is everywhere, even in the eleventh century! Well this was a bit off topic, the morse code is given below.

```
Ut queant laxis
      resonare fibris,
Mira gestorum
      famuli tuorum,
Solve polluti
      labii reatum,
Sancte Iohannes.
```

There is the morse code:

```
..--- ..--- ...-- / ..--- ----- .---- / ..--- ..--- ....- / ..--- ----- ....- / 
..--- ...-- ....- / .---- ----- ----- / .---- -.... ....- / ..--- ..--- ..... / 
.---- ----- ....- / .---- ----- ..--- / ..--- ----- ..--- / .---- -.... ....- / 
..--- ..--- ....- / -.... -.... / .---- -.... ....- / ..--- .---- ....- / 
.---- ----- ...-- / ..--- .---- ..--- / .---- ----- ..--- / .---- -.... ....- / 
..--- .---- ....- / ..--- ..--- ..... / .---- ----- ....- / .---- ----- ----- / 
..--- ----- .---- / .---- -.... ....- / ..--- ...-- ----- / .---- ----- ----- / 
..--- ..--- ....- / ..--- ----- -.... / .---- -.... ....- / ..--- ..--- ....- / 
..--- ----- -.... / .---- ----- ----- / .---- ----- ....- / .---- -.... ....- / 
.---- ----- ...-- / ..--- .---- ...-- / ..--- .---- ...-- / .---- -.... ....- / 
..--- ..--- ....- / ..--- ----- -.... / .---- ----- ..--- / .---- -.... ....- / 
..--- ..--- ....- / .---- ----- ----- / ..--- .---- ....- / .---- ----- ..--- / 
..--- ...-- -....
```

... which gives, once decoded, a few numbers of three digits, except one which has only two digits... have you noticed it?

```
223 201 224 204 234 100 164 
225 104 102 202 164 224 66 
164 214 103 212 102 164 214 
225 104 100 201 164 230 100 
224 206 164 224 206 100 104 
164 103 213 213 164 224 206 
102 164 224 100 214 102 236 
```

49 numbers, seven squared numbers. The hint "[Morgan Freeman and Kevin Spacey](https://en.wikipedia.org/wiki/Seven_(1995_film)) would have fun with this one"
brought me, firstly, to consider these numbers as a 7x7 square. I spent some hours doing a lot of weird and
outlandish operations with the lines/columns/diagonals/numbers/digits: summing, subtracting, fractioning,
finding a path in an assumed maze of digits, or coloring the prime numbers, in order to reveal a hidden message.

"But there are only digits from 0 to 6. It's the base-7 number system, isn't it?"
said Gaétan, my teammate, in the other room.

Dammit.

```
root@blinils:~# python
Python 2.7.12+ (default, Aug  4 2016, 04:04:04)
[GCC 6.1.1 20160724] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>> numbers = ["223","201","224","204","234","100","164","225","104","102",\
"202","164","224","66","164","214","103","212","102","164","214","225","104",\
"100","201","164","230","100","224","206","164","224","206","100","104","164",\
"103","213","213","164","224","206","102","164","224","100","214","102","236"]

>>> flag = ''
>>> for c in numbers: flag += chr(int(c, 7))

>>> flag
'sctf{1_u53d_t0_m4k3_mu51c_w1th_th15_4ll_th3_t1m3}'
```

This challenge was pretty cool and very entertaining!
