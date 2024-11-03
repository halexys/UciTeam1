# Misc / Two frames, one champ

Tenemos dos imagenes corruptas, si las vemos con: ` for i in {1..2}; do xxd image1.png | head -n 1 ; done` observamos que la firma de archivo de ambas es `FF 50 4E 47 0D 0A 1A 0A` pero deberia ser `89 50 4E 47 0D 0A 1A 0A`. Entonces usando programas como xxd y dd, o https://hexed.it/ editamos el primer byte.

![1](https://github.com/user-attachments/assets/73a93282-f481-460d-86aa-2cccfb62a001)

Tenemos que hacer un XOR entre ambas imagenes como indica la descripcion, para eso usamos alguna herramienta o un script, aqui un script en Go para la tarea:

``` go

package main

import (
	"fmt"
	"image"
	"image/color"
	"image/jpeg"
	"image/png"
	"os"
)

func main() {
	if len(os.Args) < 5 {
		fmt.Println("Usage xor2f <file1> <file2> <outputName> <outputFormat>")
    return
	}

  // Open the files
	file1, err := os.Open(os.Args[1])
  if err != nil { fmt.Printf("Error reading file: %s\n",os.Args[1]); return}
	file2, err := os.Open(os.Args[2])
  if err != nil { fmt.Printf("Error reading file: %s\n",os.Args[2]); return}
  defer file1.Close()
  defer file2.Close()

  // Decoding the images
  image1, _, err := image.Decode(file1)
  if err != nil { fmt.Printf("Error decoding image: %s\n",file1.Name()); return}
  image2, _, err := image.Decode(file2)
  if err != nil { fmt.Printf("Error decoding image: %s\n",file2.Name()); return}

  if image1.Bounds() != image2.Bounds() {
   fmt.Println("Images must be the same size")
   return
  }

  // Apply XOR
  bounds := image1.Bounds()
  resultImage := image.NewRGBA(bounds)
  for y:= bounds.Min.Y; y< bounds.Max.Y; y++ {
   for x := bounds.Min.X; x < bounds.Max.X; x++ {
    color1 := color.RGBAModel.Convert(image1.At(x,y)).(color.RGBA)
    color2 := color.RGBAModel.Convert(image2.At(x,y)).(color.RGBA)
    xorColor := color.RGBA{
      R: color1.R ^ color2.R, 
      G: color1.G ^ color2.G, 
      B: color1.B ^ color2.B, 
      A: color1.A,
    }
    resultImage.Set(x,y,xorColor)
   }
  }

  // Saving the new image
   outputFile, err := os.Create(os.Args[3])
   if err != nil {
    fmt.Println("Error opening file: %s",os.Args[3])
   }
   defer outputFile.Close()

   switch os.Args[4] {
    // as PNG
    case "png","PNG":
     err = png.Encode(outputFile,resultImage)
    // as JPEG
    case "jpeg","JPEG","jpg","JPG":
     err = jpeg.Encode(outputFile,resultImage,nil)
   }
   if err != nil {
    fmt.Println("Error encoding file as %s: %s",os.Args[4],os.Args[3])
    return
   }
   fmt.Println("XOR operation successful")
}
```

![2](https://github.com/user-attachments/assets/a3bd48ae-c75b-454f-b1ff-e24fffed19d5)

![3](https://github.com/user-attachments/assets/b28cca0f-475a-4883-bf97-bc4afbfeccaf)

`NICC{ch4mp_s19ht3d_0v0}`
