_[<<< Return to sCTF 2016 Q1 tasks and writeups](/sctf-2016-q1)_
# Verticode (Cryptography, 90 points)

>Welcome to Verticode, the new method of translating text into vertical codes.

>Each verticode has two parts: the color shift and the code.
The code takes the inputted character and translates it into an ASCII code,
and then into binary, then puts that into an image in which each black pixel
represents a 1 and each white pixel represents a 0.

>Except, it isn't that simple.

>A color shift is also integrated, which means that the color before each verticode shifts the ASCII
code, by adding the number that the color corresponds to, before translating it into binary. The table
for the color codes is: 0 = Red, 1 = Purple, 2 = Blue, 3 = Green, 4 = Yellow, 5 = Orange. This means
that a red color shift for the letter A, which is 65 + 0 = 65, would translate into 1000001 in binary;
however, a green color shift for the letter A, which is 65 + 3 = 68, would translate into 1000100 in binary.

>Given [this verticode](code1.png), read the verticode into text and find the flag.

Each square is 12x12 pixels, and each line is made up 14 squares.

For each line, the first seven ones are the "color", the remaining seven are the binary-ASCII code.

[This (ugly but working) Python code does the job.](verticode.py)

```
Output : JoeLopowasamanofmildtemperamentshortstatureandhadthegoalto
becometheworldsfastesttelephoneeaterThoughLoponeverknewevenbasic
physicshecreatedatelescopecapableofsightingthesmallesthaironanalienwholived
quiteafewlightyearsawayJoeLopoquicklydestroyedalargeboulderandusedtheshattered
remainstoformeightsmallstatuesthatstronglyresembledtinycreaturesbeingorrelatedtothe
waterfleaHeplacedtheminacircularpatterntoformasortofshrineandplacedthetelescope
inthemiddleofitHethenchanneledthepowerofthestonewaterfleasintothetelescopetoview
thepoweroftheheavensHewasinatrancewiththebeautyofthemysteriousdimensionand
didntevennoticetheverylargetornadoheadingtowardhimTheshrinewasquicklydemolished
andtheimmediatewithdrawlofpowersentJoeLobointoalairofpitchblacknessfoundtobea
paralleldimensionthatcausABCiamtheflagalllowercasenojokeDEFanyonewhosefirstname
beganwithJalongwithMLandQtobecomeratheruncomfortableJoewasalsosuddenlyintroduced
toundroclamaticolomphasisciousytheeccentrictapewormwithastrongmorrocanaccent
ImundroclamaticolomphasisciousytheeccentrictapewormIlikepizzasohowareyadoinIhavenoideasaidJoe
```

Solution: sctf{iamtheflagalllowercasenojoke}

