# Cuwves 2 Electric Boogaloo

![2025-03-27-144748_727x575_scrot](https://github.com/user-attachments/assets/05ea21e3-2a26-4fda-bfde-09be98c2001d)

Script de sage, ejecutar en https://sagecell.sagemath.org/
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
