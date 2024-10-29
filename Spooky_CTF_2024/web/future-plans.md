Intro:

![img1](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web4/Captura%20de%20pantalla%20de%202024-10-29%2019-11-27.png)

Como vemos en la intro nos dan unas cuantas posibles pistas, el nombre del reto es planes futuros y nos dicen algo de encontrarlo
antes de la primavera.

Una vez entramos a la web, encontramos un blog con un par de sesiones, en la principal encontramos publicaciones de misiones, con 
un botón de "busqueda" pero en realidad lo único que hace es mezclar las palabras y regar el contenido de la web (sin ningún sentido)

En la sesión plans nos deja una curiosa pista: "Check back in the future to learn about my plans in the future".

En la sesión Development nos encontramos algo parecido a un control de commits de git, con fecha, hora, estado y comentarios sobre cada
uno, curiosamente hay dos de ellos con fecha 2025 (en el futuro), pero uno de ellos es en octubre (mucho después de primavera) mientras
el otro es en abril.

Ahora, que podemos hacer con esto, pues hay unas cuantas cabeceras HTTP relacionadas con la fecha, asi que por ahí iría la cosa.
Algunas de las cabeceras relacionadas con la fecha son:

1. **Date**: Indica la fecha y hora en que se generó la respuesta del servidor. Ejemplo:
```   Date: Wed, 21 Oct 2015 07:28:00 GMT```

2. **Last-Modified**: Indica la última vez que se modificó el recurso solicitado. Esto permite a los clientes saber si deben volver
a solicitar el recurso o si pueden usar una versión en caché. Ejemplo:
```Last-Modified: Tue, 15 Nov 1994 12:45:26 GMT```

3. **Expires**: Indica la fecha y hora en que el recurso se considera obsoleto. Después de esta fecha, el recurso no debe ser considerado
válido sin una nueva solicitud. Ejemplo:
```Last-Modified: Tue, 15 Nov 1994 12:45:26 GMT```

4. **Cache-Control**: Aunque no es una cabecera de fecha per se, puede incluir directivas relacionadas con la duración del caché, como max-age,
que especifica cuánto tiempo (en segundos) el recurso es considerado fresco. Ejemplo:
```Cache-Control: max-age=3600```
   
5. **If-Modified-Since**: Esta cabecera se envía en las solicitudes HTTP para preguntar al servidor si el recurso ha sido modificado desde una fecha
específica. Si no ha cambiado, el servidor puede responder con un código 304 (Not Modified). Ejemplo:
```If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT```

6. **If-Unmodified-Since**: Similar a If-Modified-Since, pero se utiliza para verificar que el recurso no ha sido modificado desde una fecha específica; si ha sido modificado, el servidor puede responder con un error 412 (Precondition Failed). Ejemplo:
```If-Unmodified-Since: Wed, 21 Oct 2015 07:28:00 GMT```
   
Y al usar la cabecera **If-Modified-Since** el servidor nos devuelve la flag:
```bash
curl -H "If-Modified-Since: 11:14:19 18 Apr 2025 EDT" https://www.niccgetsspooky.xyz/plans
```

![flag](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web4/image4.png)
