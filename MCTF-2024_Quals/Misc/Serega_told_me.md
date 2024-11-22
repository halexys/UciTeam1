# Misc / Serega told me

Nos dan 120 operaciones matematicas , en cada una tenemos para elegir cuatro opciones, debemos escoger la mas cercana al resultado de la ecuacion:
```
......................................................................
...............=+#@@@@@@@@#%@@@@@@@@@@@@@@@@@@@@@@@@@@:::..::::::::::.
............:::+:-@#@#@#@@#-%@+*==#@-:@#%:%*@=+@=@:+@@.::.:::::::::::.
............:::=+#@@@@@@@@#%@@@@@@@@@@@@@@@@@@@@@%@@@@::::::::.::::::.
.....:@@@...-=-@@@:::@@@@%@#@@@@@@@::::@@@-@#@@@@@%@%:@@@@@@@@@@:::::.
.....:@:@::-@@@@=@.::@#@=@+#@*::#@@:::+@+@@*#+@##@#:%%@:%@@@*%@@:.::..
.:::::@@@:.=@+@@+@@@+@@@*%@*@@@@@@@:::#@@%%+*@@@@@%@#:#@@@@@@@@@:::::.
.::::::::.:-@@#@@@@@@@@@-+=+#+::#@#:::+*+=%#=:-=-:::+#*:#@%#+%@%:::::.
.:::::::::.+@@@@@-@@+-@@@%:::::--::::::=@@@@@@@@@+:::::::::-------::-.
.:-------::@@@@#@@@@@@@@@@*::---:::-::+@@@#***#%@@*---:--=+++++++=---.
.-:--==-==-@@=@@@@*%@@*@-@@------:::-=@@-%@@@@@@=@@=::-=+###**+++*###.
.+=:--::--:@@#*%@@*@@@@@@@@------++=-*%++-:::-#@@@@+:=#%%#*+==-:+*+--.
.*%*--==--:@@@=*%@%@@@@@@@@:=--=-==*++%#@@@@#-%@@@@@:*+---=+++-==:+=-.
.+-#=-:---:#@@*@@@@:%@%#%%@:-=-::=+++-*@@@@@@=@@=#@@-+*#%#=-:=+=--=-:.
.#=++*#%#+-*@@%+=:@%**#*=%*::--::::---=@@@%@@*@@#%@@-=-::+-=-:--:--:-.
.@*-+*+#%@#++@@%=-##+#=*#-::::---=*##%+@@@@@#+#+**@@=-=:-=----:--::::.
.-*+*+==+*=++-%@%-+*@*++%@@@@@@@@@@@@@@+#=--+##=-=@@%#=--+=---:::-=*@.
.-==*#*#%%*==@@@*-==#*::@@@@@@@@@@@@@@@*#=++====+=%@@@@+--=+#*====*%=.
.=---=+-:=+#@%@#+-=-=+*#@**#=---=+--+=@+@@#:=-+#@@=#@@@@-:+%**=#@@#*#.
.==--+#+-=+@@@@@++--**##+*+=++==+=-*%%@@@##*+**=--*+--@@=-=%*=++-*@@@.
.@%#@@@@@*+@@@#+==:+=+::----:---=+**-=+=-#*+==-+#%+-*@@@=:+#+=+:=-+@@.
.@@%@@@@@@@@@===:-:+=-::---:::::=*+*%%###+++--+++==-:=%*%**#+#+*=-##+.
.+##@+==#@@@+=-::---::---::::::+@@@%+==-::::--:-----::#@@@#*+@%+#:%@+.
.*=@@:=*-==*=::::-:::::::::::--@@@@@@+--::::::::-:-:::=*#@@@@@*-*#-@%.
.#-@*-*-+=++-::::::::::::--:::+@#@+:#+:---::-:-:-:::----=%@@#==--*++@.
.%*@--==-#+-:::::::--:==-==---%%-==-*#-=:::-:--:-:::--::--+*-===*%%%@.
.+-%%@@@**+-:::::=++=-=+-=+--=@%#-**#@*+=-::-:-:::-=-:---:=*=#%@@@@#%.
.++#@@@@%*=##+====:-=:=+-=+-=@@=@-*#*%@:=-::-::--:--:----:-+#@@@#=---.
.---=-+@@+--==:--=+--=-+=:=-=#@-#+=-*#@-:=::::::::-:-:=-:::-%@#+:----.
.-=-=:=@@@*#*--==:-=--=+--=:-##-+:=#%@@=:---:::::-:=-=------@@=+--=::.
.-+=:+=@@@*-:-++=--::=--::---##:--+==%@*:::-:::::---:-==-::=@@::=*-=-.
.--==-#%@@#=====-:-=-:-::--:-*#++++*%#%*+-:-=-:::::--:::--:+@+:==+*=-.
.---=+#=@@:=+:+:-=--===::::=@@@@@*@@@@++-+----::::----:::--*%+===---:.
.:+:-=+*@@=:-+-==-:=-::::--*@@@-%@*+@@:%*+-=----:::::::::::**-+#**=:-.
.-+-=+-@@#=-===-:+=-:::---:#@@@@@@@@@@@@#++*+:::--:-:::-::-*+-=*#*=::.
.-=-+**@%=-:--:+*+----:::::##@%+@#@*@@***==:+::--:-:-:-:::-=*:+-=%*--.
.-=:-:%@+=-::++=:::::::-:::#%@@@@@@#@@@@#====:::-=:-::::::--*+=-=@+=-.
......................................................................

Hello!
My calculator isn't afraid to make mistakes! Are you afraid?..

You will have 120 attempts to answer 100 mathematical equations correctly.
---------------

3 - 42 * 58  = ?

A) -915		B) -577
C) -1220		D) -1004
```

