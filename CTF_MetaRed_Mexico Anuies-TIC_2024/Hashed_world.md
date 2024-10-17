# Crypto / Hashed World

Obtenemos un zip con contraseña. Usamos john para encontrarla por fuerza bruta

![paso1](https://github.com/user-attachments/assets/b5a0cebd-9712-4741-8a42-8451fbe4f161)

![crack1](https://github.com/user-attachments/assets/091b534c-ad0a-471a-b409-2d5f3a3047f6)

Del zip extraemos un txt y un 7-zip, el txt contiene hashes, asi que se lo pasamos a Crackstation para intentar revelarlos y obtenemos la contraseña del 7-zip

![crack2](https://github.com/user-attachments/assets/e33dc9b9-7c60-4e4d-ba5f-ba99acd78fbf)

Obtenemos otro zip, esta vez con un 'flag.txt' dentro, usamos john con su diccionario por defecto para encontrar su contraseña

![crack3](https://github.com/user-attachments/assets/3ff5192f-a2b0-4452-af04-70c0ba881ba6)

Extraemos el archivo y obtenemos la flag

![final](https://github.com/user-attachments/assets/bd58c64a-6d14-422d-9b86-5d244ff7a792)

`flagmx{hashes_r_hard_to_crack}`
