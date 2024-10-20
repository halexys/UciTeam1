# Stego / Bank WiiMX

Nos dan la siguiente imagen:
![Bank_WiiMX](https://github.com/user-attachments/assets/e739e262-bd3b-42e0-832a-dd1fe3315ada)

Y nos dicen que el mensaje oculto se encuentra de 'quitar la paleta de colores de la parte inferior a la superior', entonces usamos alguna herramienta para extraer paletas de colores de imagenes como https://pixelied.com/colors/image-color-picker para extraer cada patron RGB de la parte superior (de izquierda a derecha) y el del color negro de la parte inferior en RGB

![wiimx1](https://github.com/user-attachments/assets/c2694141-b14c-46b1-8bd9-d138f7cda92b)

Nos queda una lista de valores así para la parte superior:

```
122 128 117

123 129 140

143 138 117

137 128 136 

115 132 117

135 135 115

69 74 68

77 72 145
```

Restándole [20 20 20] que es el color RGB de la parte negra de abajo queda:
```
102 108 97

103 109 120

123 118 97

117 108 116

95 112 97

115 115 95

49 54 48

57 52 125
```

Convertimos de decimal a ASCII y obtenemos la bandera

![da](https://github.com/user-attachments/assets/f5b13f8b-3801-454f-80f2-0fa71b735f7d)

`flagmx{vault_pass_16094}`
