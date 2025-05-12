# Is_it_data_or_data?

```
void main(void)

{
  char cVar1;
  do {
    cVar1 = FUN_0010286e();               // Cuando el contador llega a 7 le agrega 'g' al mensaje almacenado
    while (cVar1 == '\0') {
      cVar1 = FUN_00102f95();             // Aqui se captura y se mapea la entrada de usuario
                                          // Si es una entrada valida devuelve algo distinto de cero
    }
    DAT_00106280 = DAT_00106280 + 1;      // Se aumenta un contador
    cVar1 = FUN_00102cd1();               // Almacena las salidas del mapeo concatenandolas a un string
  } while (cVar1 == '\0');
```

Mas abajo aparece la string `inagalaxyfarfaraway`, asi que supuse que habia que producir que esta cadena se almacenace en memoria. Despues de esto el programa te devolvia la flag

El programa tecnicamente mapeaba la entrada del usuario a estos valores:
```
4 -> f
5 -> resta 1 al ultimo caracter valido (stackable)
6 -> alloc, suma 2 al ultimo caracter valido (stackable) 
7 -> a 
9 -> z
10 -> m
15 -> r
```

Esto se ve porque en `FUN_00102f95()` cuando introducimos `00111111` se llama a una funcion que muestra la cadena almacenada y termina el programa:
```
                        else {
                          uVar9 = (uint)bVar7;
                          if (local_220 == 8) {
                            iVar8 = memcmp(local_228,"00111111",8);
                            if (iVar8 == 0) {
                              FUN_001025e9();
                    /* WARNING: Subroutine does not return */
                              exit(0);
                            }
```

Solucion:
``` python
from pwn import *

#p = process('./chall')
p = remote("isitdata.chals.damctf.xyz",39531)

# Token sequence to build "inagalaxyfarfaraway"
sequences = [
    (4, 6),        # i
    (10, 6, 5, 5), # n
    (7,),          # a
    # g is automatically added after the 7th token
    (7,),          # a
    (10, 5),       # l
    (7,),          # a
    (9, 5, 5),     # x
    (9, 5),        # y
    (4,),          # f
    (7,),          # a
    (10, 6, 6, 5), # r
    (4,),          # f
    (7,),          # a
    (10, 6, 6, 5), # r
    (7,),          # a
    (9, 5, 5, 5),  # w
    (7,),          # a
    (9, 5)         # y
]

for seq in sequences:
    for token in seq:
        p.sendlineafter(b'> ', str(token).encode())

p.interactive()
# Test
#p.sendlineafter(b'> ', b'00111111')
```

`dam{I_dont_like_silicon_it_makes_cpus_and_theyre_everywhere}`







