
## Reto01
Utilizamos varias herramientas comunes en análisis de estenografía como file, cat, strings, steghide, y
stegsnow.

## Paso 1: Obtención y Descompresión del Archivo

En el reto nos proporcionan un archivo llamado reto01.zip. El primer paso fue descomprimir este archivo
utilizando el siguiente comando:

```bash
unzip Reto01.zip
```

Al descomprimir, listamos con ls el contenido de la carpeta y encontramos una serie de ficheros
nombrados de manera consecutiva.

![image](https://github.com/halexys/UciTeam1/assets/72656657/70fb7128-e9a2-48d2-a1a4-48a5494745f5)

## Paso 2: Identificación de los Ficheros

Utilizamos el comando file para determinar el tipo de cada fichero:

![image](https://github.com/halexys/UciTeam1/assets/72656657/cbd3b930-3d68-4037-a800-c37b07e60398)

Descubrimos que el primer archivo en la serie xa* es un archivo JPEG (jpg), mientras que los siguientes
archivos son de tipo data, sugiriendo que están asociados con la imagen inicial. Los últimos tres archivos
pertenecientes a la serie za* son identificados como un archivo comprimido (zip).

## Paso 3: Concatenación de los Ficheros

Procedimos a concatenar los archivos de cada serie para recomponer las imágenes y el archivo
comprimido original:

![image](https://github.com/halexys/UciTeam1/assets/72656657/6ddaeb50-248a-475d-9920-df6c8efcfdf7)

Descomprimimos el archivo file.zip obtenemos una imagen adicional (snow.jpg).

## Paso 4: Análisis Inicial de las Imágenes

Las imágenes corresponden a grandes nevadas ocurridas en Sevilla, las buscamos en Google Lens para
conocer más del contexto del ejercicio y alguna otra información adicional que pudiera ser de ayuda a la
solución del ejercicio.

![image](https://github.com/halexys/UciTeam1/assets/72656657/a0dc3f77-a2c5-4c1b-9837-1cdbbe591cf1)

![image](https://github.com/halexys/UciTeam1/assets/72656657/19ce8358-8e1d-44ef-8a7d-d340e8a421ac)

Con las dos imágenes (file.jpg y snow.jpg) obtenidas, utilizamos el comando strings para buscar pistas
textuales en los archivos:

![image](https://github.com/halexys/UciTeam1/assets/72656657/29cac896-255b-4695-814a-6790cab390b2)
