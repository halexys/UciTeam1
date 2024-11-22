# PWN / Achilles

Nos dan el codigo fuente y podemos ver que la funcion 'conquer()' devuelve la flag y que podemos ejecutar funciones por medio de eval, aunque no especificamente la que necesitamos. Tambien tenemos otras restricciones, debe ser un identificador valido en python y no puede ser una palabra reservada:
        
``` python
if not function.isidentifier():
    sys.exit(f'Invalid identifier: {function!r}')
elif iskeyword(function) or issoftkeyword(function):
    sys.exit(f'Reserved identifier: {function!r}')
elif function == 'conquer':
    sys.exit('Option [conquer] is temporarily unavailable!')
```

