# Boofer

Observamos que el programa solo imprime una cadena de texto y luego acepta una entrada de datos:

![b1](https://github.com/user-attachments/assets/f1e7175f-fd15-4263-954c-11d46e79b2cf)

Usando un debbuger como radare2 vemos que existe una función sym.win:

![b2](https://github.com/user-attachments/assets/a87c3111-17a0-4f49-8951-b8f9c5f4c4d5)

En main vemos que reserva 0x20 bytes para la entrada así que el buffer overflow ocurre al byte 32 (0x20 a decimal) + 8 (bytes extra reservados en una arquitectura de 64 bits):

![b3](https://github.com/user-attachments/assets/2e5eac47-d82b-4efe-b992-747223499107)

![b4](https://github.com/user-attachments/assets/36518082-cae4-465b-9aab-6ed117832ff3)

Perfecto, ya tenemos todo, ahora nuestro payload serian los 40 bytes de offset y la direccion de sym.win para sobreescribir el retorno de main a nuestra funcion sym.win y obtenemos la flag:

![bf](https://github.com/user-attachments/assets/ba72ce13-66ee-4160-ac8f-f53cb4b9b4ea)

`NICC{Sp00ked_the_fl4g_0ut_of_m3}`
