Me gustó mucho este reto de ingeniería inversa. Nos dan un ROM de gba, lo abrimos con un emulador de GBA como mGBA. En el juego somos una llama y tenemos que adivinar la contraseña de un cofre que resultará siendo la bandera.

![faraday1](https://github.com/user-attachments/assets/c116cd7a-af8e-464c-87be-202837329b00)

Abrimos el juego con ghidra, pero antes le instalamos esta extension para desensamblar la arquitectura SM83: https://github.com/Gekkio/GhidraBoy 

Buscamos la cadena "Wrong password!", encontraremos dos, pues hay dos funciones que hacen lo mismo pero la correcta es esta:

``` asm
                             s_Wrong_password!_1534                          XREF[1]:     FUN_1463:1522(*)  
            1534 57 72 6f        ds         "Wrong password!"
                 6e 67 20 
                 70 61 73 
```

Como se puede observar es referenciada en FUN_1463, vamos allí y buscamos la condicional que lleva al fallo

``` asm
            14d8 cd 89 12        CALL       FUN_1289                                         undefined FUN_1289(char * param_1)
            14db b7              OR         A
            14dc c2 e2 14        JP         NZ,LAB_14e2
            14df c3 22 15        JP         LAB_1522
```

Vemos que se hace una comparacion, si A no es cero entonces se continua el flujo hacia la victoria, en caso contrario se muestra al mensaje "Wrong password!". Analizamos entonces el decompilado de FUN_1289, que suponemos hace la comparación entre las cadenas

``` C
undefined FUN_1289(char *param_1)

{
  undefined uVar1;
  byte local_4;
  byte local_3;
  
  if (*param_1 == 'F') {
    if (param_1[1] == 'A') {
      if (param_1[5] == 'A') {
        if (param_1[6] == 'Y') {
          local_4 = 0;
          for (local_3 = 0; local_3 < 7; local_3 = local_3 + 1) {
            local_4 = param_1[local_3] + local_4;
          }
          if ((local_4 & 0x7f) == 0x69) {
            if (param_1[2] == param_1[4]) {
              if ((param_1[2] & 0x40U) == 0) {
                uVar1 = 0;
              }
              else if ((param_1[2] & 8U) == 0) {
                uVar1 = 0;
              }
              else if ((param_1[2] & 2U) == 0) {
                uVar1 = 0;
              }
              else if ((bool)(param_1[2] & 1)) {
                uVar1 = 0;
              }
              else if ((byte)param_1[3] < 0x41) {
                uVar1 = 1;
              }
              else {
                uVar1 = 0;
              }
            }
            else {
              uVar1 = 0;
            }
          }
          else {
            uVar1 = 0;
          }
        }
        else {
          uVar1 = 0;
        }
      }
      else {
        uVar1 = 0;
      }
    }
    else {
      uVar1 = 0;
    }
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}
```

Podemos observar claramente que los primeros caracteres son 'FA' y los ultimos 'AY'. Y aquí que la suma de todos los caracteres & 0x7f debe ser igual a 0x69. Además el tercer y quinto caracter deben ser iguales

``` C
 for (local_3 = 0; local_3 < 7; local_3 = local_3 + 1) {
            local_4 = param_1[local_3] + local_4;
          }
          if ((local_4 & 0x7f) == 0x69) {
            if (param_1[2] == param_1[4]) {
              if ((param_1[2] & 0x40U) == 0) {
                uVar1 = 0;
              }
```

Con este script de python encontramos las posibles combinaciones de los tres caracteres que nos faltan

``` python
 // solve.py
import string
# bypass  if ((local_4 & 0x7f) == 0x69)
for char_1 in string.ascii_uppercase + string.digits:
 for char_2 in string.ascii_uppercase + string.digits:
  resultado = ord('F') + ord('A') + ord('A') + ord('Y') + ord(char_1) + ord(char_2) + ord(char_2) & 0x7f == 0x69
  if resultado:
      print(f"[2] and [4]: '{char_2}'  [3]:'{char_1}'")
```

``` bash
 >> python3 solve.py
[2] and [4]: 'C'  [3]:'B'
[2] and [4]: 'B'  [3]:'D'
[2] and [4]: 'A'  [3]:'F'
[2] and [4]: '9'  [3]:'V'
[2] and [4]: '8'  [3]:'X'
[2] and [4]: '7'  [3]:'Z'
[2] and [4]: 'L'  [3]:'0'
[2] and [4]: 'K'  [3]:'2'
[2] and [4]: 'J'  [3]:'4'
[2] and [4]: 'I'  [3]:'6'
[2] and [4]: 'H'  [3]:'8'
```

Implementamos el resto de condiciones y obtenemos la combinacion correcta:
+ param[2] & 0x40 != 0
+ param[2] & 0x8  != 0
+ param[2] & 0x2  != 0
+ param[2] & 1 == 1  (LSB es 1)
+ param[3] < 0x41    (valor ASCII menor que 'A')

``` python
 // solve.py
import string

repetidos = []
unicos = []

for char_1 in string.ascii_uppercase + string.digits:
 for char_2 in string.ascii_uppercase + string.digits:
  resultado = ord('F') + ord('A') + ord('A') + ord('Y') + ord(char_1) + ord(char_2) + ord(char_2) & 0x7f == 0x69
  if resultado:
      repetidos.append(char_2)
      unicos.append(char_1)

for x in range(len(repetidos)):
 condiciones_resueltas = (ord(repetidos[x]) & 0x40 != 0)\
                         and (ord(repetidos[x]) & 0x8 != 0)\
                         and (ord(repetidos[x]) & 0x2 != 0)\
                         and not (ord(repetidos[x]) & 1)\
                         and (unicos[x] < 'A') 
 if condiciones_resueltas:
     print(f"FA{repetidos[x]}{unicos[x]}{repetidos[x]}AY")  # Flag
```

``` bash
 >> python3 solve.py
 FAJ4JAY
```

![flag](https://github.com/user-attachments/assets/453dbe2e-3859-4cda-8f4d-1aee8164aa88)

`EKO{FAJ4JAY}`
  




