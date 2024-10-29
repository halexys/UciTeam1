# Stego / Phenominal_photo

Tenemos una imagen con un zip dentro, lo extraemos y tenemos un mensaje raro y otro zip, esta vez con contraseña:

![phenom](https://github.com/user-attachments/assets/47bdee82-6723-4998-8567-6ccf07b4b77e)

Identificamos que es Alien Language con https://www.dcode.fr/identificador-cifrado:

![phenom2](https://github.com/user-attachments/assets/1511def8-703d-4725-b9da-ee3a57c47f82)
  
Nos genera esto:

![phenom3](https://github.com/user-attachments/assets/e134d1f5-3465-470a-b815-01f7c969280d)

El archivo zip tiene como nombre gps y en el mensaje nos dicen que su gps solo toma la primera letra de cada dirección a la que quieren ir. Sabiendo esto, la contraseña del zip es LUDLDRRDLULRU:

![phenomsf](https://github.com/user-attachments/assets/606b0aeb-535f-416f-824a-277f591244b3)

Nos devuelve un txt en Alien Language de nuevo, desciframos y obtenemos la flag:

![final](https://github.com/user-attachments/assets/9d08c2ac-f226-4f3c-b343-d15dc11b92e0)

`NICC{HELP_ME_FIND_THE_PLANET_B0O}`

