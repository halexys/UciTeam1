# No Leak

Se realiza un XOR con una clave de 18 bytes y la flag y nos dan el texto cifrado:
``` python3
import os
from secret import flag

key = os.urandom(18)

xored = bytes(f ^ k for f, k in zip(flag, key * (len(flag) // len(key) + 1)))

with open("output.txt", "w") as f:
    f.write(f"Key: {key.hex()}\n")
    f.write(f"Ciphertext: {xored.hex()}")

# Key: Redacted
# Ciphertext: b3f0716f4a94ef6a6d6ce2b908d52d53c64696af67477dcade387770829324f23852fe78aff3266b5780
```

Dado que sabemos que la flag comienza con "CodeVinciCTF{" y la operacion XOR es reversible, podemos obtener la clave parcial (13 bytes):
``` python
cipher = bytes.fromhex("b3f0716f4a94ef6a6d6ce2b908d52d53c64696af67477dcade387770829324f23852fe78aff3266b5780")
known_plaintext = b"CodeVinciCTF{"
# con 5 bytes de error
key = bytes(cipher[i] ^ known_plaintext[i] for i in range(len(known_plaintext))) + b"\x00" * 5
flag = bytes(cipher[i] ^ key[i % len(key)] for i in range(len(cipher)))
print(flag.decode(errors='ignore'))
```

```
python3 a.py
CodeVinciCTF{-SFf0rMa7_1s_4lW8Rx_l3aK}
```

Faltan fragmentos, el resto de los bytes los hallamos practicamente adivinando:

``` python
cipher = bytes.fromhex("b3f0716f4a94ef6a6d6ce2b908d52d53c64696af67477dcade387770829324f23852fe78aff3266b5780")

known_plaintext = b"CodeVinciCTF{"
 
_1 = cipher [13] ^ ord("F")
_2 = cipher [14] ^ ord("l")
_3 = cipher [15] ^ ord("4")
_4 = cipher[16] ^ ord("g")
_5 = cipher[17] ^ ord("_")

key = bytes(cipher[i] ^ known_plaintext[i] for i in range(len(known_plaintext))) + bytes([_1]) + bytes([_2]) + bytes([_3]) + bytes([_4]) + bytes([_5])
flag = bytes(cipher[i] ^ key[i % len(key)] for i in range(len(cipher)))
print(flag)
```

`CodeVinciCTF{Fl4g_f0rMa7_1s_4lWay5_a_l3aK}'`
