# What

El binario contiene un string largo con una serie de operaciones, un bloque de operaciones sigue la expresion regular:
 
 /?[W,H,A]+T/

El string termina con '!', que chequea que todas las operaciones llevaron a que a variable 'correct' sea 1

Nota: `La entrada de usuario nos es completamente inutil`

Para resumir, el programa selecciona 8 bytes de obj.solution secuencialmente, digamos `0x0001020304050607` y realiza un conjunto de operaciones artimeticas con un caracter de la cadena obj.what (`WHAT`), comenzando el indice en 0 y aumentando en 1 despues de cada operacion bajo modulo 4

Una cadena de operaciones puede ser `WWHWA` para modificar la entrada, esperando que al final de los calculos una `T` que compara el resultado con el valor actual de obj.solution

Debemos, con cada valor de obj.solution revertir las operaciones de cada bloque , por ejemplo si el bloque fuese `WWHWA` realizar las operaciones inversas para `AWHWW`:

``` python
def W_value(char : int,c):
    # XOR es su mismo inverso
    return char ^ what[c]

def H_value(char : int,c):
    # Inverso de la suma
    return char - what[c]

def A_value(char : int,c):
    # Inverso de la multiplicacion
    return char // what[c]
```

Obtenemos las cadenas obj.what y el string largo de operaciones:
``` python
msg = "?WAWWHT?WAAWWAHHWAWAAAT?WAAHAAHHAAT?WHAAAHAHAWWHT?WHAAHHAHAWHT?WWHHWWHAAAHHWHT?WHHHHHHHAAT?WHHHHHHWWAHHT?WHAAAHAHAWHHHHHAAHT?WHHWHHAHHAAAHAAHHHT?WHHHAHWHHHAHHHAHAAT?WAAHHAHHHAHHWHHHHHT?WHHHHAHHAHAHWHHHHHT?WHHHHHHHWAHHAHHHHHT?WAWT?WHAAAAAAAWT?WHAAHAAAWAWWT?WAAAHAWAWHHT?WAAAHHHHAT?WAHHWHAHAHT?WAHHHHWWHWHAT?WAHWHHHWHHHT?WAHHAAAHHAAHHAHHT?WHHHAHWWHAHAHAWHHAAT?WAHWHHHWAAHHHWAHHHAWT?WAHHHHHAAHHHWHAHHT?WHHHHHAHHAHHHHHAT?WHHHHHHWWHAHWHHHAHHT?WHHHHHHWHHWHWHWHHHAHT?WAAWAAAAAT?WHAAAAAWWAT?WAWWHWWHAAAAT?WAAAAWWHHHWT?WHAHHAAHWT?WHWHWAHHAHT?WHAHHWWWHWHHT?WHHAHHHHAAAWHAAWAWT?WWAWHAHHHAHHAWHAAHT?WHHAHHHHWAAHAWHHAWT?WAHHAHWAHHWHHAHWHHT?WHAHHHHWHHAWHHHWAHT?WWHWAHHHHHHHAHHHHWT?WHHWWHHWHAHHHHHHHHT?WHWHHHHHAAHWAHHHHAAHAHWHAT?WAAAAAAT?WWAAWHAWAWAT?WAAAWAHWHT?WHAHWAHAWWT?WHHHHAAT?WWHAHHHHWWWT?WHHWAWAAAHAHAHHAT?WHAAHHAHAAHAHHT?WWAHHHHHAHHHAAAT?WAHAHHHWHHAHHHWWAT?WHHHHHAWHAHHHWAHT?WHHHHHAHAHHHHHT?WHHHWHHAHHHHHHHT?WHHAHHHWAHAHAWHHAHAAHHHWT?WHAHAHWHHWHAHAAHHHHWHWHAHT?WAAAWAAT?WAAAAHT!".replace(" ","").replace("T","").split("?")[1:]
# Notese que eliminamos los caracteres ' ' y 'T' porque no nos interesan
# Usamos split('?')[1:] para dividirlo en los bloques de operaciones

what=b"WHAT"
```

