# Shuffle

Codigo fuente:
```python
#!/usr/local/bin/python3
import random
import time

FLAG = "UVT{F4k3_fl4g}"
P = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]

def padd(l):
    random.seed(int(time.time()))
    for _ in range(32 - len(l)):
        l.append(random.randint(32, 125))
    return l


def shuffle(l):
    nl = []
    for p in P:
        nl.append(l[p])

    return nl


def encrypt(pt):
    l = [ord(x) for x in pt]
    l = padd(l)
    l = shuffle(l)

    random.seed(sum(l))
    key = random.randbytes(len(l))

    ct = [x ^ y for x, y in zip(l, key)]

    return bytes(ct)

print(encrypt(FLAG).hex())
```

En la encriptacion del mensaje se hacen las siguientes operaciones:
1. Se extraen los valores ASCII de los bytes
2. Se añade un padding hasta que el mensaje tenga 32 bytes (el padding se hace con bytes aleatorios en rango 32-125 usando como generador el tiempo actual)
3. Se realiza una permutacion para desorganizar los bytes con P
4. Se realiza un XOR con el mensaje y una clave generada aleatoriamente (usando como generador la suma de los bytes de texto_plano + padding)

Para desencriptarlo hay que invertir las operaciones:
1. Hallar la semilla de la suma de caracteres por fuerza bruta en el rango (32*32,125*32)
2. Deshacer el shuffle con la permutacion inversa de P
3. Deshacer el padding
4. Obtener los bytes resultantes

```python
#!/usr/local/bin/python3
import random

P = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]

# Construir permutación inversa
P_inv = [0] * len(P)
for i, p in enumerate(P):
    P_inv[p] = i

def unshuffle(l):
    return [l[p] for p in P_inv]

def decrypt(ct_hex):
    try:
        ct = bytes.fromhex(ct_hex)
    except ValueError:
        print(f"Invalid hex string: {ct_hex}")
        return None
    
    # Rango posible para la suma S (32*32 a 125*32)
    min_S = 32 * 32
    max_S = 125 * 32
    
    for S in range(min_S, max_S + 1):
        # Encontrar el padding correcto
        random.seed(S)
        key = random.randbytes(len(ct))
        l = bytes([ct[i] ^ key[i] for i in range(len(ct))])
        
        if sum(l) == S:
            # Deshacer el shuffle
            unshuffled = unshuffle(list(l))
            
            # Convertir a string
            try:
                decrypted = ''.join([chr(b) for b in unshuffled])
                if decrypted.startswith("UVT{"):
                    flag_len = decrypted.find("}") + 1 if "}" in decrypted else 32
                    return decrypted[:flag_len]
            except:
                continue
    return None

ct_hex = "252acb5f5b560b6344ab6c2421410eca06b63acb621edf0421f1423a18920208"
flag = decrypt(ct_hex)
print(flag)
```

`UVT{1_l1ke_t0_m0v3_1t_m0v3_i7}`



