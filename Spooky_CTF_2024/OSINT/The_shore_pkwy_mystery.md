# OSINT / The shore pkwy mystery

Por el titulo buscamos 'queens shore parkway' en Google:

![compa](https://github.com/user-attachments/assets/9a0eb313-c956-4a11-a3e4-d9f4071ed2ce)

Es un pequeño tramo de Belt Parkway y se encuentra cerca de la salida 17N-S

![exit17](https://github.com/user-attachments/assets/ee1099b2-90e9-4a72-99ce-e7aabf6d57b7)

Buscando en google 'belt parkway exit 17 lights' encontramos una publicacion en Reddit: https://www.reddit.com/r/AskNYC/comments/2qajk7/what_are_those_lights_along_the_belt_parkway_east/

Encontramos la primera parte, el identificador único resulta ser un código IATA, un identificador único asignado por la International Air Transport Association (IATA) a cada aeropuerto en el mundo

![part1](https://github.com/user-attachments/assets/0689c5b8-b32b-48e9-975c-d7a7d31c5300)

La parte dos se refiere a las pistas de aterrizaje del JF que son indicadas por estas luces:

![runway](https://github.com/user-attachments/assets/3a60f239-4747-4014-8c23-014227615164)

La parte tres nos dice que el 13 de octubre de 2024 entre las 7:47pm  y 7:48pm hora local se realizó una operación (despegue o aterrizaje de un vuelo). Aqui tenemos que rastrear el vuelo a esa fecha y hora exacta que pasaba por belt parkway, necesitamos la hora en UTC(11:47pm -11:48pm):

https://globe.adsbexchange.com/?replay=2024-10-13-23:47&lat=40.639&lon=-73.876&zoom=16.6

![dal386](https://github.com/user-attachments/assets/7a0d8eaa-6474-4a3b-8d7e-433a214f3aff)

![dal386-2](https://github.com/user-attachments/assets/9d2c68c9-93a2-44da-ac41-e06e82e369a7)

Y el numero final es el identificador del vuelo, el 386

`NICC{JFK,13,386}`

