_[<<< Return to ABCTF 2016 tasks and writeups](/CTF-Jeopardy/2016-abctf)_
# Caesar Salad (Cryptography, 10 points)

>Most definitely the best salad around. Can you decrypt this for us? xyzqc{t3_qelrdeq_t3_k33a3a_lk3_lc_qe3p3}

Many CTFs begin with a [Caesar code](https://en.wikipedia.org/wiki/Caesar_cipher) challenge,
as a welcome gift, such as [When in Rome](/CTF-Jeopardy/2016-sctf-q1/challenges/when-in-rome-10) ([sCTF 2016 Q1](/CTF-Jeopardy/2016-sctf-q1)).

This time, I used the [Caesar cipher in Bash](https://web.archive.org/web/20160604002957/http://www.shell-fu.org/lister.php?id=195) with a right shift of 3,
and [a tip](https://www.digitalocean.com/community/tutorials/how-to-use-bash-history-commands-and-expansions-on-a-linux-vps)
to re-execute the previous provided command.


```console
root@blinils:~/abctf-2016# echo "xyzqc{t3_qelrdeq_t3_k33a3a_lk3_lc_qe3p3}"
xyzqc{t3_qelrdeq_t3_k33a3a_lk3_lc_qe3p3}

root@blinils:~/abctf-2016# echo `!!` | tr '[x-za-w]' '[a-z]'
echo `echo "xyzqc{t3_qelrdeq_t3_k33a3a_lk3_lc_qe3p3}"` | tr '[x-za-w]' '[a-z]'
abctf{w3_thought_w3_n33d3d_on3_of_th3s3}
```

