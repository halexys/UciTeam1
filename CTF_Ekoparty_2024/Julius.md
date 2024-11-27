Tenemos un archivo de datos en bruto, se obtiene una imagen con la flag al restarle 3 a cada byte, es decir, desplazarlos aritmeticamente, sabiendo que el titulo alude a Julio Cesar, el cifrado es similar al cifrado homónimo


``` python
# Nombre del archivo de entrada
input_file = "julius"  # Reemplázalo con el nombre de tu archivo si es diferente

# Nombre del archivo de salida en formato JPEG
output_file = "decoded_julius.jpg"

# Abrir el archivo de entrada en modo de lectura binaria
with open(input_file, "rb") as f:
    encoded_data = f.read()

# Desplazar cada byte hacia atrás en 3 posiciones
decoded_data = bytes((byte - 3) % 256 for byte in encoded_data)

# Escribir los datos decodificados en un nuevo archivo
with open(output_file, "wb") as f:
    f.write(decoded_data)

print("Decoding complete! The output is saved as decoded_julius.jpg")
```

![flag](https://github.com/user-attachments/assets/b5817bb5-5f1d-482d-8b39-d3b66b3bd930)

`EKO{Cis4rs_rul3z}`
