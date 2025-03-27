# Mothership 

![2025-03-27-144412_721x366_scrot](https://github.com/user-attachments/assets/832b1ba8-8300-44d0-9729-cde080b90a57)

```
=== Alien Transmission System ===
Welcome to the transmission system.

SAFE TRANSMISSION: XqbxczX5fiBKq0mj4fthQzK87AcZVmVUOtXitT1AJN0=
SEND TRANSMISSION:
```

Mothership consiste en el intercambio de mensajes cifrados usando AES-128-CBC

Nos envia en base64 un mensaje cuyos primeros 16 bytes son el `iv` o vector de inicializacion y los otros 16 son el mensaje "SHIP:SAFE" cifrado:
``` python
def encrypt(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(message.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded)
    return base64.b64encode(iv + ciphertext).decode()
...
print("\nSAFE TRANSMISSION:", encrypt("SHIP:SAFE", key, iv))
```

Espera una transmision en base64 cifrada usando la misma clave y vector de inicializacion que usa para enviar "SHIP:SAFE":
``` python
def validate(data, key):
    try:
        data = base64.b64decode(data)
        iv = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

        return decrypted == "SHIP:FIRE"
    except:
        print("Invalid transmission.")
        raise SystemExit(1)
```

Si el mensaje recibido descifrado es "SHIP:FIRE", y esto ocurre 200 veces, entonces nos daran unas cordenadas:
``` python
    for i in range(200):
        key = os.urandom(16)
        iv = os.urandom(16)

        print("\nSAFE TRANSMISSION:", encrypt("SHIP:SAFE", key, iv))
        data = input("SEND TRANSMISSION: ")
        if not validate(data, key):
            print("Safe transmission received. Exiting.")
            return
        print(f"Attack transmission received ({i + 1}/200). Continue to confirm.")

    print("Attack mode initiated. Ship coordinates:", COORDS)
``` 

Del mensaje que nos envia la nave nodriza obtenemos el iv, el mensaje cifrado y sabemos el mensaje en texto plano

### Bit Flipping en AES-CBC

El proceso de encriptacion de AES-CBC es de la siguiente forma:

`c = cipher(m ^ iv)` 

Donde c es el texto cifrado, cipher es el algoritmo, m es el mensaje e iv es el vector de inicializacion

El proceso de desencriptacion es la inversa de las operaciones:

`m = decipher(c) ^ iv`

Debemos enviar el texto cifrado (16 bytes) y el iv (16bytes) y codificarlo en base64

¿ Que ocurre si hacemos new_iv =  iv ^ "SHIP:SAFE" ^ "SHIP:FIRE" y enviamos base64(cypher("SHIP:SAFE") + new_iv) ?

Si originalmente:

    IV = IV

    Plaintext = "SHIP:SAFE"

    Ciphertext = Encrypt(IV XOR "SHIP:SAFE")

El ataque hace:

    New IV = IV XOR "SHIP:SAFE" XOR "SHIP:FIRE"

    Cuando se descifra: Decrypt(Ciphertext) XOR New IV
    = Decrypt(Ciphertext) XOR (IV XOR "SHIP:SAFE" XOR "SHIP:FIRE")
    = (Decrypt(Ciphertext) XOR IV) XOR "SHIP:SAFE" XOR "SHIP:FIRE"
    = "SHIP:SAFE" XOR "SHIP:SAFE" XOR "SHIP:FIRE"
    = "SHIP:FIRE"

``` python
#!/bin/env python3

from pwn import *
from base64 import b64decode, b64encode
from Crypto.Util.Padding import pad

io = remote("mothership.ctf.ritsec.club",31750)


for i in range(200):

    io.recvuntil(b"SAFE TRANSMISSION: ")
    # Server data
    safe_plaintext=pad(b"SHIP:SAFE",16)
    safe_transmission=io.recvline().strip()
    print(safe_transmission)
    data = b64decode(safe_transmission)
    iv = data[:16]
    safe_ciphertext = data[16:]

    # Our data
    fire_plaintext=pad(b"SHIP:FIRE",16)
    # Flip attack
    new_iv = bytes(iv[i] ^ safe_plaintext[i] ^ fire_plaintext[i] for i in range(16))
    fire_transmision = b64encode(new_iv+safe_ciphertext)
    io.sendline(fire_transmision)
    attack_line=io.recvline().strip()
    print(attack_line)

success(io.recv())
```

![2025-03-22-161440_817x549_scrot](https://github.com/user-attachments/assets/f8a80099-242f-43ee-babf-9f2acac6fe9b)

Obtuvimos las coordenadas. La flag especifica el formato "what.three.words" a partir de las coordenadas

https://what3words.com/ es un sitio que asigna tres palabras aleatorias a una localizacion

![2025-03-22-162848_771x348_scrot](https://github.com/user-attachments/assets/f7139172-e5c7-4b41-b0eb-58c606cb46e0)

`RS{humans.knee.barn}`
