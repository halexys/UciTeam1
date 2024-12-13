# Reverse / Flag Checker

Tras la ejecución, el binario solicita al usuario que ingrese una cadena de 4 caracteres. Un análisis rápido de la subrutina principal revela que el binario espera una cadena de 4 caracteres como argumento de la línea de comando. Esta entrada se almacenará en la variable pbInput en la sección .data.

![radare1_args2](https://github.com/user-attachments/assets/5bbc41bc-cb11-4c2a-b5f7-a22c82152f8f)

![2_comprobacion4caracters](https://github.com/user-attachments/assets/7f9f3094-277f-442e-b0c3-89ac1a262c42)

![datasection](https://github.com/user-attachments/assets/7b5a2714-e5f5-4c39-b66b-080d0f25fe74)


La siguiente sección de código realiza la verificación del argumento de la línea de comando. Antes de continuar, es importante tener en cuenta que hay una devolución de llamada TLS implementada en este binario que escribe un valor falso en pbInput en la sección .data antes de ejecutar la función principal. Si no se proporciona ningún argumento de línea de comando, el binario utilizará este valor falso de 4 bytes.

![valorpordefecto](https://github.com/user-attachments/assets/3ead5153-f5ac-4308-9004-f3f82b5b4529)

Binario en este caso tiene un recurso cifrado. Este recurso almacena un binario de Windows cifrado. La función principal leerá el contenido de este recurso en una región de memoria asignada con malloc.

Luego calcula un hash MD5 de 16 bytes de la cadena de entrada de 4 caracteres y utiliza este hash de 16 bytes como clave XOR para descifrar el recurso cifrado.

![subrutina1](https://github.com/user-attachments/assets/5eefae52-9f0f-42be-b52d-9216bb35e119)

