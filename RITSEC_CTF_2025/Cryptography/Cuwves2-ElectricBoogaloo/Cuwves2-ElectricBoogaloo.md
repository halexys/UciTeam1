# Cuwves 2 Electric Boogaloo

![2025-03-27-144748_727x575_scrot](https://github.com/user-attachments/assets/05ea21e3-2a26-4fda-bfde-09be98c2001d)

Debemos determinar el j-invariante de la curva final resultante de un camino de isogenias.

Tenemos un campo finito bajo modulo `p^2`, la profundidad del camino `n=4` y un grado de isogenias `l=3`

La curva supersingular inicial es `y^2 = x^3 + 3x + 1` y una curva intermedia en el camino isogenico es `y^2 = x^3 + 243x + 729`. En criptografía con isogenias, todas las curvas supersingulares están conectadas en un grafo (volcán). Si E_start y E_mid son supersingulares, existe un camino entre ellas.

El kernel se da de la forma (x, y, z) que representa en coordenadas proyectivas los puntos (x/z,y/z) = (1/0,0/0), lo cual no es posible, entonces este es un kernel trivial y (0 : 1 : 0) representa el punto en el infinito, para construir una isogenia el kernel no puede ser trivial. Este dato es irrelevante para la solucion.

El dato que nos dan de "una curva intermedia en el camino isogenico" nos da a entender que el camino isogenico comenzó, por lo que la usaremos como curva inicial.

El camino isogenico para el reto se resume en:

1 - Elegir la profundidad de camino

2 - Elegir el grado de isogenia (l)

3 - Tomar una curva inicial

4 - Tomar los puntos de orden l en la curva actual

5 - Si solo hay un punto de orden l (punto al infinito o trivial) saltar al paso 10

6 - Tomar el primer punto no trivial como generador

7 - Construir una nueva isogenia de la curva actual a la siguiente usando el kernel generador

8 - Actualizar la curva actual para que apunte a la nueva curva obtenida despues de aplicar la isogenia

9 - Regresar al paso 4

10 - Calcular el j-variant de la ultima curva obtenida

Afortunadamente para calculos con curvas elipticas podemos usar SageMath, una libreria y sistema algebraico coputacional muy poderoso construido sobre paquetes matemáticos como NumPy, Sympy, PARI/GP o Maxima

Script de sage (ejecutar en [el sitio oficial de SageMath](https://sagecell.sagemath.org/))
``` sage
p = 4049
F = GF(p^2, name='a')
l = 3
n = 4

# Starting curve (supersingular)
E_start = EllipticCurve(F, [3, 1])
j_start = E_start.j_invariant()

# Leaked midpoint curve (supersingular)
E_mid = EllipticCurve(F, [243, 729])
j_mid = E_mid.j_invariant()

# Find a point of order l on E_mid to continue the walk
E_current = E_mid
for _ in range(n):
    # Find a point of order l (non-trivial kernel)
    points = E_current(0).division_points(l)
    if len(points) <= 1:
        break  # No more l-isogenies
    kernel = points[1]  # Take first non-trivial point
    
    # Compute l-isogeny
    phi = E_current.isogeny(kernel)
    E_current = phi.codomain()

# Final j-invariant
secret_j = E_current.j_invariant()
print(f"RS{{{secret_j}}}")
```

`RS{3002}`
