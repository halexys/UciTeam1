# Volvamos a nuestra infancia


Encontramos un archivo .nds, un Nintendo DS ROM, lo ejecutamos con un emulador, en este caso desmume:

![Ctf_nds](https://github.com/user-attachments/assets/2014fde6-6908-44dc-9906-85c1464b1781)

El juego consiste en una combinacion de 6 teclas, asumimos que obtendremos la bandera si escribimos la correcta.

Para el análisis del binario usamos Ghidra con el siguiente plugin para obtener información precisa: 
https://github.com/pedro-javierf/NTRGhidra

Creamos un proyecto, importamos el archivo (seleccionamos ARM9 y NO cuando el plugin nos pregunte acerca de archivo) 
y abrimos con el debbuger:

![paso1](https://github.com/user-attachments/assets/068cb8fb-463a-4dcf-b956-6e1fc25d1707)

Dentro del debbugger usamos /Search/For Strings... y encontramos un mensaje de victoria:

![paso2](https://github.com/user-attachments/assets/28236e44-cac2-466f-a5d5-58a7dd02856c)

Entonces vamos a esa dirección de memoria (02029306) y encontramos una cross reference:

![paso3](https://github.com/user-attachments/assets/895e9d16-e376-4fbf-99b2-3a4d867a5fa4)

Vamos a esa dirección de memoria (020014e0) y encontramos dos comparaciones, una con el numero 6 y otra entre dos registros:

![paso4](https://github.com/user-attachments/assets/50f0cbd0-10ca-4608-a0ac-d12f52984d30)

Creamos una copia del archivo y usamos radare2 para cambiar ´cmpeq r5, r7´ por ´cmpne r5, r7´:

![paso5](https://github.com/user-attachments/assets/f5959426-5b01-4a25-b38f-4298e0af31b6)

Luego con una combinación cualquiera excepto la correcta y presionando Enter obtenemos la bandera:

![paso6](https://github.com/user-attachments/assets/dbb073b6-3e7a-4fdf-bbbe-da81e68361a6)

```flag{la_b4nda_3n_can41_sur}```