Hallamos los valores de obj.solution con un depurador como radare2 (sabemos que son 61*8 bytes porque el string de operaciones tiene 61 bloques):
```
[0x7f049b2e9b40]> pcd 61*8@ obj.solution | tr -d "ULL"
#define _BFFER_SIZE 61
const uint64_t buffer[_BFFER_SIZE] = {
  0x0000000000000f54, 0x00016f4a5e260570, 0x000009bd5485c77c,
  0x000000523e921c64, 0x0000000131a573ad, 0x0000000008f0366a,
  0x000000000031923c, 0x0000000000008045, 0x0007bdd4f2f841e4,
  0x000095916508bfe9, 0x0000008be32212f8, 0x0000000096a96236,
  0x0000000008f505cc, 0x00000000002ba72f, 0x0000000000000d79,
  0x00067f100a7fe057, 0x0000165f086e2afb, 0x0000000e629b2305,
  0x000000004759f2cc, 0x0000000001067699, 0x0000000000015e23,
  0x0000000000000fed, 0x000a58a6ff5e80c3, 0x0000420719f56d10,
  0x0000000de2c53af7, 0x00000000869bf143, 0x000000000da18d18,
  0x00000000003b669b, 0x0000000000010197, 0x0002f5ff57445d00,
  0x00002d028a7a55f4, 0x00000016d07ce160, 0x000000005dc6247d,
  0x0000000002b0a9cd, 0x00000000001ee163, 0x000000000000442c,
  0x0010deb1377a1730, 0x000015288f08a6d8, 0x000000769ffa893b,
  0x0000000016c9a3fc, 0x00000000042356fe, 0x00000000001ca845,
  0x000000000000ae04, 0x002acbc4c1348ca7, 0x0000156652f56900,
  0x000000141a6b0269, 0x0000000085044ca1, 0x0000000004233d6b,
  0x000000000027cf3c, 0x0000000000003279, 0x0011ab80fced20e4,
  0x00001d631a31a393, 0x000000414d72a784, 0x000000005e787f58,
  0x0000000013497804, 0x0000000000260b58, 0x0000000000009a54,
  0x000a5d9dfc502eaa, 0x0000135ac1bc1242, 0x00000018d84f7478,
  0x000000005394c6b7
};
```

