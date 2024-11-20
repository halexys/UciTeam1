# Web / Jenkins

Entramos a un sitio web creado con Jenkins:

![jenkins1](https://github.com/user-attachments/assets/f66d68e8-5eb1-4ee1-87af-f0f0ff18908a)

La ruta /jnlpJars/ contiene archivos JAR necesarios para la comunicación entre el servidor Jenkins y los agentes remotos. Normalmente contiene 'agent.jar' y 'jenkins-cli.jar'

![jenkins2](https://github.com/user-attachments/assets/22105d87-c5a0-4bfb-acce-c21183698baa)

Existe una vulnerabilidad reciente de Jenkins que permite leer archivos total o parcialmente de manera remota por medio de jenkins-cli, **CVE-2024-23897**

![jenkins4](https://github.com/user-attachments/assets/c67e62c0-9218-43e4-9708-daaa78d55ab6)

Al parecer los permisos de lectura eran globales, esto funcionó:

![jenkinsf](https://github.com/user-attachments/assets/ad5560ca-ddfe-4928-a96e-2cd63a732a41)

`BattleCTF{se_me_olvido_la_flag_y_el_sitio_ya_no_esta_disponible}`


