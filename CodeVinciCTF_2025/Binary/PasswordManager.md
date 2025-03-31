# Password Manager

Primero, revisando las strings nos percatamos de que el binario esta empaquetado con UPX asi que lo desempaquetamos

```
 strings passwordManager| grep UPX
UPX!
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 4.22 Copyright (C) 1996-2024 the UPX Team. All Rights Reserved. $
UPX!u
UPX!
UPX!

┌──(venv)─(kalcast㉿debian)-[~/Descargas]
└─$ ~/Herramientas/upx-4.2.4-amd64_linux/upx -d passwordManager
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2024
UPX 4.2.4       Markus Oberhumer, Laszlo Molnar & John Reiser    May 9th 2024

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
     24055 <-      7028   29.22%   linux/amd64   passwordManager

Unpacked 1 file.
```

Revisando con radare2 vemos la clave en la funcion main:

``` C
 sym.imp.printf("Give me the Master Password: ");
    *(puVar3 + -8) = 0x1233;
    iVar1 = sym.imp.__isoc99_scanf("%49s", &stack0xffffffffffffffb8);
    if (iVar1 == 1) {
        *(puVar3 + -8) = 0x1267;
        iVar1 = sym.imp.strcmp(&stack0xffffffffffffffb8, "CiaoSonoBenjaminQuestaPasswordNonLaVedraiMai");
```

```
chmod u+x passwordManager && ./passwordManager
Give me the Master Password: CiaoSonoBenjaminQuestaPasswordNonLaVedraiMai

Access Granted!
+----------------+-----------------------------------------------+
| Welcome        | To CodeVinci CTF                              |
+----------------+-----------------------------------------------+
| Website        | https://www.codevinci.it                      |
| Username       | benjamin                                      |
| Password       | 6e6578742074696d6520646f6e7420646f206974      |
| Flag           | CodeVinciCTF{d0n7_u5e_UpX_FoR_r3m0v3_1nFoS_}  |
| Secret Message | welcome to codevinci                          |
+----------------+-----------------------------------------------+
```

`CodeVinciCTF{d0n7_u5e_UpX_FoR_r3m0v3_1nFoS_}`
