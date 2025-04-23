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
