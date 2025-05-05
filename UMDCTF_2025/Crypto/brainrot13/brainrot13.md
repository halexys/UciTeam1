# Brainrot13

Se añade un padding cíclico 'OAEP' al mensaje y se cifra la flag y ROT13(flag) con RSA.

Tenemos un `n` demasiado grande para factorizar, asi que no podemos encontrar `d`.

Se puede aplicar Coppersmith Attack para romper el cifrado y recuperar el contenido de la flag

Condiciones para aplicar Coppersmith Attack:
1. **Exponente publico pequeño** (e=3 en nuestro caso)
2. **Parte del mensaje conocida** (Conocemos "UMDCTF{" y "}")
3. **Incertidumbre pequeña**: x<N(1^e)
4. La incognita `x` debe poder aislarse con un desplazamiento (Los bytes desconocidos deben estar contiguos, en nuestro caso es correcto)



#### Demostración de la 3era condicion
N es de 2048 bits

N^(1/3) ≈ 2^(2048/3) ≈ 2^(682)

x son 20 bytes (28 - 8 bytes de b"UMDCTF{}" ), x = 2^(20*8) = 2^160

2^160 < 2^682

Entonces x < N(1^e)

#### Aplicacion del ataque en un script de Sage
```sage
n = 96685821958083526684938680238271304286887980859392922334047044570819254535637534763165507014186569373580269436562287115575895071477094697751185058766474544708343165263644182297048851208627306861544906558700694910255483830223450427540731613986917757415247541102253686241820221043700623282515147528145504812161
ct1 = 31415617614942980419493801728329478459882170524654275330189702271291172239569974917796230082992620119324013322311500280165046115132115888952730272833129650105740565501270236988682510607126061981801996717672566496111413558704046446132351270004211376270714769910968931266620926532143617027921568831958784579911
e = 3

def long_to_bytes(n):
    if n == 0:
        return b'\x00'
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

def bytes_to_long(b):
    return int.from_bytes(b, 'big')

flag = b'UMDCTF{' + b'\x00'*20 + b'}'  # x como bytes nulos para que no tenga valor numerico en el padding

assert len(flag) == 28


while (len(flag) < 120):
        # Optimal Asymmetric Encryption Padding
        flag += b'OAEP'

pt = bytes_to_long(flag)
padding = flag[28:] # 28 porque incluimos b"}" en el padding
l = len(padding)

# Crear variable x para polinomios definidos bajo modulo n
PR.<x> = PolynomialRing(Zmod(n))
f = (x * 256^l + pt)^3 
f = f - ct1
# Normalizar el polinomio
f = f.monic()
# Hallar raiz pequeña (x, el contenido de la flag)
flag = int(f.small_roots()[0])
print(long_to_bytes(flag))
```

`UMDCTF{shouldverotatedtwice}`



