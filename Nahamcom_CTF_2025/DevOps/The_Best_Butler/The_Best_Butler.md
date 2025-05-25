# The Best Butler 

En el escudo arriba a la derecha del panel administrativo nos muestra que la version de Jenkins y ls componentes usados son vulnerables, en especifico `CVE-2024-23897` (https://www.trendmicro.com/en_us/research/24/c/cve-2024-23897.html)

De acuerdo a esto jenkins tiene una CLI mediante la cual es posible hacer lectura arbitraria, descargando el .jar que nos especifican en /cli/:

![2025-05-25-175145_1349x588_scrot](https://github.com/user-attachments/assets/d070362f-67e9-4abc-a469-3337b2c964f7)

Podemos explotar esta vulnerabilidad con el siguient comando:

![2025-05-23-213248_951x91_scrot](https://github.com/user-attachments/assets/1a201891-b3bc-4ae6-9eac-f3f2ccd4f614)

