El programa nos pide introducir código para insertarlo en template.rs pero tiene restricciones, que se pueden ver en runner.py

``` bash
 nc localhost 1337
Input your code to insert into template.rs.
One expr!
> let a = 1
This is too complicated, make it simpler! ('=' symbols are not allowed)
```

``` rust
// template.rs
fn safe_function() {
    /// *** YOUR CODE *** ///;
}

fn main() {
    let flag = "/// *** MY FLAG *** ///";

    safe_function();
}
```

El programa toma nuestro código, lo copia en safe_function(), copia la flag en la variable del mismo nombre y compila el programa. Entre los caracteres permitidos se notan "_!()", esto indica que se pueden usar [macros](https://doc.rust-lang.org/reference/macros.html)


``` python3
# runner.py
ALLOWED_CHARACTERS = string.ascii_letters + string.digits + " _!()"
if any(c not in ALLOWED_CHARACTERS for c in code):
    disallowed = set(c for c in code if c not in ALLOWED_CHARACTERS)
    print(f"This is too complicated, make it simpler! ('{''.join(disallowed)}' symbols are not allowed)")
    exit(1)
```

Entonces estas son las macros importantes para el proceso:

+ [file!()](https://doc.rust-lang.org/std/macro.file.html) : Devuelve al nombre del archivo en la cual fue invocada

+ [include_str!(archivo)](https://doc.rust-lang.org/std/macro.include_str.html): Devuelve un archivo codificado en UTF-8 como una cadena

+ [dbg!(expresion)](https://doc.rust-lang.org/std/macro.dbg.html) Imprime el valor de una expresión, junto con información sobre el archivo, la línea y la expresión misma

Juntando estas tres:
+ file!() obtiene la ruta del archivo e el que se encuentra
+ include_str!(file()) guarda en una string el codigo fuente del codigo
+ dbg!(include_str!(file())) lo imprime en pantalla

``` bash
 nc localhost 1337
Input your code to insert into template.rs.
One expr!
> dbg!(include_str!(file!()))
[/tmp/main.rs:3:5] include_str!(file!()) = "\nfn safe_function() {\n    dbg!(include_str!(file!()));\n}\n\nfn main() {\n    let flag = \"wwf{REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED}\";\n\n    safe_function();\n}\n"
```
