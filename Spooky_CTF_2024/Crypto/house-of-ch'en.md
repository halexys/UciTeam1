Intro:

![img1](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/Crypto/img/image1.png)

Luego de descargarnos los archivos del reto, tenemos tres cosas, un script en perl y dos archivos de texto. De los archivos uno contenía 
un formato: ```word1_WORD2_word3_WORD4``` y el otro tenía una frase: ``` The format of japh.txt you have is right but the words are wrong. Also...who is japh?```

Si buscamos en google que es japh, nos sale en el primer enlace:

![img2](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/Crypto/img/image2.png)

Entonces supongo que sea: just_ANOTHER_perl_HACKER.

Antes de todo, hay un pequeño problema, el japh.pl esta en base64, y al decodificarlo sale la cabecera y un contenido extraño, pero 
si miramos bien, en el medio del base64 hay algo entre paréntesis ```(HEYMAYA)```, tal vez sea una clave de algo, pero si la quitamos 
tendremos el script completo:

![img3](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/Crypto/img/image7.png)

Si miramos el script, vemos que hace unas cuantas cosas raras con nuestra entrada antes de compararla con el archivo donde debe estar
ubicada la frae (file: japh.txt, content: just_ANOTHER_perl_HACKER). Así que intentaremos descubrir que hace para lograr pasarlo.

Primeramente muestra algo en pantalla y se queda esperando por la entrada del usuario para tomar el input y guardarlo en una variable:

Luego elimina el caracter de nueva linea y elimina las repeticiones de caracteres del alfabeto o numeros del 0 al 9:

```perl
chomp($s);     # elimina el caracter de nueva linea al final
$s =~ y/0-9A-Za-z/0-9A-Za-z/s; # comprueba que no hayan repeticiones seguidas de numeros ni letras
```

Comprueba que la entrada sea mayor a 216 bytes y termina el programa en caso de que no sea así:


```perl
if (length($s) <216) {  # la entrada tiene que ser mayor a 216 bytes
  print("Cease your meddling! This will be your tomb!\n"); #si es menor se cierra el programa
  exit;
}
```
Luego comienzan las modificaciones y la primera es un poco compleja, ya que usa la función substr() para obtener solo un pedazo
de la guardada en $s (nuestra cadena), el problema es que la función substr() toma generalmente tres parámetros, una cadena y dos enteros,
la cadena es de la cual vamos a obtener nuestra subcadena, el primer entero es el offset, el desplazamiento desde donde comienza la
subcadena y el segundo entero es lenght,  tamaño que tendrá la subcadena. En este caso se le estan pasando como parámetros los siguientes:
```perl
my $b = substr($s, $s-1, $s);
```
Se le pasa como subcadena la introducida por nosotros, pero como offset se le pasa la misma cadena restándole 1, y como lenght se le pasa
$s también, así que si le pasas como cadena: "just_ANOTHER_perl_HACKER", luego de este cambio nuestra cadena queda en "", nada, ya que toma 
como offset = -1 y como leght = 0.

Pero, debe existir un vacío legal en esta función, vamos a encontrarlo!

Luego de leer la documentación de substr(), encontré que en caso de pasarle una cadena como argumento donde debería ir un entro, la
función tomará, en caso de que hayan, al número que esté delante como valor, o 0. Es decir que si le pasamos "72just_ANOTHER_perl_HACKER", 
tomará 72 como valor e ignorará lo otro, y en caso de "just_ANOTEHR_perl_HACKER" tomará 0 como valor.

Así que de esta forma podemos pasar la 1ra validación, y la segunda también ya que es mas de lo mismo, ejemplo, si le pasamos:
```24sasdfasdfasdfasdfasdfjust_ANOTHER_perl_HACKER``` tomará esto como cadena, 23 de offset (24 - 1), y 24 de lenght (24 es el tamaño
de la cadena just_ANOTHER_perl_HACKER).

Después de esto, en el código vienen una serie de sustituciones a nuestra cadena:
```perl
$b =~ s/R/0/g; #sustituye todas las R por 0
$b =~ s/([H-S])/\c8/g; #convierte a minúsculas todas las letras entre H y S
$b =~ s/([i-t])/uc($1)/ge; # conviete a mayúsculas todas las letras entre i y t
$b =~ s/x/R/ge; # sustituye todas las x por R
my $d = $b;
$d =~ y/4-p/A-{/; # hace una sustitución de tipo ROT a los caracteres desde 4 a p por los caracteres desde A hasta {
```

Teniendo todo esto entendido, podemos armar nuestra carga útil (payload) para enviarla al servidor. Solo debemos seguir cada sustitución
para que luego de todas quede la letra que querramos, por ejemplo, para la "j", como al final hay un ROT donde se intercambian los caracteres
siguiendo los siguientes alfabetos:

```456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnop
ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{```

para obtener al final una j, debemos tener un ] al llegar al ROT, pero debemos ver si pasa las sustituciones anteriores, las cuales si para
ya que no afectan a este caracter. Esto debemos hacer con todos. Luego de esto así quedaría nuestro payload:

```49asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfas24sasdfasdfasdfasdfasdfsd]ufgr4ABG;8ErcXe_r;46>8E```

Como la primera validación es que el texto introducido tenga mas de 216 caracteres, agregamos un poco de basura al final, no importa ya que
luego de los dos substr() nuestro texto quedará en: ```]ufgr4ABG;8ErcXe_r;46>8E```

Mandamos el payload al servidor y nos devuelve la flag!!!

![flag](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/Crypto/img/image8.png)

