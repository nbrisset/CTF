_[<<< Return to NeverLAN CTF 2017 tasks and writeups](/2017-neverlanctf)_

# Master Mind 1 (Other, 50 points)
>Can you break my three digit lock? [MasterMind1.txt](MasterMind1.txt)

```
+-----------------------+
|   7   |   3   |   6   | One number is correct but wrongly placed
|   0   |   6   |   5   | One number is correct and correctly placed
|   3   |   7   |   2   | Two numbers are correct but wrongly placed
|   6   |   4   |   7   | No numbers are correct
|   5   |   2   |   4   | One number is correct and correctly placed
+-----------------------+
```

* Possible: three distinct numbers in {0, 2, 3, 4, 5, 6, 7} which means 7x6x5 = 210 combinations.
```
023 024 025 026 027 032 034 ... 345 346 347 350 352 354 ... 756 760 761 762 763 764 765
```

* Fourth line: three distinct numbers in {0, 2, 3, 5} which means 4x3x2 = 24 combinations.
```
023 025 032 035 052 053 203 205 230 235 250 253 302 305 320 325 350 352 502 503 520 523 530 532
```

* Third line: 3 and 2 are wrongly placed, which eliminates the 3-x-x and x-x-2 combinations.
```
023 025 035 053 203 205 230 235 250 253 503 520 523 530
```

* First line: 3 is correct but wrongly placed, which eliminates the x-3-x combinations.
```
023 025 053 203 205 250 253 503 520 523
```

* Second line: either 0 or 5 is correctly placed, which eliminates all but the 0-x-x and x-x-5 combinations (and 0-x-5 too).
```
023 053 205 253
```

* Fifth line: either 2 or 5 is correctly placed, which eliminates all but the 5-x-x and x-2-x combinations (and 5-2-x too).
```
023
```

# Master Mind 2 (Other, 100 points)
>I've upgraded my lock! Can you solve it? [MasterMind2.txt](MasterMind2.txt)

```
|   9   |   5   |   3   |   2   | One number is correct but wrongly placed
|   1   |   6   |   7   |   3   | Two numbers are correct and correctly placed
|   0   |   6   |   5   |   9   | Two numbers are correct but wrongly placed
|   2   |   4   |   3   |   8   | No numbers are correct
|   5   |   2   |   4   |   0   | One number is correct and correctly placed
```

* Possible: four distinct numbers in {0,1,2,3,4,5,6,7,8,9} which means 10x9x8x7 = 5040 combinations.
```
0123 0124 0125 0126 0127 0128 0129 0132 0134 ... 9865 9867 9870 9871 9872 9873 9874 9875 9876
```

* Fourth line: four distinct numbers in {0,1,5,6,7,9} which means 6x5x4x3 = 360 combinations.
```
0156 0157 0159 0165 0167 0169 0175 0176 0179 .... 9710 9715 9716 9750 9751 9756 9760 9761 9765
```

* Second line: 3 is incorrect, so is 6 (according to the third line) then the combination is 1-x-7-x.

* Fifth line: either 0 or 5 is correctly placed, which eliminates all but the 5-x-x-x and x-x-x-0 combinations.

5 cannot be the first number, so the combination is 1-x-7-0.

* First line: either 9 or 5 is correct but wrongly placed, which eliminates the 9-x-x-x and x-5-x-x combinations.

5 is incorrect, so the combination is 1-9-7-0.
