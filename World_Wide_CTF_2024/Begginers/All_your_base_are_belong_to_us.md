# Begginers / All your base are belong to us.

Tenemos el siguiente texto codificado:

MkpIbmdFcWs4MzVjR3BHRXFVVnZtZWJUQWtSTlNNamE1dGZYQTdwR25ac203SnJQV2FyTUdHQnA3Uk1XZDNZVFlTNTJjemVya1BCN0dBY2NBNkN4U1VBS29TalVBOU1tR1EyYUF0UVlHZTFYOXp1TThWS2o1OHdKRFJaVXhzTGRaZUpaTGV6NUFWc2JHdm5CbTdjV28yNTRyWGpzQURYdEhkSmJmWmtGREVEQWZWeEhFeDNYanNNODZMZVo2cnM2NExGbU5QeG1mUXBqQ3BoY3pCczlRa3kySnFZb1JzSnFtUnk0cW02WFgyOU50N1g2Vg==

Usando [cyberchef](https://cyberchef.io/) y su operación Magic, con la secuencida de operaciones FromBase64 -> FromBase58 -> FromBase32 -> FromBase85 podemos sacar unos caracteres que parecen chinos

𔕷𠅦𖥣桢顲桨鑦敤𓅥𓉮鵟𔐴鐳ꌴ鑬鵴鐳𐘴𔕳𓀳鑳𔔴敧栴鬲ᕽ

En la descripción del reto se alude a base 2^16 o base 65536, usando este [decodificador](https://www.better-converter.com/Encoders-Decoders/Base65536-Decode) extraemos la flag

`wwf{cyb3rch3f_d0esnt_h4v3_4ll_th3_4nsw3rs_4wg0432f}`