Podemos hacer un script que resuelva esto, es decir, evaluamos la operacion y calculamos el modulo del resultado obtenido con cada una de las 4 opciones, el modulo mas cercano a cero es el de la opcion mas cercana, entonces enviamos la letra de la solucion. Repetimos esto 100 veces par obtener la flag.

``` python
from pwn import *

io = remote("mctf-game.ru",4445)

# Enviamos la primera sin importar el resultado
io.recv()
io.sendline(b'A')

# La respuesta difiere un poco si se falla, corregimos esto 
correct = io.recvline().decode('utf-8')
if not 'Correct' in correct:
    io.recvline()
    io.recvline()

# Enviamos todas las demas respuestas
for i in range(100):
    mejor_opcion = 'A'
    menor_diferencia = float('inf')
    # calcular
    print(correct)
    op=io.recvuntil(b"=").decode("utf-8").strip()
    op=eval(op[:len(op)-1])
    # Sacar mejor caso
    cases=io.recv().decode("utf-8").strip()
    opciones = []
    for line in cases.splitlines():
          if line.startswith(('A)', 'B)', 'C)', 'D)')):
             partes = line.split()
             letra1 = partes[0][:1]  
             valor1 = int(partes[1]) 
             letra2 = partes[2][:1]  
             valor2 = int(partes[3]) 
             opciones.append((letra1, valor1))
             opciones.append((letra2, valor2))

# Encontrar la opción más cercana al resultado

    for letra, valor in opciones:
            diferencia = abs(valor - op)  # Calcular la diferencia
            if diferencia < menor_diferencia:
              menor_diferencia = diferencia
              mejor_opcion = letra
    io.sendline(str.encode(mejor_opcion))
    correct = io.recvline()

success(io.recv().decode('utf-8'))
```

```
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
b'Correct!\n'
[+] You deserve it: MCTF{n1k0gd4_n3_b0jsya_0sh1b4tsya}
```

`MCTF{n1k0gd4_n3_b0jsya_0sh1b4tsya}`
