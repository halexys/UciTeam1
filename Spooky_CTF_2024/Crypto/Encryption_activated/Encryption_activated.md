# Crypto / Encryption activated

Nos dan un script de python con una función 'mycipher' y un archivo 'flag.output' con un mensaje cifrado:
``` python 
def mycipher(myinput):
    global myletter
    rawdecrypt = list(myinput)
    for iter in range(0,len(rawdecrypt)):
        rawdecrypt[iter] = chr(ord(rawdecrypt[iter]) + ord(myletter))
        myletter = chr(ord(myletter) + 1)
    encrypted = "".join(rawdecrypt)
    print("NICC{" + encrypted + "}")

```

La función recibe una cadena de entrada, la convierte en una lista de caracteres, se define un letra, luego se itera sobre la lista de caracteres cambiando cada caracter con el resultado de la suma del valor ASCII del caracter actual con el valor ASCII de la letra, luego el valor ASCII de la letra aumenta en 1, es decir, se desplaza. Lo que tenemos que hacer es probar todos los posibles resultados de esta función para cada valor de myletter, aceptando como myinput el contenido de 'flag.input' y encontrar algo con significado que pueda ser la flag. Puede optarse por modificar el propio script de python, yo prefiero usar Go:

``` go
package main
import (
	"fmt"
	"os"
)
func main(){
 message,_ := os.ReadFile("flag.output")
 var decrypted string

 for ascii_num:= 0; ascii_num <=127; ascii_num++ {
  ascii_letter := ascii_num
  for _,char := range(string(message)) {
   decrypted += string(int(char)+ascii_letter)
   ascii_letter++
  }
  fmt.Printf("ASCII %d -> NICC{%s}\n",ascii_num,decrypted)
  decrypted = ""
 }
} 
```

![fina](https://github.com/user-attachments/assets/084571a6-6ad4-4c36-8d3c-bb6a4c8b4a8a)

`NICC{WAt_dO_yOu_tHINk_of_My_cIpHerG}`
