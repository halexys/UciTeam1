Reto 02
Nos presenta un motor v8 de javascript:
Lo ejecutamos y vemos la definición de una función que retorna “FLAG”:


 
Analizando la función podemos observar que recibe un arreglo como parámetro y deben cumplirse 
4 condiciones para conseguir la bandera: 
 
1 - El arreglo no puede ser nulo o estar indefinido
2 - El arreglo no puede tener una extension positiva
3 - El arreglo debe heredar de Array.prototype
4 - El contenido del arreglo debe ser exactamente igual a ‘expo92’
 
Usamos el siguiente código para superar las condiciones:
Notese que hacer arr = ‘expo92’ hace que arr.length = 6 de manera implícita por lo que 
aprovechamos que en javascript podemos declarar atributos de dos formas:
- objeto.atributo
- objeto[‘atributo’]
Estas declaraciones no afectan a arr.length, que permanece negativo, entonces ahora concatenamos 
todo y llamamos a la funcion con nuestro arreglo:
Recibimos un texto en base64 , lo decodificamos con el comando base64 -d :
 Obtenemos la flag final: flag{e_Xp09y2}