Invertimos el orden de las operaciones, ajustamos el indice y cuadramos todo:
``` python
msg = "?WAWWHT?WAAWWAHHWAWAAAT?WAAHAAHHAAT?WHAAAHAHAWWHT?WHAAHHAHAWHT?WWHHWWHAAAHHWHT?WHHHHHHHAAT?WHHHHHHWWAHHT?WHAAAHAHAWHHHHHAAHT?WHHWHHAHHAAAHAAHHHT?WHHHAHWHHHAHHHAHAAT?WAAHHAHHHAHHWHHHHHT?WHHHHAHHAHAHWHHHHHT?WHHHHHHHWAHHAHHHHHT?WAWT?WHAAAAAAAWT?WHAAHAAAWAWWT?WAAAHAWAWHHT?WAAAHHHHAT?WAHHWHAHAHT?WAHHHHWWHWHAT?WAHWHHHWHHHT?WAHHAAAHHAAHHAHHT?WHHHAHWWHAHAHAWHHAAT?WAHWHHHWAAHHHWAHHHAWT?WAHHHHHAAHHHWHAHHT?WHHHHHAHHAHHHHHAT?WHHHHHHWWHAHWHHHAHHT?WHHHHHHWHHWHWHWHHHAHT?WAAWAAAAAT?WHAAAAAWWAT?WAWWHWWHAAAAT?WAAAAWWHHHWT?WHAHHAAHWT?WHWHWAHHAHT?WHAHHWWWHWHHT?WHHAHHHHAAAWHAAWAWT?WWAWHAHHHAHHAWHAAHT?WHHAHHHHWAAHAWHHAWT?WAHHAHWAHHWHHAHWHHT?WHAHHHHWHHAWHHHWAHT?WWHWAHHHHHHHAHHHHWT?WHHWWHHWHAHHHHHHHHT?WHWHHHHHAAHWAHHHHAAHAHWHAT?WAAAAAAT?WWAAWHAWAWAT?WAAAWAHWHT?WHAHWAHAWWT?WHHHHAAT?WWHAHHHHWWWT?WHHWAWAAAHAHAHHAT?WHAAHHAHAAHAHHT?WWAHHHHHAHHHAAAT?WAHAHHHWHHAHHHWWAT?WHHHHHAWHAHHHWAHT?WHHHHHAHAHHHHHT?WHHHWHHAHHHHHHHT?WHHAHHHWAHAHAWHHAHAAHHHWT?WHAHAHWHHWHAHAAHHHHWHWHAHT?WAAAWAAT?WAAAAHT!".replace(" ","").replace("T","").split("?")[1:]

what=b"WHAT"
solution = (
  0x0000000000000f54, 0x00016f4a5e260570, 0x000009bd5485c77c,
  0x000000523e921c64, 0x0000000131a573ad, 0x0000000008f0366a,
  0x000000000031923c, 0x0000000000008045, 0x0007bdd4f2f841e4,
  0x000095916508bfe9, 0x0000008be32212f8, 0x0000000096a96236,
  0x0000000008f505cc, 0x00000000002ba72f, 0x0000000000000d79,
  0x00067f100a7fe057, 0x0000165f086e2afb, 0x0000000e629b2305,
  0x000000004759f2cc, 0x0000000001067699, 0x0000000000015e23,
  0x0000000000000fed, 0x000a58a6ff5e80c3, 0x0000420719f56d10,
  0x0000000de2c53af7, 0x00000000869bf143, 0x000000000da18d18,
  0x00000000003b669b, 0x0000000000010197, 0x0002f5ff57445d00,
  0x00002d028a7a55f4, 0x00000016d07ce160, 0x000000005dc6247d,
  0x0000000002b0a9cd, 0x00000000001ee163, 0x000000000000442c,
  0x0010deb1377a1730, 0x000015288f08a6d8, 0x000000769ffa893b,
  0x0000000016c9a3fc, 0x00000000042356fe, 0x00000000001ca845,
  0x000000000000ae04, 0x002acbc4c1348ca7, 0x0000156652f56900,
  0x000000141a6b0269, 0x0000000085044ca1, 0x0000000004233d6b,
  0x000000000027cf3c, 0x0000000000003279, 0x0011ab80fced20e4,
  0x00001d631a31a393, 0x000000414d72a784, 0x000000005e787f58,
  0x0000000013497804, 0x0000000000260b58, 0x0000000000009a54,
  0x000a5d9dfc502eaa, 0x0000135ac1bc1242, 0x00000018d84f7478,
  0x000000005394c6b7)

def decrypt(byte : int, exec_chain : str,counter):
    for action in exec_chain[::-1]:
        if action == "W":
            byte = W_value(byte,counter)
        elif action == "H":
            byte = H_value(byte,counter)
        elif action == "A":
            byte = A_value(byte,counter)
        else:
            return "err"
        counter = (counter - 1) % 4
    return chr(byte %0xff)

def W_value(char : int,c):
    return char ^ what[c]

def H_value(char : int,c):
    return char - what[c]

def A_value(char : int,c):
    return char // what[c]


flag =  ""
for i in range(len(msg)):
    what_idx = (len("".join(msg[:i+1]))-1) % 4
    flag += decrypt(solution[i],msg[i],what_idx)

print(flag)
```

`bctf{1m_p3rplexed_to_s4y_th3_v3ry_l34st_rzr664k1p5v2qe4qdkymerr`


