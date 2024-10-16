# Network / Infiltrated Spy

Aquí también recibimos un archivo de captura, lo abrimos con Wireshark y hay tráfico HTTPS, así que descargamos todo (Archivos/Exportar Objetos/HTTP...). Vemos que los 'insert-libro.php' lucen asi:

![123](https://github.com/user-attachments/assets/2c6fe4a9-1daa-4012-a125-bc1a96e33b00)

En la descripción del reto nos dicen que alguien puede estar enviando mensajes codificados y dentro de 'libro.js' se encuentran unas funciones 'encrypt' y 'decrypt', asumimos que esto se usa para el cifrado del mensaje, así que creamos un script para simular 'decrypt' (también se puede usar ese mismo código javascript con nodejs), en mi caso usaré Go

```
package main

import (
	"bufio"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"os"
)


func main() {
 // Entrada
 reader := bufio.NewReader(os.Stdin)
 encrypted_string,_ := reader.ReadString('\n')

  // Desplazamiento ASCII - 1
  shifted := ""
  for _,char := range(encrypted_string) {
    shifted += string(int(char-1))
  } 

   // Hexadecimal a base64
   hexed,_ := hex.DecodeString(shifted) 

   // Base64 a texto plano
   plaintext,_ := base64.StdEncoding.DecodeString(string(hexed))
   fmt.Println(string(plaintext))
}
```

Entonces pasamos como entrada estándar los mensajes de cada llamada a insert-libro.php:

![flag](https://github.com/user-attachments/assets/c6377c2d-8ddc-42bd-a42a-c73cfd6ebc3c)

`flagmx{internal_spy_data_leak}`
