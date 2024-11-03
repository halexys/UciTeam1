# Forensic / Event code hunt

Tenemos un zip, dentro varios registros de eventos de Windows y la flag encriptada:

![eventocde](https://github.com/user-attachments/assets/b71b7584-621d-487d-9d22-9512f006f94d)

Convertimos a xml el archivo PowershellOP.evtx usando evtx_dump.py:

![s2](https://github.com/user-attachments/assets/c4724b5c-a68a-4fb4-9b18-776dfa5e2307)

Vemos un script de python:

![script](https://github.com/user-attachments/assets/6c262c9e-f4e3-4c72-b466-370f3a0cdc32)

Vemos que realiza un XOR y toma tres parametros, un archivo de salida, uno de entrada y una llave:

```
<Data Name="ScriptBlockText">python3 .\Documents\Chrome.py .\Documents\flag.txt .\Documents\encrypt_flag.txt I_Like_Big_Bytes_And_I_cannot_Lie!</Data>
```

Entonces nuestro script queda así:

``` python
import sys

def process_data(input_bytes, key):
 key_bytes = key.encode('utf-8')
 return bytearray([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(input_bytes)])

def main():
 if len(sys.argv) != 4:
  print('Usage: python script.py &lt;input_file&gt; &lt;output_file&gt; &lt;key&gt;')
  return

input_file = sys.argv[1]
output_file = sys.argv[2]
key = sys.argv[3]

with open(input_file, 'rb') as f:
 input_data = f.read()

result_data = process_data(input_data, key)  

with open(output_file, 'wb') as f:
 f.write(result_data)

if __name__ == '__main__':
    main()
```

Dado que ya tenemos todos los parametros, lo ejecutamos:

![final](https://github.com/user-attachments/assets/3b354ab9-424c-4daa-a057-2a8ee3c42b0d)

`NICC{Maya_Elmer_D3t3cts_Mal1c10us_P4yl04d_1n_3v3ntL0gs}`




