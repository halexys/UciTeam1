Esto es un cifrado similar a RSA, pero vulnerable, ya que en RSA el cifrado ocurre de la manera siguiente:

`c = m^e (mod n)`

Donde c es el mensaje cifrado, m es el mensaje en texto plano, e es un numero que cumple 1 < e < φ(n) y gcd(e, φ(n)) = 1. 

Pero en el reto el cifrado es este:

`c = m^p (mod q)`


