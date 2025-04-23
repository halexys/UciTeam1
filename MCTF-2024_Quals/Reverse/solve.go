package main

import (
	"os"
	"strings"
)

var lookupTable = map[rune]rune{
    'v': 'w', 'j': '5', 't': 'x', '}': 'g', 'y': 'o', 'z': 'e', 'i': '{', 'h': '4', 'n': 'b', 'c': '8',
    'm': 'p', 'a': '7', 'l': 'u', '_': 'q', '0': 'd', 'f': 's', '2': 'k', '3': '6', '1': 'r', '9': '9',
    'r': '1', '6': '3', 'k': '2', 's': 'f', 'd': '0', 'q': '_', 'u': 'l', '7': 'a', 'p': 'm', '8': 'c',
    'b': 'n', '4': 'h', '{': 'i', 'e': 'z', 'o': 'y', 'g': '}', 'x': 't', '5': 'j', 'w': 'v',
 }
 var firstString = "p8xsi8dlba61rb9q0obhpr8qhbhuojrjqrjqshr1uoqjrpmu6"

func main() {
 if len(os.Args) != 2 {
   os.Exit(1)
 }
 // flag
 secondString := strings.Map(transform,os.Args[1])

 // lookupTable es bidireccional, transform(transform(str)) == str
 // aqui obtenemos la flag pasando cualquier argumento
 flag := strings.Map(transform,firstString)
 print(flag)

 if secondString != firstString {
   os.Exit(1)
 }
 os.Exit(0)
}

func transform(r rune) rune {
 mapped, ok := lookupTable[r]
 if ok {
  return mapped
 }
 return r
}
