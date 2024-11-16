# Crypto / The Biggest

Tenemos el script del cifrado, las operaciones para obtener la clave, el texto cifrado, el nonce y el tag, solo queda revertir el cifrado:

``` python
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
import sys 

# Decrypt
def decrypt(ciphertext, key, nonce, tag):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext


# Get the key
sys.set_int_max_str_digits(2147483646)
n = ((((((42 * 17 + 50 ** 2) * 1000) // 3) * 7 + sum(range(1, 101))) * 123) + -786759022)
p = (1 << n) - 1
p = str(p).encode()
key = p[1000000:1000032]

# Known nonce , ciphertext and tag
nonce = bytes.fromhex("0a6cdcd02b77d771ab3578995ede7039")
ciphertext = bytes.fromhex("36611db0c0008001bf38fcb63c64ce5f378e9d07355ff1cf44")
tag= bytes.fromhex("408801ff1ee7625e688c1ce73279433a")

print(decrypt(ciphertext, key, nonce, tag))
```

`flag{B1gg3st_Pr1m3_3v3r!}`
