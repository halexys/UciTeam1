# Intercepted Transmission

![2025-03-24-101147_800x490_scrot](https://github.com/user-attachments/assets/99b59ac4-a342-43b6-bfc5-ac8a49855472)

En la traza hay paquetes ICMP de tipo echo (8) que envian una carga util de 1 byte que pertenece a la flag, en orden:

```
tshark -r transmission.pcapng -Y "icmp.type == 8 and data.len == 1" -x | grep 0020 | cut -d " " -f 13 | tr -d "\n"| xxd -r -p
RS{Its_A_Coverup}
```

`RS{Its_A_Coverup}`
