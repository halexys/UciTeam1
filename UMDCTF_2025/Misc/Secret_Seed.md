# Secret Seed

Codigo fuente:

``` python
import random
import time

seed = int(time.time())
random.seed(seed)

plaintext = b"UMDCTF{REDACTED}"
keystream = bytes([random.getrandbits(8) for _ in range(len(plaintext))])
ciphertext = bytes([p ^ k for p, k in zip(plaintext, keystream)])

#with open("secret.bin", "wb") as f:
#   f.write(ciphertext)
```

La flag fue encriptada con XOR usando como clave grupos de bits aleatorios entre 0-255 (o sea un byte a la vez) con la misma extension que la flag, generados con una semilla basada en tiempo y almacenada en `secret.bin`

Conocemos el inicio de la flag , si hacemos `parte` ^ `cifrado` obtenemos el `keystream` parcial:
``` python
with open("secret.bin", "rb") as f:
     cipher = f.read()
     part = b"UMDCTF{"
     part_key = bytes([cipher[i] ^ part[i] for i in range(len(part))])

```

Para recuperar el keystream completo le damos para atras, probando desde el tiempo actual hasta `max_time_diff` segundos en el pasado:
- Tomamos el tiempo actual y le restamos N segundos
- Lo asignamos a random.seed
- Extraemos bytes aleatorios hasta la extension de `part_key` 
- Si estos bytes son iguales a nuestra `part_key` entonces este es el tiempo correcto

Luego de esto es simular la operacion con `cipher` y un `keystream_full` para recuperar la flag:

``` python
import random
import time

def recover_seed(known_keystream, max_time_diff=3600):
    current_time = int(time.time())
    for possible_seed in range(current_time - max_time_diff, current_time + 1):
        random.seed(possible_seed)
        generated_keystream = bytes([random.getrandbits(8) for _ in range(len(known_keystream))])
        if generated_keystream == known_keystream:
            return possible_seed
    return None


with open("secret.bin", "rb") as f:
     cipher = f.read()
     part = b"UMDCTF{"
     part_key = bytes([cipher[i] ^ part[i] for i in range(len(part))])
     seed = recover_seed(part_key,400000)
     assert seed != None
     print("Seed:",seed)
     if seed:
        random.seed(seed)
        keystream_full = bytes([random.getrandbits(8) for _ in range(len(cipher))])
        plaintext = bytes([c ^ k for c, k in zip(cipher, keystream_full)])
        print(plaintext.decode())
```

**Nota**: Esto se volvera imposible de resolver a futuro, ahora es posible porque ha pasado poco tiempo desde que se creó el reto. La semilla es `1745447710`

`UMDCTF{pseudo_entropy_hidden_seed}`
