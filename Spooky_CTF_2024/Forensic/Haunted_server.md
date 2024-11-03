# Forensic / Haunted Server

+ Convertir de .aff a .raw: `affconvert -r haunted-server.aff`
+ Extraer el volumen logico: `7z x haunted-server.raw`
+ Asignar el volumen logico a un dispositivo de bucle: `sudo losetup -fP 1.lvm`
+ Escanear y activar el grupo de volumenes: `sudo vgscan && sudo vgchange -ay`
+ Identificr volumen logico: `sudo lvdisplay`
+ Montar volumen logico: `sudo mount  /dev/cs_simonserver/root /lvmount/`

Perfecto, tenemos la particion lista, con la pista que nos dan buscamos en https://attack.mitre.org/techniques/T1546/004/ y vemos los archivos que podria usar el atacante para garantizar persistencia. En .bashrc encontramo la primera parte de la bandera en base64:
 
![bashrc](https://github.com/user-attachments/assets/7605a155-b1f7-429a-af0c-f36ae4b80a09)

En .vimrc vemos que estuvo modificando un archivo peculiar:

![vimrc](https://github.com/user-attachments/assets/74dae5e3-4340-4c40-a2af-438b3dbe8400)

Resulta ser un script de python, y encontramos la segunda parte de la bandera, tambien en base64:

![systemcotrol](https://github.com/user-attachments/assets/2944f2f0-a6a0-4c88-a8eb-521aae49dd3c)

`NICC{rb_wuz_h3r3_hahahaha}`

+ Desmontar el volumen logico: `sudo umount /lvmount`
+ Desactivar el dispositivo de bucle: `sudo losetup -d 1.lvm`

