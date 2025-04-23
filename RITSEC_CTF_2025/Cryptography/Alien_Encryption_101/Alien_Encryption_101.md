# Alien Encryption 101

![2025-03-24-110705_736x350_scrot](https://github.com/user-attachments/assets/93ad1666-72dc-4c9d-bf1c-c92d90f6c6e5)

Nos dicen que los aliens han investigado el metodo RSA, pero aun no comprenden del todo.


## Nomenclatura de RSA

`m` --> texto plano

`c` --> texto cifrado

`(p,q)` --> un par de enteros primos muy grandes

`n = p * q` --> (modulo de las operaciones de encriptacion/desencriptacion)

`phi(n) = (p-1)*(q-1)` --> (funcion phi de Euler para `n`, cantidad de enteros positivos menores a `n` y coprimos con `n`)

`e; e <= phi(n)` --> exponente de la clave publica (primo relativo a `phi(n)`)

`d; d *e = 1 mod phi(n)` --> exponente de la clave privada (inverso modular multiplicativo de `e`)

`c = m^e mod n` (operacion de cifrado)

`m = c^d mod n` (operacion de descifrado)

## Resolucion del reto

`n` = 196603733802071409961275562212278242151

`e` = 65537

`c` = 151832817966710307438243645623410737448

Entonces puesto que `m = c^d mod n` tenemos que encontrar `d`, pero `d` depende de `phi(n)`, que a su vez depende de `p` y `q`.

Pasa que normalmente `p` y `q` son muy grande, de unos 1024 o 2048 bits, lo que representa unos 104 o 308 digitos aproximadamente, y `n` por lo tanto de 2048 a 8192 bits.

La fuerza de RSA radica en la dificultad de factorizar `n` en `p` y `q`, pero al ser `n` relativamente pequeño es factorizable.

Podemos crear el algoritmo o usar sitios como https://www.factordb.com/ para factorizarlo:

![2025-03-24-112830_1363x374_scrot](https://github.com/user-attachments/assets/06508b5a-5a0c-467b-ac23-e207ddd93e75)

Tenemos `p = 879421070503884397` y `q = 223560408541749867683`, podemos hallar d y descifrar el mensaje:

``` python 
# solve.py
# Pub key
e = 65537
# Mod
n = 196603733802071409961275562212278242151
# Mod factors
p = 879421070503884397
q = 223560408541749867683
assert(p*q==n)
# Eulers phi totient
phi = (p - 1) * (q - 1)
# Ciphertext
c = 151832817966710307438243645623410737448
#Priv key
d = pow(e, -1, phi)
# Plaintext
m = pow(c, d ,n)
# Convert to bytes
byte_length = (m.bit_length() + 7) // 8
m_bytes = m.to_bytes(byte_length, byteorder='big')

print(f"m={m}")
print(f"m_bytes={m_bytes}")
```

```
python3 solve.py
m=232190557692152706
m_bytes=b'\x038\xe8\x14\xffp\xcb\x82'
```

Normalmente el mensaje se encuentra en el numero convertido a bytes, pero en este caso la flag era simplemente el numero:
`RS{232190557692152706}`




