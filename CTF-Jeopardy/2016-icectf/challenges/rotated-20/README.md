_[<<< Return to IceCTF 2016 tasks and writeups](/2016-icectf)_
# Rotated! (Crypto, 20 points)

>They went and ROTated the flag by 5 and then ROTated it by 8! The scoundrels!

>Anyway once they were done this was all that was left VprPGS{jnvg_bar_cyhf_1_vf_3?}

It seems that the flag has been ciphered with ROT13, which replaces each letter
by its partner 13 characters further along the alphabet.

```python
>>> "VprPGS{jnvg_bar_cyhf_1_vf_3?}".encode("rot13")
'IceCTF{wait_one_plus_1_is_3?}'
```
