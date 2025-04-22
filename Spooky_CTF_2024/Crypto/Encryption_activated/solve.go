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
