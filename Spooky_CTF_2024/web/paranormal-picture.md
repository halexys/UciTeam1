Intro:

![img1](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web2/image1.png)

Aquí tenemos una web, con algunas imágenes raras y un input para introducir una url de un "blog" el cual debería cargar una vez
introducida la url.

![img2](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web2/image3.png)

Intenté aglunas cosas pero no cargó nada.
En el reto también nos comparten el backend, escrito en python y usando flask, y si le echamos un vistazo vemos par de cosas interesantes:

Primeramente una función que verifica si la url es válida para la aplicación o no:

```python
def verifyBlog(url):
    blog_list = ["blog","cryptid","real","666",".org"]
    for word in blog_list:
        if word not in url:
            return False
    return True
```

Para que la url sea válida, tiene que contener en ella cada una de las palabras de la lista blog_list.

Más abajo se define lo que sucede si hay una petición a la ruta /flag:

```python
@app.route('/flag')
def flag():
    if request.remote_addr == '::ffff:127.0.0.1' or request.remote_addr == '::1':
        return render_template('flag.html', FLAG=os.environ.get("FLAG"))

    else:
        return render_template('alarm.html'), 403
```

Aquí se verifica que la petición solo sea realizada desde el propio servidor, en caso contrario devuelve una plantilla de alarma.

Así que la vulnerabilidad a explotar en este caso es un SSRF (Server Side Request Forgery), que consiste en abusar de alguna funcionalidad
mal configurada para hacer que el servidor realice peticiones controlas por nosotros, en este caso para que realice una petición al propio
localhost:

```http://localhost/flag?blogcryptidreal666=.org```

El parámetro tramitado es para lograr pasar la validación de url del comienzo, si ponemos esta url en el campo de búsqueda:

![flag](https://github.com/halexys/UciTeam1/blob/main/Spooky_CTF_2024/web/img/web2/image2.png)

Obtenemos la flag!.
