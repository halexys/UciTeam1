# Forensic / Symphony

![noteAud](https://github.com/user-attachments/assets/6c257b5e-de3c-4753-b0eb-a5b65c28c0da)

Tenemos un archivo con datos en hexadecimal con dos 'X' en los bytes 3 y 4 respectivamente. Entonces lo decodificamos y guardamos:

![s1](https://github.com/user-attachments/assets/aaeb433b-3b8e-47a1-9a82-8752ef1a5441)

Comienza con 'RI' por lo que podria ser un archivo RIFF dañado, algunos programas como Audacity nos permiten abrir datos en bruto, asi que hacemos eso, abrimos Audacity y vamos a Archivo/Importar/Datos en bruto...; luego presionamos Detectar e Importar:

![noteAud](https://github.com/user-attachments/assets/d37382ba-8ea9-43cf-bbb8-96515c464f2e)

Si acercamos lo suficiente la Forma de Onda podemos ver bloques anchos y finos, agrupados de manera diferente, si le bajamos la velocidad de reproduccion encontramos que es codigo Morse. Entonces exportamos el audio y se lo pasamos a algun sitio que decodifique audio en Morse como https://morsecodemagic.com/morse-code-audio-decoder/. Otro enfoque podria ser traducir nosotros mismos como '-' y '.' los pitidos y pasarselo a algun decodificador de texto en Morse.

https://github.com/user-attachments/assets/46cb260f-fd4d-4246-a4d1-90502f2f2024

![morse1](https://github.com/user-attachments/assets/efcd69e4-11a0-4d97-90e6-2ba803bf2fed)

Nos piden formato: BattleCTF{t1_t2_t3_t4_t5}, y en la Forma de Onda observamos 4 espacios que separan algunos trozos del mensaje en 5 partes:

![rejas](https://github.com/user-attachments/assets/a5f134c2-5e0f-4dea-98d0-7ce33a53871f)

Formateando el mensaje nos queda: 

`BattleCTF{M0RS3_C0D3_!TRANSL4T0R@@WITH_4UD10_FE4TUR3512598648}`





