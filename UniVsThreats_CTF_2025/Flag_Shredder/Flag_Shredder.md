# Flag Shredder

```
file freeflags.img
freeflags.img: DOS/MBR boot sector, code offset 0x3c+2, OEM-ID "mkfs.fat", sectors/cluster 4, reserved sectors 4, root entries 512, Media descriptor 0xf8, sectors/FAT 128, sectors/track 32, heads 8, sectors 131072 (volumes > 32 MB), reserved 0x1, serial number 0x2d08ca2, unlabeled, FAT (16 bit)
```

Montamos el archivo (-o loop para montarlo como un dispositivo de bloques) (-t vfat porque es un sistema de archivos FAT)
`sudo mount -o loop freeflags.img /mnt/freeflags -t vfat`

El sistema de archivos solo tiene un ejecutable, actualmente inutil.

Revisamos los archivos borrados:
```
 fls -r -f fat16 freeflags.img
r/r 5:	Run_for_flag.exe
r/r * 8:	Maybe_Real_Flag.png
v/v 2092995:	$MBR
v/v 2092996:	$FAT1
v/v 2092997:	$FAT2
V/V 2092998:	$OrphanFiles
```

Encontramos una imagen eliminada, la recuperamos por el inodo:
```
istat -f fat16 freeflags.img 8
Directory Entry: 8
Not Allocated
File Attributes: File, Archive
Size: 11030
Name: _AYBE_~1.PNG

Directory Entry Times:
Written:	2025-05-02 19:44:16 (CDT)
Accessed:	2025-05-02 00:00:00 (CDT)
Created:	2025-05-02 19:44:17 (CDT)

Sectors:
16724 16725 16726 16727 16728 16729 16730 16731
16732 16733 16734 16735 16736 16737 16738 16739
16740 16741 16742 16743 16744 16745 0 0
```

Y la flag esta en la imagen:

![Maybe_Real_Flag](https://github.com/user-attachments/assets/bf8a1743-ee3d-41b4-af9b-20e278b93b28)

`UVT{D3l3t3d_But_N0t_D3stRoy3d}`
