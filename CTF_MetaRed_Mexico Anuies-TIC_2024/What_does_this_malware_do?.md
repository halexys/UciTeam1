# Forensic / What does this malware do?

Recibimos un disk dump o imagen de disco, listamos su arbol de directorios con fls:

![1](https://github.com/user-attachments/assets/1727b5c0-664c-4a79-b746-12fa6c83d10b)

Extraemos 'README' y 'findme' con icat:

![2](https://github.com/user-attachments/assets/c413df9f-a50a-492e-8038-37d8d6a3af1c)

Como vemos 'findme' es una traza asi que la abrimos con Wireshark e inspeccionando vemos esto:

![pdf](https://github.com/user-attachments/assets/588a9fd0-2e1f-4b28-bb08-7868b5439c45)

Lo exportamos (Archivos/Exportar Objetos/HTTP...) y revisando vemos que es un Portable Executable de Windows

![pe](https://github.com/user-attachments/assets/01ef58aa-fa80-47b8-81a2-faaf026f0fce)

Revisamos sus strings y nos fijamos que fue empaquetado usando UPX así que lo desempaquetamos:

![upx](https://github.com/user-attachments/assets/b1ec584a-ef04-4dec-95a7-00f0c32824c1)

Al ejecutarlo el binario solo muestra: 'Ok Malware infection done!'. Revisando con radare2 no aparece ninguna string determinante, por lo que inspeccionamos la declaracion de variables locales con la intrucción "/ad mov dword [rbp +" en radare2 y visualizamos un sospechoso bloque:
 
 ![block](https://github.com/user-attachments/assets/34a8203f-63ab-4b28-80fd-22583bcf22e2)

Vamos a la primera dirección de memoria en la imagen (0x1400179bd), decompilamos (instalar decompilador con 'r2pm -i r2dec') y encontramos la bandera

![img1](https://github.com/user-attachments/assets/73623cfd-24c0-4314-afce-7989aa68fbdd)

![img2](https://github.com/user-attachments/assets/a15ca9ad-f83c-48e5-addf-0d19ecd2ce24)

`flagmx{this_is_not_malware}`

