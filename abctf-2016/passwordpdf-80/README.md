# PasswordPDF (Forensics, 80 points)
>Oh no. We locked [this](https://mega.nz/#!ER8wEBDD!kdjQxaoBX2qWky1dKvlAZq-ToC_kGJbpiV-hOfxXdks)
PDF and forgot the password. Can you help us?

We are given a link to a PDF file.
The holy flag is in it, but unfortunately, a password is required to open the file.

![1st screenshot of the "PasswordPDF" challenge](mypassword1.png)

After all usual checks were completed (binwalk, file, hachoir-subfile, strings/grep)
without any result, only one path remains: that mysterious password.

Passwords are generally cracked using one of the following methods : guessing, dictionary attacks or bruteforce attacks.

* Guessing: for example, a list of the most commonly used passwords (azerty, 123456, password, orange...) 
is published every year. Your birth place, your favorite color or your pet name... an easy password to
remember, but an easy password to guess or to find on the social networks.

* [Dictionary attacks](https://en.wikipedia.org/wiki/Password_cracking): this attack is
"based on trying all the strings in a [...] list of words such as in a dictionary".

* [Brute-force attacks](https://en.wikipedia.org/wiki/Brute-force_attack): every possible combination is tested,
which may take a very VERY long time but the password will be eventually found.

For this challenge, I read again and again
[this excellent guide](https://repo.zenk-security.com/Reversing%20.%20cracking/Cracking_Passwords_Guide.pdf),
and opted for a dictionary attack.

I used the pdfcrack tool with a big dictionary of Dirbuster,
a tool designed to search for directories and files on web servers.

```
root@blinils:~/ABCTF# time pdfcrack -f mypassword.pdf -w /usr/share/wordlists/dirb/big.txt

PDF version 1.5
Security Handler: Standard
V: 2
R: 3
P: -4
Length: 128
Encrypted Metadata: True
FileID: 1ecbf21672ff4260869a162859538cd1
U: fd971477b14eba588631b5d8a336247700000000000000000000000000000000
O: 7bb5945af9cc21222b426d621fd7036701b96c4b23b26632822ae1d9f262b59a
found user-password: 'elephant'
 
real    0m0.207s
user    0m0.192s
sys    0m0.012s
```
 
And.... taadaaam! In less than half a second, the password is recovered: elephant.

We open the PDF and then...

![2nd screenshot of the "PasswordPDF" challenge](mypassword2.png)

This is not over, but the flag is necessarily hidden in the document.

Actually, if we select all the text, copy and paste it into a text editor, we have the flag.

Solution: ABCTF{Damn_h4x0rz_always_bypassing_my_PDFs}
