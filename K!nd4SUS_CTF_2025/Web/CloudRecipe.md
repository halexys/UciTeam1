# Cloud Recipe

![2025-03-16-104024_1340x517_scrot](https://github.com/user-attachments/assets/ba8e0991-be72-4462-8d04-b1943cae2d12)

Nos encontramos en un sitio para subir y guardar recetas. Vamos a /register y creamos una cuenta.
A partir de aqui podemos crear recetas en /create_recipe, verlas en /recipes, y enviar al administrador para que las revise el id de una receta nuestra en /send_recipe.

![2025-03-16-104213_681x571_scrot](https://github.com/user-attachments/assets/1772e914-96c4-44a6-8268-0bd70053c0a8)

![2025-03-16-104325_689x629_scrot](https://github.com/user-attachments/assets/41d40b89-cc20-4419-b4d5-09b279ca432f)

![2025-03-16-104351_691x582_scrot](https://github.com/user-attachments/assets/b19d6d10-f648-4221-af00-54865309f20f)

Aqui intentamos diferentes tipos de ataques XSS pero todas fueron bloqueadas debido al Content Security Policy de la pagina, el cual podemos ver en el codigo fuente que nos ofrecen. Tambien podemos subir archivos pero estos no seran relevantes en el reto.

```
  Content-Security-Policy
	script-src 'nonce-kOa0etvnClbdzUC_1NdVvBreNd7sixQ0'; style-src 'self' 'nonce-kOa0etvnClbdzUC_1NdVvBreNd7sixQ0'; default-src *
```

``` python
csp = {
    'script-src': '',    
    'style-src': ["'self'"],       
    'default-src': ['*']
}

Talisman(app,
         force_https=False,
         session_cookie_secure=False,
         content_security_policy=csp,
         content_security_policy_nonce_in=['script-src', 'style-src']
)
```

Le pasamos este CSP a https://csp-evaluator.withgoogle.com/ para ver si hay alguna posible configuracion vulnerable:

![2025-03-16-104937_822x272_scrot](https://github.com/user-attachments/assets/ca15505b-f1e0-4067-a722-32d7a74e9ab3)

Observamos que podemos cargar cualquier base-uri, lo que nos permite cambiar la direccion base de cualquier src en la pagina a la del sitio que queramos. Con esto probamos a crear una receta nueva. Usamos un subdominio de neocities.org, sitio que permite hospedar paginas web (aunque solo el frontend) de manera gratuita.

![2025-03-16-105846_572x502_scrot](https://github.com/user-attachments/assets/ce9039fd-af5c-4414-8bf8-c5c623aed91b)

![2025-03-16-105909_955x108_scrot](https://github.com/user-attachments/assets/c50b8793-fc49-4170-af20-9fe811a7c2d4)

Podemos observar que el script /static/js/image.js ahora es llamado de nuestro sitio trampa. Perfecto, ahora observemos el comportamiento del bot que revisa nuestras recetas:

``` python
def admin_bot_visit(recipe_id):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) CTF-Admin-Agent"
        )
        
        context.add_cookies([{
            "name": "flag",
            "value": SECRET_FLAG,
            "domain": "127.0.0.1",
            "path": "/",
            "httpOnly": False
        }])
        
        context.set_extra_http_headers({"X-Bot-Token": BOT_TOKEN})

        page = context.new_page()
        url = f"http://127.0.0.1:5000/admin/recipe/{recipe_id}"
        page.goto(url)
        page.wait_for_load_state("networkidle")
        browser.close()
```

El bot administrador contiene la flag en la cookie value pero solo es para su dominio, tambien podemos ver el HttpOnly en false, lo que significa que se puede acceder a las cookies desde el javascript cliente. Ahora hay que tener en cuenta que:
` Al cambiar la URI base con nuestra receta ese sitio es considerado el dominio principal, entonces el bot enviara la cookie al acceder a este.`

Entonces lo que hicimos fue crear la ruta en nuestro subdominio de neocities.org y hacer un fetch a un webhook en https://webhook.site/ enviandole las cookies:

![2025-03-16-110734_1362x288_scrot](https://github.com/user-attachments/assets/9e4e6360-6aa0-4b80-84c1-3d295d2ddc90)

Enviamos el id de nuestra receta al bot para que la revise y revisamos nuestro hook para ver la peticion:

![2025-03-16-111029_1306x295_scrot](https://github.com/user-attachments/assets/a0f92cc3-fc1c-4e6e-ae67-561595ad81f6)

![2025-03-16-111057_1366x768_scrot](https://github.com/user-attachments/assets/f0f02584-00ea-482e-b780-1a458b12b1e8)

`KSUS{0h_n0_m4_l4546n4_r3c1p3}`




