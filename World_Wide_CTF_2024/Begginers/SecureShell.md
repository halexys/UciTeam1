# Begginers / Secure Shell

Nos daban una pagina web en la cual podiamos escribir comandos, la mayoria los denegaba lo que nos daba a pensar que usaba
una whitelist en lugar de una blacklist de comandos. El comando `ls` y `echo` eran de los comandos permitidos, con `ls`
podíamos ver que en el directorio actual había un index.php, y `ls /` veíamos que habían varios archivos entre ellos un `readflag`.
Comencé el RCE usando \` command \` con echo: "echo \`cat index.php\`", el index dentro de los comentarios mencionaba los comandos permitidos,
`echo`,`ls`... Luego con "echo \`file /readflag\`" veíamos que era un binario y con "echo \`/readflag\`" leíamos la flag.  
