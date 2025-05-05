# RAMblings of Cornelia

```
file cornelias-memory.raw
cornelias-memory.raw: ELF 64-bit LSB core file, x86-64, version 1 (SYSV), SVR4-style
```

Es un "core file", un volcado de memoria, si vemos las cadenas verificamos que es un volcado en un sistema Windows:
```
strings cornelias-memory.raw | grep -F "C:\\" | head
C:\WINDOWS\system32
SystemRoot=C:\Windows
WC:\KuaiwanBox\src\XXBrowserBHO\out\Release\x86\XXBrowserBHOx86.pdb!#ALF:HSTR:VirTool:Win32/CeeInject.LH
@C:\Program Files\Common Files\Microsoft Shared\Ink\mip.exe,-291
@C:\Windows\System32\AuthFWGP.dll,-20
@C:\Windows\system32\msconfig.exe,-5006
C:\WINDOW
/C:\
/C:\
C:\myapp.exe
```

Obtenemos la estructura del sistema de archivos con Volatility: `volatility -f cornelias-memory.raw windows.filescan.FileScan | tee filesystem.txt`

Filtramos por palabras clave y encontramos un par de archivos interesantes:
```
cat filesystem.txt | grep -E "cornelia|secret|intel|password"
0xb7873d37d220	\Windows\System32\drivers\intelppm.sys
0xb7873fe4bd20	\Users\sawat\company-intel.7z
0xb78741195900	\Users\sawat\company-intel.7z
0xb78742406380	\Users\cornelia\kind-reminder.txt
0xb78742b46890	\Users\sawat\company-intel.7zy-intel.7z
0xb78742b5d180	\Users\kiyas\AppData\Roaming\Microsoft\Windows\Recent\cornelia.lnk
0xb78743184500	\Users\cornelia\master-plan.txt
```

Volcamos `master-plan.txt` y `kind-reminder.txt`:
```
 volatility -f cornelias-memory.raw windows.dumpfiles.DumpFiles --virtaddr 0xb78743184500
Volatility 3 Framework 2.11.0
Progress:  100.00		PDB scanning finished
Cache	FileObject	FileName	Result

DataSectionObject	0xb78743184500	master-plan.txt	file.0xb78743184500.0xb78743147a10.DataSectionObject.master-plan.txt.dat
```

```
volatility -f cornelias-memory.raw windows.dumpfiles.DumpFiles --virtaddr 0xb78742406380
Volatility 3 Framework 2.11.0
Progress:  100.00		PDB scanning finished
Cache	FileObject	FileName	Result

DataSectionObject	0xb78742406380	kind-reminder.txt	file.0xb78742406380.0xb78741b04350.DataSectionObject.kind-reminder.txt.dat
```

En `master-plan.txt` nos dice que no confiemos en la compañia (sawat), que el archivo que guardan todavia esta en el sistema y que lo veamos

En `kind-reminder.txt` parece haber una contraseña

Volcamos entonces el archivo `company-intel`:
```
volatility -f cornelias-memory.raw windows.dumpfiles.DumpFiles --virtaddr 0xb7873fe4bd20
Volatility 3 Framework 2.11.0
Progress:  100.00		PDB scanning finished
Cache	FileObject	FileName	Result

DataSectionObject	0xb7873fe4bd20	company-intel.7z	file.0xb7873fe4bd20.0xb78742786490.DataSectionObject.company-intel.7z.dat
SharedCacheMap	0xb7873fe4bd20	company-intel.7z	file.0xb7873fe4bd20.0xb78740631990.SharedCacheMap.company-intel.7z.vacb
```

Usamos la contraseña que encontramos para descomprimirlo:
```
mv file.0xb7873fe4bd20.0xb78742786490.DataSectionObject.company-intel.7z.dat company-intel.7z

7z x company-intel.7z

7z x company-intel.7z

7-Zip 24.07 (x64) : Copyright (c) 1999-2024 Igor Pavlov : 2024-06-19
 64-bit locale=es_CU Threads:4 OPEN_MAX:1024

Scanning the drive for archives:
1 file, 2150400 bytes (2100 KiB)

Extracting archive: company-intel.7z

Enter password (will not be echoed):

WARNINGS:
There are data after the end of archive

--
Path = company-intel.7z
Type = 7z
WARNINGS:
There are data after the end of archive
Physical Size = 2147505
Tail Size = 2895
Headers Size = 273
Method = LZMA2:3m 7zAES
Solid = +
Blocks = 1

Everything is Ok

Archives with Warnings: 1

Warnings: 1
Files: 2
Size:       2148136
Compressed: 2150400
```

Dentro encontramos una imagen con la flag:
![hq](https://github.com/user-attachments/assets/abf57aea-5b16-4893-9af2-3cfb9ed6a1ba)

`UVT{C0rn3l1a_dUmPs_tH3_r4W_tRutH}`

