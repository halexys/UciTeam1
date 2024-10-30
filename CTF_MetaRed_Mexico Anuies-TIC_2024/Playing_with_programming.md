# Programming / Playing With Programming

Nos dan un archivo enorme de texto (en promedio 300mb de peso y unas 15000 lineas). Si filtramos con:

`grep "{" filechartpassword.txt > a`

`grep "}" filechartpassword.txt > b`

Y abrimos con un editor de texto los archivos creados observamos que en las lineas que los contienen estas llaves se encuentran entre arrobas:

`@@@@@@@{@@`

`@@@@@@@}@@`

Si extraemos algunas lineas mas, por ejemplo con:

`cat filechartpassword.txt | head -n 5 > c`

Y abrimos con un editor de texto encontramos que cada linea contiene `@@@@@@@-@@`

Entonces asumiendo que los caracteres de la flag se encuentran entre @@@@@@@ y @@, filtramos las lineas por esos caracteres, excluyendo los '-':

`grep -Po '(?<=@@@@@@@)[^-]*?(?=@@)' filechartpassword.txt` 

La flag vendra con los caracteres invertidos, asi que para formatear mejor la salida usamos tr y echo:

![programmin](https://github.com/user-attachments/assets/7c136045-d121-4dec-b471-e4fdc6591a52)

`flagmx{playing_with_letters_and_numbers}`


