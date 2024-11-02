# Misc / No access

Hay que hacer una petición a la API de Discord, primero busca tu token de usuario: https://robots.net/tech/how-to-get-your-discord-token/

Una vez tenemos el token hacemos una peticion a la API de discord para canales del grupo:
`curl -H "Authorization: TU_TOKEN_DE_ACCESSO" https://discord.com/api/v9/guilds/1158962403757785118/channels`

En la respuesta hay una canal con nombre 'super-secret' con la propiedad 'topic' conteniendo un valor en base64, esa es la flag:

![req](https://github.com/user-attachments/assets/ed3d465d-22b5-442c-9b28-e7286a5ac673)

![final](https://github.com/user-attachments/assets/7f880a1a-e7d0-481e-9a5d-47a53c036506)

`NICC{d03S_dISc0Rd_4Ll0W_tHiZ?}`
