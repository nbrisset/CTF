_[<<< Return to BitsCTF 2017 tasks and writeups](/bitsctf-2017)_
# Black Hole (Forensics, 10 points)

>We are trying to study the Black Holes. One of the most controversial theory related to Black Holes is the "Information Loss Paradox". Calculations suggest that physical information could permanently disappear in a black hole. But this violates the quantum theory. To test the hypothesis, we sent our flag encoded in Base64 format towards a Black Hole. With the help of our Hubble Space Telescope, we got some pictures of the Black Hole. See if you can recover the flag from this information.

This challenge consists in [a beautiful picture](black_hole.jpg) of a black hole.

Apparently, the flag has been sent encoded in Base64 format, so let's check this.

```console
root@blinils:~/bitsctf-2017# echo "BITSCTF{flag}" | base64
QklUU0NURntmbGFnfQo=

root@blinils:~/bitsctf-2017# strings black_hole.jpg | grep QklU
UQklUQ1RGe1M1IDAwMTQrODF9
```

Gotcha! We are pretty lucky because this flag wasn't in the usual format.

```console
root@blinils:~/bitsctf-2017# echo "QklUQ1RGe1M1IDAwMTQrODF9" | base64 -d
BITCTF{S5 0014+81}
```


