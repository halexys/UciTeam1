# Crypto / XOR 3: Bugbounty description 

Ver https://en.wikipedia.org/wiki/Bug_bounty_program y hacer un XOR entre el texto del documento challenge.txt y el principio del articulo

``` python 
from Crypto.Util.strxor import strxor

with open('challenge.txt', 'r') as f:
    ct = f.read().replace('\n', '')

ct = bytes.fromhex(ct)

flag_head = b'flag{'
pt_head = strxor(ct[:len(flag_head)], flag_head).decode()
print('[+] pt head:', pt_head)

# guess
pt = 'A bug bounty program is a deal offered by many websites, organizations, and software developers'
flag = strxor(ct[:len(pt)], pt.encode()).decode()
print('[*] flag:', flag)
```

`flag{C3rTUNlP_2024_fflag}`
