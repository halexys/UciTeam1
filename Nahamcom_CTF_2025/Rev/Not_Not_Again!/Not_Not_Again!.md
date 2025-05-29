# Not, Not Again!

Si buscamos las referencias a la cadena "Correct! The flag is:" llegamos a una funcion donde se ve un bucle de comparacion, que imprime la cadena si todos los bytes despues de las operaciones aplicadas a una cadena en el programa son iguales a la entrada de usuario.

El script para resolverlo es este:
``` python
""""
if (lStack_20f8 == 0x26) {
      uVar7 = 0x61353fb0;
      lVar15 = 0;
      do {
      // Revisa todos los bytes
        if (lVar15 == 0x26) {
          uStack_2058 = &PTR_s_Correct!_The_flag_is:_140006530 ;
          goto LAB_140001f4d;
        }
        uVar7 = uVar7 * -0x620ff1e3 + 0x1a026a35;
        pbVar30 = (byte *)((longlong)ppuStack_2100 + lVar15);
        pbVar26 = &BYTE_140006470 + lVar15;
        lVar15 = lVar15 + 1;
      } while ((byte)((byte)(uVar7 >> 0x15) ^ *pbVar30) == *pbVar26);
    }

    (uVar7 >> 0x15) ^ *pbVar30 == *pbVar26

    lVar15 --> contador de bucle
    pbVar30 --> string hardcodeada
    pbVar26 --> entrada de usuario ?
    uVar7 --> parametro1
"""

pbVar30 = bytes.fromhex('3A772CA80A82D27F551140B662648C394EDECB8B914960A8F12FBDE5E07BDBDA7BD33304289E')
pbVar26 = []
uVar7 = 0x61353fb0

for i,b in enumerate(pbVar30):
    uVar7 = uVar7 * -0x620ff1e3 + 0x1a026a35; 
    pbVar26.append(bytes([((uVar7 >> 15) ^ pbVar30[i]) & 0xff])) 
print(b"".join(pbVar26))
```
