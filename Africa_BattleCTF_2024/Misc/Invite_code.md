# Misc / Invite Code

En el servidor de discord encontramos un mensaje sospechoso:

![misc2](https://github.com/user-attachments/assets/e2bb714d-73b4-4f56-a8d0-4d68898cd40b)

Tenemos algo en base64 y una url, ignoramos lo primero porque al final es un enlace de youtube que no sirve para nada

![2](https://github.com/user-attachments/assets/27710531-418b-4a28-8c9b-6b4c20228946)

La direccion contiene un archivo comprimido con gzip y codificado con base64, hacemos las operaciones a la inversa y obtenemos esto:

![3](https://github.com/user-attachments/assets/00f7aa61-e26f-4a49-b961-7d2cbcd8fbb6)

![4](https://github.com/user-attachments/assets/f853b348-9758-42b3-b69b-0c2467a494a8)

![5](https://github.com/user-attachments/assets/e61f8b9d-32fb-4663-acd7-9dc7b3f2c2cf)

Hay un hash de bcrypt y datos en hexadecimal encriptados con RC4, entonces encontramos el valor del hash con John The Ripper o Hashcat:

![j1](https://github.com/user-attachments/assets/7d3418f3-01bb-4916-8d54-37af04a61204)

![j2](https://github.com/user-attachments/assets/f8be862b-e146-435d-820c-7d268a8dd662)

Y desencriptamos la informacion:

![final](https://github.com/user-attachments/assets/2709ad3e-d55e-45de-93d9-362383bead70)

`battleCTF{pwn2live_d7c51d9effacfe021fa0246e031c63e9116d8366875555771349d96c2cf0a60b}`
