# Moving Money

![2025-03-24-123231_727x268_scrot](https://github.com/user-attachments/assets/98d79b9f-ffdd-49a3-aae1-c3af80e63ec8)

Vemos las transacciones de la billetera virtual en https://mempool.space/ en la red "Tesnet" y encontramos un OP_RETURN en base 64 en una de las transacciones:

![2025-03-24-123802_1136x159_scrot](https://github.com/user-attachments/assets/29ed84c3-9316-4a99-8259-5156320120ec)

Las operaciones con OP_RETURN no estan diseñadas para transferir valor, sino que se utilizan para incrustar datos en la blockchain. OP_RETURN permite almacenar hasta 80 bytes de datos.

```
echo "UlN7Q292ZXJ1cF9GdW5kc30="|base64 -d
RS{Coverup_Funds} 
```

`RS{Coverup_Funds}`
