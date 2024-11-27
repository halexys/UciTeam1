Tenemos un mapa de bits y un 'delta' en formato binario. Un delta son los cambios realizados a un mapa de bits durante la codificacion en el contexto actual. Utilizamos una herramienta como xdelta3 que pueda decodificarlo

```
 >> xdelta3 decode -s null.bmp flag.bin modified.bmp

```

![bestdelta](https://github.com/user-attachments/assets/15ac6edd-fe6f-4de9-b918-9c4c12abd55b)

`EKO{b3st_d3lt4}`
