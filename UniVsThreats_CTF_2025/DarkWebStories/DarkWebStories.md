# Dark Web Stories

```
 file conversation_dump.pcap
conversation_dump.pcap: pcap capture file, microsecond ts (little-endian) - version 2.4 (Ethernet, capture length 262144)
```

Si revisamos el contenido de las peticiones HTTP con `tshark -r conversation_dump.pcap -Y "http" -T fields -e text` encontramos una conversacion en la que mencionan que encontraron un archivo secreto pero la contraseña son un monton de strings.

Estos strings son hashes MD5 de la contraseña, si revisamos en https://crackstation.net:

![2025-05-04-221959_1360x609_scrot](https://github.com/user-attachments/assets/aa7028fa-83f0-419f-97d5-6238394ef507)


Con un script de python usando fuerza bruta podemos encontrar la contraseña completa:
```python
import string
import hashlib

book = string.printable

hashes = [
    "50f4646135205fd4a5417e460cf71d3c",
    "eb22cfa0890a2df3177966854a7176bc",
    "845f49aa19c955b849d57593bf09d224",
    "87f63931da79aa969ac4a776ce6cfb03",
    "9793d9d6041c80f46ad7c1f530c8bbf8",
    "2f88d89a8f50426a6285449be3286708",
    "61bd22f017588208a0cacdf9a1a7ca1e",
    "a7623c8b76316e10538782371b709415",
    "c6cca42180caba17e9e6882dc66cc6ee",
    "7c854900e46ebc5ee5680032b3e334de",
    "ac81882b848b7673d73777ca22908c0d",
    "4ce97d67963edca55cdd21d46a68f5bb",
    "4abb62a00bccb775321f2720f2c7750b",
    "67e00e8ef738fe75afdb42b22e50371e",
    "b561052e5697ee5f1491b5e350fb78e1"
]

flag = "Sup3r"

for h in hashes:
    for c in book:
        hash = hashlib.md5((flag+c).encode()).hexdigest()
        if hash == h:
            flag += c
            print(f"{flag}    {hash}")
            break

print("Flag: UVT{" + flag + "}") # Pensaba que era la flag pero no XD
```

Asi que extraemos los archivos del trafico HTTP:
```
 tshark -r conversation_dump.pcap -Y "http.request.method == GET" --export-objects http,get_files/
    4   0.000248    127.0.0.1 → 127.0.0.1    HTTP 664 GET / HTTP/1.1
   22  13.418974    127.0.0.1 → 127.0.0.1    HTTP 586 GET /robots.txt HTTP/1.1
   40  26.644180    127.0.0.1 → 127.0.0.1    HTTP 585 GET /index.php HTTP/1.1
   52  32.375518    127.0.0.1 → 127.0.0.1    HTTP 586 GET /index.html HTTP/1.1
   64  35.032266    127.0.0.1 → 127.0.0.1    HTTP 727 GET /admin.html HTTP/1.1
  146 105.742030    127.0.0.1 → 127.0.0.1    HTTP 586 GET /backup.tar HTTP/1.1
  158 108.648821    127.0.0.1 → 127.0.0.1    HTTP 586 GET /backup.zip HTTP/1.1
  170 111.743888    127.0.0.1 → 127.0.0.1    HTTP 587 GET /backup.html HTTP/1.1
  182 127.517327    127.0.0.1 → 127.0.0.1    HTTP 593 GET /backup_files.html HTTP/1.1
  194 156.546426    127.0.0.1 → 127.0.0.1    HTTP 587 GET /secret.html HTTP/1.1
  206 164.857110    127.0.0.1 → 127.0.0.1    HTTP 587 GET /hidden.html HTTP/1.1
  218 172.273619    127.0.0.1 → 127.0.0.1    HTTP 589 GET /register.html HTTP/1.1
  230 176.791395    127.0.0.1 → 127.0.0.1    HTTP 687 GET /admin.html HTTP/1.1
  252 195.526262    127.0.0.1 → 127.0.0.1    HTTP 678 GET / HTTP/1.1
  316 226.071125    127.0.0.1 → 127.0.0.1    HTTP 628 GET /hidden/ HTTP/1.1
  328 251.103829    127.0.0.1 → 127.0.0.1    HTTP 644 GET /hidden/secretdata.zip HTTP/1.1
```

Descomprimimos `secretdata.zip` con la contraseña y nos devuelve una foto:

![hacker](https://github.com/user-attachments/assets/194dd1ff-2405-4090-89fb-e508243b5c72)

La flag fue ocultada en la imagen usando LSB en el byte azul:
```
zsteg --lsb hacker.png
imagedata           .. text: "8;:59:$%%"
b1,b,lsb,xy         .. text: "UVT{4_l0T_0f_lay3r5_70_unc0v3r_1nn1t?}"
b1,bgr,lsb,xy       .. text: "[lm'cR5kv7+QKd"
b2,rgb,lsb,xy       .. file: OpenPGP Public Key
b2,bgr,lsb,xy       .. file: OpenPGP Public Key
b4,r,lsb,xy         .. text: "\"$5D33C44DDDDDC33D3D3D3D3D3EDDDCDDDDTETUDDEUUUeU3U3U3U3UUUDDDDEE3U3U3U33\"U3U3U2#253CB334DDDDDDDDDEh"
b4,g,lsb,xy         .. text: "UWhwffvggwwwwwvf"
b4,b,lsb,xy         .. text: "uE2\"3DUEU\"2##UUDSDEETU4ETwvFw"
```

`UVT{4_l0T_0f_lay3r5_70_unc0v3r_1nn1t?}`

