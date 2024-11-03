# Steg / Photo clue

Tenemos un zip que contiene un Windows Event Trace Log, entonces buscamos imagenes jpg dentro de la memoria con Volatility:

`vol -f Challenge3.raw windows.filescan | grep ".jpg"`

Vemos esto:

![redacted](https://github.com/user-attachments/assets/fe4a373c-ceb5-4438-9a2c-dc7cadbade63)

Lo extraemos:

`vol -f Challenge3.raw -o "./output" windows.dumpfiles --virtaddr 0xb70fca699c30`

Intentamos extraer datos con steghide y encontramos un pdf:

![pdf](https://github.com/user-attachments/assets/0218e390-188b-4d02-afab-88c0c4a86096)

El pdf está protegido por contraseña, lo crackeamos con john o hashcat:

![ha2](https://github.com/user-attachments/assets/201eba51-b39f-4f84-9279-eda5fd83a0a0)

El pdf contiene un mensaje en binario, lo decodificamos y obtenemos la flag:
  
![final](https://github.com/user-attachments/assets/1c2fafc8-b517-4357-bdfb-18780385d145)

`NICC{M0rse_Ph0t0_S3crets}`
