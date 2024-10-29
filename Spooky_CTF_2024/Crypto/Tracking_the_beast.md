# Crypto / Tracking the beast

Nos dan un punto inicial (26,38), la curva eliptica  y^2 = x^3 + 73x + 42 mod 251 y el numero de comic de Linterna Verde con la portada requerida es el #49: 

![lea](https://github.com/user-attachments/assets/54038285-ade1-4aa2-9e00-1af16f80cb23)

Entonces se realiza se debe hacer una multiplicacion escalar, el punto (26,38) por el escalar 49, utilizando la operación de suma de puntos en la curva elíptica. El resultado de la multiplicación es otro punto en la curva elíptica, que representa el destino final de Bigfoot

![48](https://github.com/user-attachments/assets/4f346f88-167f-422b-9d84-9aa893a18bfa)


Usando https://graui.de/code/elliptic2/ podemos ver los puntos del campo finito generado en una curva bajo aritmética modular. Si hacemos click en el punto que nos dan como dato en la tabla de suma de puntos podremos ver el subgrupo generado por una operación de suma de puntos con él mismo X veces, de tal manera que aplicar 49 veces esta operacion nos da como resultado el punto de la flag 

`NICC{(72,17)}`
