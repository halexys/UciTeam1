# Forensic / Memory puzzle

Extraemos el rar y tenemos un Windows Trace Log y un archivo 'flag.enc', entonces usamos Volatility para listar archivos:

`vol -f memory-puzzle.raw windows.filescan > file`

Revisando el resultado encontramos dos archivos en el escritorio de johndoe, 'system_update.py' y 'system_update.exe':

![py](https://github.com/user-attachments/assets/8996b3c1-afe9-410e-9387-e5c5424b1832)

![exe](https://github.com/user-attachments/assets/26135db0-db7d-4cd1-962a-4bcc8520db9e)

Volcamos el ejecutable:

`mkdir output ; vol -f memory-puzzle.raw -o "./output" windows.dumpfiles --virtaddr 0xb1083fcf40c0 --virtaddr 0xb1084089e960`

Lo abrimos con algun debugger como radare2 y obtenemos del decompilado que:

+ Abre un archivo flag.txt
+ Lo encripta usando AES-128-CBC con la clave 'SuperSecretKey12'
+ Lo almacena en un archivo flag.enc

![openflag](https://github.com/user-attachments/assets/e6391aa6-2c6c-44e0-9135-b811dce759fd)

![encryptflag](https://github.com/user-attachments/assets/46d8c60b-71f4-49fe-ac36-c930ef1e8b7f)

![key](https://github.com/user-attachments/assets/a8b28336-202e-436b-a139-e3cee10b8ef1)

![cifrado](https://github.com/user-attachments/assets/dcc69d7b-27d9-45c6-b52d-295d4880cfcd)

Asumiendo que el vector de inicializacion son 16 bytes puestos a 0 y que AES es un algoritmo de llave simetrica entonces aplicamos la operacion inversa con https://cyberchef.io/ y obtenemos la flag:

![flag](https://github.com/user-attachments/assets/b53942a0-e3eb-48ed-8e9e-29d5fd57785d)

`NICC{S1m0n_Tr4v3rses_T1m3}`
