# Misc / Read the rules

En el codigo fuente de la pagina de las reglas (https://ctf.cert.unlp.edu.ar/rules_prizes) encontramos comentarios con letras, comenzando con \<!--Z--> que se van alejando cada vez mas del inicio (<!--). Los extraemos en ese orden y decodificamos la base64 para obtener la flag:

```
curl -s https://ctf.cert.unlp.edu.ar/rules_prizes | grep -e '^<!-' | tr " " "-"   | awk '{ print length, $0 }' | sort -n | cut -d" " -f2- | tr -d '\<\>\!-' | tr -d "\r\n" | base64 -d
flag{T3xt-Pl41n-c0mm3nt5-4r3-4w3s0m3}
```

`flag{T3xt-Pl41n-c0mm3nt5-4r3-4w3s0m3}`
