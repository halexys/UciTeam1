# Forensic / Too Hidden

Tenemos una captura de red y observándola con wireshark o tshark lo único relevante son unos paquetes ICMP

![icmp](https://github.com/user-attachments/assets/05aa0422-be80-43d8-9af3-e397f6389422)

Todos tienen la misma extensión y tipo, lo único que cambia son los dos bytes de Data y por supuesto los checksums. Los dos bytes de Data forman un patrón representado con tres valores (32, 45 y 46). Estos valores llevados de decimal a ASCII representan los caracteres 'SPACE', '-' y '.'. Esto es código Morse (https://en.wikipedia.org/wiki/Morse_code)

Extraemos cada valor y lo convertimos a ASCII, para eso usé este (no muy bello) one-liner en bash

``` bash
 tshark -r chall.pcapng -x | grep -E '*f\.*[0-9]{2}' | tr '.' ' '| awk {'print $15'} | while read -r line; do for decimal in $line; do printf \\$(printf '%03o' $decimal); done; done
 .-- .-- ..-.  .... --- .-.. -.-- ..--.- ... .... . . . . - ..--.- -.-- --- ..- ..--.- -.-. .- -. ..--.- ..-. .. -. -.. ..--.- -- . ..--.- ..--.. ..--.. ..--.. ..--.. ..--.. ..--.. ..--.. ..--.. ..--.. ..--..
```

Decodificamos el codigo Morse y obtenemos la flag

![holly](https://github.com/user-attachments/assets/70844a9c-9380-4109-ac43-b9924e237a86)

`WWF{HOLYSHEEEET_YOU_CAN_FIND_ME??????????}`
