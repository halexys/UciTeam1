# Crypto / Tracking the beast

Nos dan un punto inicial (26,38), la curva eliptica  y^2 = x^3 + 73x + 42 mod 251 y nos describen la portada de un comic de Linterna Verde que resulta ser el #49: 

![lea](https://github.com/user-attachments/assets/54038285-ade1-4aa2-9e00-1af16f80cb23)

Efectivamente (26,38) pertenece al campo finito generado

`(y^2 = x^3 + 73x + 42 mod 251) para y=38 y x=26`

`y^2 mod 251 = x^3 + 73x + 42 mod 251 `

`38^2 mod 251 = 26^3 + 73*26 + 42 mod 251`

`1444 mod 251 = 19516 mod 251`

`189 = 189`

Entonces se debe hacer una multiplicacion escalar, el punto (26,38) por el escalar 49, utilizando la operación de suma de puntos en la curva elíptica. El resultado de la multiplicación es otro punto en la curva elíptica, que representa el destino final de Bigfoot

![48](https://github.com/user-attachments/assets/4f346f88-167f-422b-9d84-9aa893a18bfa)


Usando https://graui.de/code/elliptic2/ podemos ver los puntos del campo finito generado en una curva bajo aritmética modular. Si hacemos click en el punto que nos dan como dato en la tabla de suma de puntos podremos ver el subgrupo generado por una operación de suma de puntos con él mismo X veces, de tal manera que aplicar 49 veces esta operacion nos da como resultado el punto de la flag.

Otra solucion es este script de python:
``` python
from ecdsa.ellipticcurve import CurveFp, Point
name="Curve"
p=251
a=73
b=42
x=26
y=38
assert (y*y) % p == (x*x*x + a*x + b) % p
curve = CurveFp(p,a,b)

P = Point(curve,x,y)
n=49
PF = P * n

print(f"P Final: ({PF.x()},{PF.y()})")
```

`NICC{(72,17)}`
