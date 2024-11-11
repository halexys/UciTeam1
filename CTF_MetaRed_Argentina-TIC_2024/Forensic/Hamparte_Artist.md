# Forensic / Hamparte Artist

Tenemos un volcado de memoria de Windows, analizamos los procesos con:

`python3 vol.py -f MEMORY.DMP windows.pslist.PsList`

Volcamos el proceso de mspaint.exe porque el titulo sugiere el arte:

`vol.py -f MEMORY.DMP --output-dir=. windows.memmap.Memmap --pid 2808 --dump`

Abrimos el archivo resultante como datos en bruto en algun editor de imagenes como GIMP y modificando el desplazamiento y la anchura se encuentra un texto reflejado:

![whois](https://github.com/user-attachments/assets/6e0fc450-b9e1-4e25-aaa7-28fd1977ecb1)

Hacemos una captura de pantalla y volteamos la imagen:

![magick](https://github.com/user-attachments/assets/9e6bf712-7271-4546-a650-6eb6bc55b81e)

`flag{who-is-cr7}`
