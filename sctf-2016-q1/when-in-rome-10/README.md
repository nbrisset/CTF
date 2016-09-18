# When in Rome (Cryptography, 10 points)

>I heard of a cipher named after Julius Caesar, and I want you to try it out! Try decoding this message:
`Nvctfdv kf jTKW! Nv yfgv pfl veafp kyv gifscvdj nv yrmv nizkkve wfi kyv wzijk hlrikvi fw 2016.
Yviv zj pfli wzijk fw (yfgvwlccp) drep wcrxj! jtkw{ny3e_1e_tkw_u0_r5_tkw3i5_u0}`

Well, as the title says, this message has been encrypted with Caesar's code, a famous substitution cipher.
Actually, each letter in the original message has been replaced by a letter further in the alphabet:
for example, "with a left shift of 3, D would be replaced by A, E would become B, and so on".

For this competition, each "flag" (or answer) has the following format: sctf{some_random_words},
then it's easy to find the "key" (or shift parameter). With a left shift of 17, jTKW would be sCTF.
Knowing the key, the plaintext could be recovered: 

`Welcome to sCTF! We hope you enjoy the problems we have written for the first quarter of 2016.
Here is your first of (hopefully) many flags! sctf{wh3n_1n_ctf_d0_a5_ctf3r5_d0}`
