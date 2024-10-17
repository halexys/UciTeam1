# OSINT / Cybro

Es un reto de Osint, donde te daban un perfil de facebook:

![1000000000000556000003007ED271E9](https://github.com/user-attachments/assets/e36a4fb9-5700-4e8a-8ef4-347d6fbc8d79)

Buscando un poco entre las publicaciones, nos encontramos con esto: **(HIENXDVCOXFS)**

![10000000000005560000030040FF4C1B](https://github.com/user-attachments/assets/c48b7d06-1665-4499-ab27-74c5df85923a)

Al parecer es un mensaje pero no está del todo claro. Luego de seguir investigando el facebook, nos podemos dar cuenta de que entre sus gustos se encuentra la plataforma Telegram:

![10000000000005560000030060971B6B](https://github.com/user-attachments/assets/57ef6f9a-4a72-4bc4-87be-c522ad411ee0)

Asi que buscamos el mismo nombre del perfil en Telegram y entre las opciones, una nos devuelve un mensaje, la flag, pero esta codificada:

![1000000000000556000003001491CE33](https://github.com/user-attachments/assets/95b0ce12-b66e-4f78-8bb2-807ef7261edc)

**mtetja{rkhe_hqizs_ybdmpg_xsv_kmjrkgn}**

Al parecer esta utilizando un método de cifrado por sustitución, ya que la flag mantiene el formato pero los caracteres cambian, asi que intentamos descifrarla en https://www.dcode.fr

Nos identifica que es el cifrado de Vigenere, cifrado por sustitución polialfabética:

![100000000000055600000300BADC1858](https://github.com/user-attachments/assets/3269d9b6-d606-4359-95b5-c4692c8f9879)

Por lo tanto lo desciframos y encontramos la flag:

![100000000000055600000300D6435FC0](https://github.com/user-attachments/assets/11ff091a-2e8f-44af-bc98-bf7ae7a95b54)

`flagmx{with_cybro_learns_and_defends}`
