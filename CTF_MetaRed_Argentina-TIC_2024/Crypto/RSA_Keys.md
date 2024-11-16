# Crypto / RSA Keys

``` python
#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import itertools

ns = []
for i in range(25):
    fname = 'challenge/public-%d.txt' % i
    with open(fname, 'r') as f:
        pub_data = f.read()

    pubkey = RSA.importKey(pub_data)
    n = pubkey.n
    e = pubkey.e
    assert e == 65537

    ns.append(n)

e = 65537

for (n0, n1) in list(itertools.combinations(ns, 2)):
    p = GCD(n0, n1)
    if p > 1:
        idx = ns.index(n0)
        q = n0 // p
        break

phi = (p - 1) * (q - 1)
d = inverse(e, phi)

ct_fname = 'challenge/ciph-%d.txt' % idx

with open(ct_fname, 'rb') as f:
    c = bytes_to_long(f.read())

m = pow(c, d, n0)
flag = long_to_bytes(m).decode()
print(flag)
```

`flag{LosPrimosSeanUnidos}`
