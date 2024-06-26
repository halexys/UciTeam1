Reto 02

Nos presenta un motor v8 de javascript:

![1](https://github.com/halexys/UciTeam1/assets/72656657/cb25b45d-120c-401f-b6e0-d8d7ca966136)

Lo ejecutamos y vemos la definición de una función que retorna “FLAG”:

![image](https://github.com/halexys/UciTeam1/assets/72656657/fa418d3e-b063-4aeb-8038-9c97f2daea58)

![image](https://github.com/halexys/UciTeam1/assets/72656657/9039a51f-049b-4f6b-98ae-6e833134a40b)


Analizando la función podemos observar que recibe un arreglo como parámetro y deben cumplirse 
4 condiciones para conseguir la bandera: 
 
1 - El arreglo no puede ser nulo o estar indefinido
2 - El arreglo no puede tener una extension positiva
3 - El arreglo debe heredar de Array.prototype
4 - El contenido del arreglo debe ser exactamente igual a ‘expo92’
 
Usamos el siguiente código para superar las condiciones:

![image](https://github.com/halexys/UciTeam1/assets/72656657/26a6c0c4-c33e-4422-a0b3-b5934047d4c1)


Notese que hacer arr = ‘expo92’ hace que arr.length = 6 de manera implícita por lo que 
aprovechamos que en javascript podemos declarar atributos de dos formas:
- objeto.atributo
- objeto[‘atributo’]
Estas declaraciones no afectan a arr.length, que permanece negativo, entonces ahora concatenamos 
todo y llamamos a la funcion con nuestro arreglo:

![image](https://github.com/halexys/UciTeam1/assets/72656657/f028c521-6336-4308-ac58-8df9aef36797)


Recibimos un texto en base64 , lo decodificamos con el comando base64 -d :

![image](https://github.com/halexys/UciTeam1/assets/72656657/c10a338e-07a2-4eb0-ad82-e9931fec5e8b)


 Obtenemos la flag final: flag{e_Xp09y2}
