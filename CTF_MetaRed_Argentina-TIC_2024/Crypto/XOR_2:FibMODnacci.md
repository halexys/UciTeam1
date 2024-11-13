# Crypto / XOR 2: FibMODnacii

'676d63647e5f627a4d580ecfbe1c0eb779283b5eef68c24e204411009455'

Hay que hacer convertir esto de hexadecimal a un array de bytes, crear un array de bytes de igual longitud, y aplicarles la operacion XOR mod 256:

``` python
def fibo(n):
    a, b = 0, 1
    sequence = []
    while n:
        n -= 1
        sequence.append(b)
        a, b = b, a+b
    return sequence


data = "676d63647e5f627a4d580ecfbe1c0eb779283b5eef68c24e204411009455"
enc_data = bytes.fromhex(data)
fib_key = fibo(len(enc_data))

flag = ''

for i in range(len(enc_data)):
    flag += chr(enc_data[i] ^ fib_key[i] % 256)

print(flag)
```

`flag{WooooW_WellD0n3-G3n1uSs!}`

