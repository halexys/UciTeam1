# Stego / Can you find my account number ?

Recibimos un archivo MP3, pero tiene la firma de un PDF que al abrirlo no contiene informacion relevante. Buscamos archivos embebidos con binwalk y encontramos un mensaje PGP

![b1](https://github.com/user-attachments/assets/c923a8c9-1646-412b-82ef-89703d5b7418)

La extraccion con binwalk falla, así que lo hacemos manualmente, en mi caso usé vim:

![vim](https://github.com/user-attachments/assets/55203a94-edb4-4a90-a58b-5b911c9b9c09)

![vim2](https://github.com/user-attachments/assets/c5bb6e30-353e-4df3-b918-f601e675058f)

Necesitamos una contraseña. Recordamos que en el reto se dice que ocultó la clave en un GIF dentro del PDF, y buscando manualmente encontramos una cabecera GIF89a pero con '1' en lugar de 'I':

![gif](https://github.com/user-attachments/assets/cc587845-366f-473c-b0f4-06074c6f8948)

Cambiamos ese caracter para arreglarlo y eliminamos la cabecera y los metadatos del PDF, que son las 1633 lineas, hasta '%%EOF', justo antes de la cabecera del GIF. Puedes optar por hacerlo con un editor de texto o dd para mayor precisión.

![dd](https://github.com/user-attachments/assets/b4c1c938-0574-4945-8f2c-fb7678a76527)

Herramientas como hexdump y xxd usan un offset en hexadecimal, el offset de el salto de linea '.' despúes de EOF es 76920+8, lo cual en decimal es 485664+8=485672, que es la posicion a partir de la cual escribiremos en el nuevo archivo, con un block size de 1 byte

Abrimos el GIF y nos muestra la clave para el mensaje GPG:

![key](https://github.com/user-attachments/assets/0f6d2f12-22f0-4bb4-83b1-94502eda9509)
  
Desencriptamos con gpg y obtenemos la flag:

![flag](https://github.com/user-attachments/assets/78575c5a-5a4f-4e6a-b641-4b682c22199d)

`flagmx{my_account_number_is_onetwotrhee}`


