# Reto01

Utilizamos varias herramientas comunes en análisis de estenografía como file, cat, strings, steghide, y stegsnow.

## Paso 1: Obtención y Descompresión del Archivo

En el reto nos proporcionan un archivo llamado reto01.zip. El primer paso fue descomprimir este archivo utilizando el siguiente comando:

```bash
unzip Reto01.zip
```

Al descomprimir, listamos con `ls` el contenido de la carpeta y encontramos una serie de ficheros nombrados de manera consecutiva.

![image](https://github.com/halexys/UciTeam1/assets/72656657/412493ca-b1c6-406d-9ead-16cafc2a64cc)


## Paso 2: Identificación de los Ficheros

Utilizamos el comando file para determinar el tipo de cada fichero:

![image](https://github.com/halexys/UciTeam1/assets/72656657/b0a53093-a625-4e7a-96ba-7d07f87eb66f)


Descubrimos que el primer archivo en la serie xa\* es un archivo JPEG (jpg), mientras que los siguientes archivos son de tipo data, sugiriendo que están asociados con la imagen inicial. Los últimos tres archivos pertenecientes a la serie za\* son identificados como un archivo comprimido (zip).

## Paso 3: Concatenación de los Ficheros

Procedimos a concatenar los archivos de cada serie para recomponer las imágenes y el archivo comprimido original:

![image](https://github.com/halexys/UciTeam1/assets/72656657/f5b328f8-06dd-4d83-b7ea-068dc381738f)


Descomprimimos el archivo file.zip obtenemos una imagen adicional (snow.jpg).

## Paso 4: Análisis Inicial de las Imágenes

Las imágenes corresponden a grandes nevadas ocurridas en Sevilla, las buscamos en Google Lens para conocer más del contexto del ejercicio y alguna otra información adicional que pudiera ser de ayuda a la solución del ejercicio.

![image](https://github.com/halexys/UciTeam1/assets/72656657/67b9eca7-1931-4215-a82f-4ef950ea31c5)


![image](https://github.com/halexys/UciTeam1/assets/72656657/5cadea91-5199-48d6-94ac-0eb4324fcb81)


Con las dos imágenes (file.jpg y snow.jpg) obtenidas, utilizamos el comando strings para buscar pistas textuales en los archivos:

![image](https://github.com/halexys/UciTeam1/assets/72656657/eec39ae3-1682-4450-8705-1563a2b1e778)


En file.jpg no encontramos nada relevante, pero en snow.jpg descubrimos las siguientes cadenas:

`_ApparentlyThisIsAPassw0rd but the final password is not visible`

Esto nos sugirió que podría haber una contraseña y un mensaje oculto dentro de las imágenes. Utilizamos la herramienta stegsolve.jar en ambas imágenes en busca de algo oculto en los diferentes canales. También recurrimos a la herramienta online https://29a.ch/photo-forensics/, ninguna arrojo resultado alguno.

## Paso 5: Extracción de Datos Ocultos con Steghide

Decidimos utilizar steghide para buscar y extraer datos ocultos en ambas imágenes, empleando como passphrase la cadena obtenida anteriormente “\_ApparentlyThisIsAPassw0rd”:

![image](https://github.com/halexys/UciTeam1/assets/72656657/bbf95686-7751-4e14-8133-07d0c2144031)


Este comando nos permitió extraer un archivo flag.txt de la imagen file.jpg.

## Paso 6: Análisis del Archivo flag.txt

El archivo flag.txt contenía una breve explicación sobre por qué no nieva en Sevilla según el meteorólogo Juan Algar. Sin embargo, notamos que había caracteres no imprimibles (tabulaciones y espacios) al final de cada línea al abrir el archivo con nano:

![image](https://github.com/halexys/UciTeam1/assets/72656657/3cc5b469-0dcf-4a8a-8bd9-2f639571c65c)


Esto nos sugiere que hay algo oculto en el fichero flag.txt

## Paso 7: Extracción del texto oculto con Stegsnow

Para extraer el texto oculto en el contenido de flag,txt, utilizamos la herramienta stegsnow:

![image](https://github.com/halexys/UciTeam1/assets/72656657/fde3d701-7aaa-416b-847d-ce5265627069)


En el primer intento nos percatamos que el texto no era legible (debieron emplear la compresión) por lo que empleamos el parámetro –C para obtener el texto en formato legible. Esto nos permitió recuperar la flag final:

`flag{1s_v3ry_H00t}`
