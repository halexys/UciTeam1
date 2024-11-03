# Forensic / Wont somebody think of the children

Obtenemos una imagen svg bastante pesada, podemos usar algun software como inkscape para separar las capas del svg. En una de estas capas se encuentra la flag. En mi caso usé un script en bash que separa las imagenes dentro del svg:

``` bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_file>"
  exit 1
fi

input_file="$1"
line_number=1

# Extraer y procesar las líneas del archivo de entrada
grep -oP 'base64,.*' "$input_file" | sed 's/base64,//' | sed 's/"\/>//' | while IFS= read -r line
do
  # Decodificar la línea Base64 y guardar como archivo .png
  echo "$line" | base64 --decode > "image_$line_number.png"
  ((line_number++))
done
```

![img5](https://github.com/user-attachments/assets/abccac29-e72e-4316-a691-d36fc2e0d44e)

`NICC{H3ck_th3m_kids_what_@bout_the_council?}`
